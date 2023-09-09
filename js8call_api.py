import json
import logging
import select
import time
import os

from socket import socket, AF_INET, SOCK_STREAM

from fortune_settings import *

class Js8CallApi:
    connected = False
    my_station = ''
    my_freq = ''
    my_grid = ''

    def __init__(self):
        self.sock = socket(AF_INET, SOCK_STREAM)

    def connect(self):
        logging.info( 'info: Connecting to JS8Call at ' + ':'.join(map(str, server)))
        try:
            api = self.sock.connect(server)
            self.connected = True
            logging.info( 'info: Connected to JS8Call')
            return api

        except ConnectionRefusedError:
            logging.warning( 'err: Connection to JS8Call has been refused.')
            logging.warning( 'info: Check that:')
            logging.warning( 'info: * JS8Call is running')
            logging.warning( 'info: * JS8Call settings check boxes Enable TCP Server API and Accept TCP Requests are checked')
            logging.warning( 'info: * The API server port number in JS8Call matches the setting in this script'
                      ' - default is 2442')
            logging.warning( 'info: * There are no firewall rules preventing the connection')
            exit(1)

    def set_my_grid(self, grid):
        self.my_grid = grid
        return

    def set_my_station(self, station_id: str):
        self.my_station = station_id

    def set_my_frequency(self, frequency: str):
        self.my_frequency = frequency
        logging.info("Station Frequency is: " + str(frequency))

    def listen(self):
        # the following block of code provides a socket recv with a 10 second timeout
        # we need this so that we call the @MB announcement code periodically
        self.sock.setblocking(False)
        ready = select.select([self.sock], [], [], 10)
        if ready[0]:
            content = self.sock.recv(65500)
            logging.debug('recv: ' + str(content))
        else:
            content = 'Check if announcement needed'

        if not content:
            message = {}
            self.connected = False
        else:
            try:
                message = json.loads(content)

            except ValueError:
                message = {}

        return message

    @staticmethod
    def to_message(typ, value='', params=None):
        if params is None:
            params = {}
        return json.dumps({'type': typ, 'value': value, 'params': params})

    def send(self, *args, **kwargs):
        params = kwargs.get('params', {})
        if '_ID' not in params:
            params['_ID'] = '{}'.format(int(time.time() * 1000))
            kwargs['params'] = params
        message = self.to_message(*args, **kwargs)

        if args[1]:  # if no args must be an api call that doesn't send a message
            # under normal circumstances, we don't want to fill the log with post content
            # only log the message content if running at log level 2 or above
            if current_log_level >= 2:
                log_line = args[1]
            else:
                temp = args[1].split('\n', 1)
                log_line = temp[0]
            logging.info('omsg: ' + self.my_station + ': ' + log_line)  # console trace of messages sent

        message = message.replace('\n\n', '\n \n')  # this seems to help with the JS8Call message window format
        logging.info('send: ' + message)

        if args[1] and debug:
            logger.info('info: MB message not sent as we are in debug mode')
            # this avoids hamlib errors in JS8Call if the radio isn't connected
        else:
            self.sock.send((message + '\n').encode())   # newline suffix is required

    def close(self):
        self.sock.close()

