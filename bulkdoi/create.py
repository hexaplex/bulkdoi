#!/usr/bin/env python3
# coding: utf8

'''Given DOI data as input, create DOIs via web service
'''

import sys
import argparse
import logging
import json
import csv
import random
import string
import datacite
import dcdata
import services

LOGGER = logging.getLogger(__name__)
logging.basicConfig(filename='example.log', filemode='w', level=logging.DEBUG)

def get_args():
    '''Get command line arguments as well as configuration settings'''
    parser_desc = 'Create DOIs from input file.'
    parser = argparse.ArgumentParser(description=parser_desc)
    parser.add_argument("requests", help="CSV formatted file of DOI requests")
    parser.add_argument("-c", "--config", help="Config file path (defaults to './config.json')", default='config.json')
    #parser.add_argument('-v', '--verbose', action='store_true', help="Show detailed output")
    parser.add_argument('-s', '--submit', action='store_true', help="Submit DOI data to Datacite")
    parser.add_argument('-l', '--live', action='store_true', help="Create DOIs on the live system instead of the test system")
    parser.add_argument('-p', '--publish', action='store_true', help="Publish DOIs in addition to creating them. Note that published DOIs cannot be deleted.")
    args = vars(parser.parse_args())
    return args

def get_config(path):
    with open(path) as json_data_file:
        settings = json.load(json_data_file)
    return settings

def gen_data(infile):
    with open(infile) as csvfile:
        reader = csv.DictReader(csvfile)
        for r in reader:
            yield r

def gen_request_data(data):
    for d in data:
        yield make_request_data(d)

def gen_suffix():
    chars = '0123456789bcdfghjkmnpqrstvwxyz' # alphanum without vowels and l
    while True:
        yield ''.join([random.choice(chars) for _ in range(8)])

def make_request_data(csvdata):
    request_data = {}
    request_data['url'] = csvdata['URL']
    request_data['creators'] = csvdata['Creators']
    request_data['title'] = csvdata['Title']
    request_data['publisher'] = csvdata['Publisher']
    request_data['publication_year'] = csvdata['Publication Year']
    request_data['resource_type'] = csvdata['Resource Type']
    request_data['description'] = csvdata['Description']
    return request_data

def main():
    args = get_args()
    datacite_params = get_config(args['config'])
    if args['live']:
        datacite_settings = datacite_params['datacite_live']
    else:
        datacite_settings = datacite_params['datacite_test']
    datacite_service = datacite.DataciteService(datacite_settings)
    names = services.DOINameGenerator(datacite_service, gen_suffix()).doi_names()
    doi_service = services.DOIService(datacite_service, dcdata.create_payload, names)
    data = gen_data(args['requests'])
    for request in gen_request_data(data):
        #print(request) 
        doi = doi_service.submit_doi(request, submit=args['submit'])
        print(doi)

if __name__ == "__main__":
    sys.exit(main())
