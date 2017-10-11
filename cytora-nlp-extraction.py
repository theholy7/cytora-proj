import glob
import json
import logging
import sys
from argparse import ArgumentParser

import spacy

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
stream_handler = logging.StreamHandler(sys.stdout)
logger.addHandler(stream_handler)


def parse_file(path):
    with open(path, 'r') as infile:
        try:
            data = json.load(infile)
        except json.JSONDecodeError as e:
            logger.error("Failed to read file {}".format(path))
            raise Exception()

    logger.info("Successfully read file {}".format(path))
    return data


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


if __name__ == '__main__':
    main()
