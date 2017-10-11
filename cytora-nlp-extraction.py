import glob
import json
import logging
import sys
from argparse import ArgumentParser
from itertools import chain

import spacy

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)
stream_handler = logging.StreamHandler(sys.stdout)
logger.addHandler(stream_handler)


def parse_file(path):
    # Parses the json file and returns dict
    with open(path, 'r') as infile:
        try:
            data = json.load(infile)
        except json.JSONDecodeError as e:
            logger.error("Failed to read file {}".format(path))
            raise Exception()

    logger.info("Successfully read file {}".format(path))
    return data


def extract_entities(data, nlp):
    # Receives a data dict and extracts named entities
    # This code comes from Cytora's NLP tutorial
    if 'title' not in data.keys() or 'content' not in data.keys():
        logger.error("Incomplete data in json file")
        raise Exception()

    analysed_title = nlp(data['title'])
    analysed_content = nlp(data['content'])

    all_entities = chain(analysed_title.ents, analysed_content.ents)

    organisation_set = set()
    people_set = set()
    geolocation_set = set()

    for ent in all_entities:
        if ent.label_ not in ['PERSON', 'GPE', 'ORG']:
            continue

        if ent.label_ == 'PERSON':
            people_set.add(ent.text)
            logger.info("Found {} of type PERSON".format(ent.text))
        elif ent.label_ == 'ORG':
            organisation_set.add(ent.text)
            logger.info("Found {} of type ORG".format(ent.text))
        elif ent.label_ == 'GPE':
            geolocation_set.add(ent.text)
            logger.info("Found {} of type GPE".format(ent.text))
        else:
            raise Exception()

    logger.debug(people_set)
    logger.debug(organisation_set)
    logger.debug(geolocation_set)

    if len(people_set) > 0:
        data['personal_ents'] = list(people_set)

    if len(organisation_set) > 0:
        data['organisations'] = list(organisation_set)

    if len(geolocation_set) > 0:
        data['geo_locations'] = list(geolocation_set)


def main():
    parser = ArgumentParser()

    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument('-f', '--file',
                       help='File to extract entities from.')
    group.add_argument('-d', '--dir',
                       help='Directory to extract entities from.')

    args = parser.parse_args()

    logger.info("Initializing SpaCy EN model...")
    nlp = spacy.load('en')
    logger.info("Done!")

    data = parse_file(args.file)
    analysed_data = extract_entities(data, nlp)


if __name__ == '__main__':
    main()
