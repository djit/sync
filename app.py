#!/usr/bin/env python

import traceback
import argparse
import configparser
from lib import FeedDownloader, FeedParser, Keywords, Formater
from pymongo import MongoClient
import json


class SyncManager(object):
    """docstring for syncmanager"""
    def __init__(self, source=''):
        self.source = source

    # run the sync process
    def run(self):
        print('- running sync for feed', self.source)

        try:
            config = configparser.RawConfigParser()
            config.read('sources/' + self.source + '.ini')
            self.config = config
            self.process()
        except Exception:
            traceback.print_exc()


    # start the sync process using the feed config
    def process(self):
        feedName = self.config['DEFAULT']['Name']
        feedUri = self.config['Feed']['Uri']
        feedItemTag = self.config['Feed']['ItemTag']
        productsMapping = json.loads(self.config['Mapping']['Products'])
        categoriesMapping = json.loads(self.config['Mapping']['Categories'])
        print('- processing source', feedUri)

        # 1 - download feed
        feed = FeedDownloader.gethttpfeed(feedName, feedUri, True)

        # 2 - parse feed
        if feed:
            xmlTree = FeedParser.xmlparser(feed, feedItemTag)
        else:
            print(feedName + ' file not found')
            return

        # 3 - run xml feed through profile mapping
        data = self.parse(xmlTree, productsMapping, categoriesMapping)

        # 4 - store data in db
        if data:
            client = MongoClient('mongodb://localhost:27017')
            db = client.discounted

            # delete & insert products data for this source
            db.products.remove({ 'source': feedName })
            result = db.products.insert_many(data)
            print('- ' + str(len(result.inserted_ids)) + ' item inserted')


    # parse feed and return data array
    def parse(self, xmlTree, productsMapping, categoriesMapping):
        print('- running parse')
        #print('- mapping', mapping['description'])

        data = []  # array of feed items
        for entry in xmlTree:
            fields = {}
            originalFields = {}
            fields['source'] = self.config['DEFAULT']['Name']
            fields['logo'] = self.config['DEFAULT']['Logo']
            for node in entry:
                # if node has children, loop throug them and get all text
                if list(node):
                    fields[node.tag] = []
                    for child in node.itertext():
                        if child.strip():
                            originalFields[node.tag].append(child.rstrip())
                # if not children, get node text
                else:
                    if node.text:
                        originalFields[node.tag] = node.text.rstrip().lower()

                # map source fields with products fields
                if node.tag in originalFields and node.tag in productsMapping:
                    fields[productsMapping[node.tag]] = originalFields[node.tag]

                # map source category value with products category
                if(node.tag == 'product_type'):
                    if(originalFields[node.tag] in categoriesMapping.values()):
                        print('category mapping for ' + list(categoriesMapping.keys())[list(categoriesMapping.values()).index(originalFields[node.tag])])
                        fields['category'] = list(categoriesMapping.keys())[list(categoriesMapping.values()).index(originalFields[node.tag])]
                    else:
                        break

            if(fields['category'] in categoriesMapping):
                data.append(fields)

        return data


if __name__ == '__main__':
    # get args
    parser = argparse.ArgumentParser(description='sync process')
    parser.add_argument('--source', dest='source', help='source name')
    args = parser.parse_args()
    source = args.source

    # instantiate syncManager
    manager = SyncManager(source)
    manager.run()
