#!/usr/bin/python

import json
import os
import random
import requests

from random import randint

from flask import Flask, request, Response

# Extension supported sorted by priority.
PRIORITY = ['.gif', '.webm', '.png', '.jpg']

# Access token for slack integration.
ACCESS_TOKEN = os.environ.get('SLACK_WEBHOOK_TOKEN')

# Default board to use.
DEFAULT_BOARD = 'gif'

def getBoards():
    """ Retrieves list of available boards. """
    response = requests.get('http://a.4cdn.org/boards.json')
    json = response.json()
    boards = []
    for board in json['boards']:
        boards.append(board['board'])
    return boards

class Crawler:
    """ 4Chan crawler based on read only API. """

    def __init__(self, board): # TODO : Add filter.
        """ Default constructor. """
        self.board = board
        self.images = {}

    def getResource(self, name):
        """ Retrieves JSON resources for the given <tt>name</tt>. """
        endpoint = 'http://a.4cdn.org/%s/%s.json' % (self.board, name)
        response = requests.get(endpoint)
        return response.json()

    def parseImages(self, threads):
        """ Parses given threads list to index available images. """
        for thread in threads:
            for post in thread['posts']:
                if 'tim' in post:
                    name, extension = post['tim'], post['ext']
                    # TODO : Filter tim.
                    if not extension in self.images:
                        self.images[extension] = []
                    self.images[extension].append(name)

    def getRandomImage(self):
        """ Main access point : parse image from first board page
        and return random image based on image extension priority.
        """
        firstpage = self.getResource(1)
        if not 'threads' in firstpage:
            return -1, 'No thread found in board %s' % self.board
        self.parseImages(firstpage['threads'])
        for extension in PRIORITY:
            if extension in self.images:
                selected = randint(0, len(self.images[extension]))
                name = self.images[extension][selected]
                return 0, 'http://i.4cdn.org/%s/%s%s' % (self.board, name, extension)
        return -1, 'No valid image resource found'

# Web service instance.
service = Flask(__name__)

# Valid board list
boards = getBoards()

@service.route('/', methods=['POST'])
def webhook():
    """ Webhook implementation. """
    if request.form.get('token') == ACCESS_TOKEN:
        board = request.form.get('text').replace(' ', '')
        if len(board) == 0 or not board in boards:
            board = DEFAULT_BOARD
        response = {}
        response['response_type'] = 'in_channel'
        crawler = Crawler(board)
        result, data = crawler.getRandomImage()
        if result == -1:
            message = {}
            message['color'] = '#DD2222'
            message['text'] = 'Sorry an error occurs while retriving image : %s' % data
            response['attachements'] = [message]
        else:
            response['text'] = data
        return Response(json.dumps(response), mimetype='application/json')
    return Response(), 401

if __name__ == '__main__':
    service.run(host='0.0.0.0')
