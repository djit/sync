# download and save xml file
import os
from os.path import dirname
import requests

DIR = dirname(dirname(os.path.abspath(__file__)))


# retrieve and parse XML feed
def gethttpfeed(source, feed_url, cached=False):
    # download xml file if requested no cache
    xml_feed_path = DIR + '/feeds/' + source + '.xml'

    if(not cached or cached and not os.path.exists(xml_feed_path)):
        try:
            headers = {'user-agent': 'Mozilla/5.0'}
            req = requests.get(feed_url, headers)

            with open(xml_feed_path, "wb") as file:
                file.write(req.content)

            print('- feed downloaded to', xml_feed_path)
            return xml_feed_path
        except Exception as e:
            print(e)
            return None
    else:
        if os.path.isfile(xml_feed_path):
            print('- using cached file', xml_feed_path)
            return xml_feed_path
        else:
            return None
