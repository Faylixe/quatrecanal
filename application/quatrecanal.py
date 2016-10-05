#!/usr/bin/python

import random
import requests

from random import randint

from flask import Flask, request, Response

# Extension supported sorted by priority.
PRIORITY = ['.gif', '.webm', '.png', '.jpg']

# Access token for slack integration.
ACCESS_TOKEN = os.environ.get('SLACK_WEBHOOK_TOKEN')

class Crawler:
    """ 4Chan crawler based on read only API. """

    def __init__(self, board='b'): # TODO : Add filter.
        """ Default constructor. """
        self.board = board
        self.images = {}

    def getResource(self, name):
        """ Retrieves JSON resources for the given <tt>name</tt>. """
        endpoint = 'http://a.4cdn.org/%s/%s.json' % (self.board, name)
        response = requests.get(endpoint)
        return response.json()

    def getURL(name, extension):
        """ Retrieves the image denoted by the given filename. """
        return 'http://i.4cdn.org/%s/%ss%s' % (self.board, name, extension)

    def parseImages(self, threads):
        """ Parses given threads list to index available images. """
        for thread in threads:
            for post in thread['posts']:
                if 'tim' in post:
                    name, extension = post['tim'], post['ext']
                    # TODO : Filter tim.
                    if not extension in images:
                        self.images[extension] = []
                    self.images[extension].append(name)

    def getRandomImage(self):
        """ Main access point : parse image from first board page
        and return random image based on image extension priority.
        """
        firstpage = getResource(1)
        if not 'threads' in firstpage:
            return -1, 'No thread provided'
        parseImages(firstpage['threads'])
        for extension in PRIORITY:
            if extension in self.images:
                selected = randint(0, len(self.images[extension]))
                return 0, self.images[extension][selected]
        return -1, 'No valid resource found'

# Web service instance.
service = Flask(__name__)

@service.route('/', methods=['POST'])
def webhook():
    """ Webhook implementation. """
    if request.form.get('token') == ACCESS_TOKEN:
        return Response('Animated porn is coming'), 200
    return 401

if __name__ == '__main__':
    service.run()
