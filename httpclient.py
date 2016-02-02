#!/usr/bin/env python
# coding: utf-8
# Copyright 2013 Abram Hindle
# 
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
# 
#     http://www.apache.org/licenses/LICENSE-2.0
# 
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

# Do not use urllib's HTTP GET and POST mechanisms.
# Write your own HTTP GET and POST
# The point is to understand what you have to send and get experience with it

import sys
import socket
import re
# you may use urllib to encode data appropriately
import urllib, urllib2, urlparse
import csv

def help():
    print "httpclient.py [GET/POST] [URL]\n"

class HTTPResponse(object):
    def __init__(self, code=200, body=""):
        self.code = code
        self.body = body


class HTTPClient(object):
    # Headers in a dictionary with callables
    httpheaders = {}
    # Response codes in a dictionary with handlers
    httpresponsecodes = {}

    def __init__(self):
        print("")
    #def get_host_port(self,url):


    def csvtodict(self, source, d={}):
        ''' Helper function to generate dictionary from .csv '''
        try:
            read = csv.reader(open(source))
            for line in read:
                k = line[0]
                if k not in d:
                    try:
                        # don't know if anything to put
                        d[k]=line[1:]
                    except:
                        d[k]=None
            return d
        except IOError:
            pass


    def connect(self, host, port):
        # use sockets!
        p = (port if port is not None else 80)
        return socket.create_connection((host,p))


    def get_code(self, data):
        ''' get HTTP tokens from data string '''
        # for bug tests
        #last_msg = data.split()[2]
        # assuming looks like "HTTP/1.x [code] [message]
        try:
            return int(data.split()[1])
        except:
            return "500"


    def get_headers(self,data):
        ''' after success code, get HTTP response header '''
        return data.split("\r\n\r\n")[0]


    def get_body(self, data):
        try:
            return data.split("\r\n\r\n")[1]
        except:
            return ""


    def format_header(self, cmd="GET ", path="/", hostname="none", accept="*/*"):
        request = (cmd + path + " HTTP/1.1\r\n"+
                "Host: "+ hostname + "\r\n"+
                "Accept: "+ accept + "\r\n"+
                "User-Agent: httpclient.py\r\n"+
                "Connection: close\r\n\r\n")
        return request


    def recvall(self, sock):
        buffer = bytearray()
        done = False
        while not done:
            part = sock.recv(1024)
            if (part):
                buffer.extend(part)
            else:
                done = not part
        return str(buffer)


    def GET(self, url, args=None):
        # TODO substitute for inhouse parser
        parse = urlparse.urlparse(url)
        request = self.format_header("GET ",url)
        print request
        
        response = ""
        try:
            socket = self.connect(h=parse.hostname,p=parse.port)
            socket.sendall(request)
            response = self.recvall(socket)
        except:
            print( "Request failed" )
            #assert False

        return HTTPResponse(self.get_code(response), self.get_body(response))


    def POST(self, url, args=None):
        # TODO substitute for inhouse parser
        parse = urlparse.urlparse(url)
        request = self.format_header("POST ",url)
        print request
        
        response = ""
        try:
            socket = self.connect(host,port)
            socket.sendall(request)
            response = self.recvall(socket)
        except:
            print( "Request failed" )
            #assert False

        return HTTPResponse(self.get_code(response), self.get_body(response))


    def command(self, url, command="GET", args=None):
        if (command == "POST"):
            return self.POST( url, args )
        else:
            return self.GET( url, args )


if __name__ == "__main__":
    # ==== DEBUG ====
    global DEBUG
    DEBUG = False
    # ^ NEVER DO THIS

    client = HTTPClient()
    command = "GET"
    if (len(sys.argv) <= 1):
        help()
        sys.exit(1)
    elif (len(sys.argv) == 3):
        print client.command( sys.argv[2], sys.argv[1] )
    elif (sys.argv[1]=="DEBUG"):
        # DEBUG MODE
        DEBUG = True
        print ''
        client.GET("http://www.google.ca")
        assert True
    else:
        print client.command( sys.argv[1] )   
