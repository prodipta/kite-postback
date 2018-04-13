# -*- coding: utf-8 -*-
"""
Created on Tue Mar 27 20:52:14 2018

@author: Prodipta
"""
import pandas as pd
from BaseHTTPServer import HTTPServer, BaseHTTPRequestHandler
import json
import logging
import configparser
from order import OrderWriter
from checksum import verify_checksum

logger = logging.getLogger(__name__)


config = configparser.ConfigParser()
config.read('config.ini')

PORT = int(config['DEFAULT']['PORT']) # 'port on which this runs'
SERVER_ADDR = config['DEFAULT']['SERVER_ADDR'] # 'server address'
DBPATH = config['DEFAULT']['DBPATH'] # 'db pathname'
SECRET_KEY = config['DEFAULT']['SECRET_KEY'] # 'API SECRET KEY'
TIMEOUT = int(config['DEFAULT']['TIMEOUT']) # 'socket read timeout'

writer = OrderWriter(DBPATH)

class PostbackHandler(BaseHTTPRequestHandler):
    def _send_response(self, code, msg):
        if code != 200:
            self.send_error(code, msg)
        else:
            self.send_response(code, msg)
            
    def update_orderbook(self, post_data):
        order_id = post_data['order_id']
        timestamp = post_data['order_timestamp']
        checksum = post_data['checksum']
        if verify_checksum(order_id,timestamp,checksum,SECRET_KEY):
            logger.info('user id is'+post_data['user_id']+'...\n')
            writer.upsert(post_data)

    def do_POST(self):
        msg = "Success"
        self._send_response(200, msg)
        content_length = int(self.headers['Content-Length'])
        self.rfile._sock.settimeout(TIMEOUT)
        post_data = self.rfile.read(content_length)
        try:
            post_data = json.loads(post_data)
            if isinstance(post_data,list):
                timestamps = [pd.Timestamp(d['order_timestamp']) for d in post_data]
                sorted_index = sorted(range(len(timestamps)), key=lambda k: timestamps[k])
                for i in range(len(timestamps)):
                    self.update_orderbook(post_data[sorted_index[i]])
            elif isinstance(post_data,dict):
                self.update_orderbook(post_data)
            else:
                with open("postback.txt","a") as outfile:
                    outfile.write("unknown data type {}".format(post_data))
                raise TypeError("expect a dict")
            
        except:
            pass
        

class PostBackServer():
    def __init__(self,server_class=HTTPServer, port=PORT):
        self.server_class = server_class
        self.port = port
        self.handler_class = PostbackHandler
    
    def run(self):
        server_address = (SERVER_ADDR, self.port)
        httpd = self.server_class(server_address, self.handler_class)
        logger.info('Starting postback server...\n')
        try:
            httpd.serve_forever()
        except KeyboardInterrupt:
                pass
        httpd.server_close()
        logger.info('Stopping postback server...\n')

if __name__ == '__main__':
    server = PostBackServer()
    server.run()
