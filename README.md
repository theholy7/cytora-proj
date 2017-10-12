## Cytora project

This is the project for Cytora. Entity extraction from news articles using SpaCy.

Make your virtualenv with python 3.6.2

Install requirements with `pip install -r requirements.txt`

Run `python -m spacy download en` to download the EN model

Don't forget to get a googlemaps API key with access to the Geocoding API

Run the code with `python cytora-npl-extraction.py -f path/to/jsonfile -k google_api_key`

## TODO
1. Tests
2. Better logging
3. Don't repeat geocode queries for already know geolocations
