#  coding: utf-8 
from cgi import print_form
from operator import index
import socketserver
import os

# Copyright 2013 Abram Hindle, Eddie Antonio Santos
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
#
#
# Furthermore it is derived from the Python documentation examples thus
# some of the code is Copyright © 2001-2013 Python Software
# Foundation; All Rights Reserved
#
# http://docs.python.org/2/library/socketserver.html
#
# run: python freetests.py

# try: curl -v -X GET http://127.0.0.1:8080/


class MyWebServer(socketserver.BaseRequestHandler):
    
    def handle(self):
        

        self.data = self.request.recv(1024).strip()
        str = self.data.decode("utf-8")
        

        def is_get(str):
            method = str[0:3]
            if method != "GET":
                return 404
        
    
        def get_path(str):
            tempStr = str.split("GET ")[1]
            path = tempStr.split(" HTTP")[0]
            if path == "/www/":
                return path
            return "/www" + path
        
        #open html package
        def html_part(path):
            html_content = b"""HTTP/1.1 200 OK\r\nContent-Type: text/html\r\n\r\n"""
            f= open(f".{path}",'rb')
            html_content = html_content + f.read()
            f.close()
            self.request.sendall(html_content)
            
        
        

        #css part
        def css_part(path):
            css_content = b"""HTTP/1.1 200 OK\r\nContent-Type: text/css\r\n\r\n"""
            f = open(f".{path}",'rb')
            css_content = css_content + f.read()
            f.close()
            self.request.sendall(css_content)


        path = get_path(str)
        
        def router(path):
            # if path == "/":
            #     path = path + "www/index.html"
            # if path == "/www":
            print(path)
            if path == "/www/":
                return path + "index.html"
            
            return path

        path = router(path)
        
        def endswithwhich(path):

            if path.endswith('.css'):
                css_part(path)
           
            if path.endswith('.html'):
                html_part(path)
        


        endswithwhich(path)


        # print ("Got a request of: %s\n" % self.data)
        # print(f"this is afasdfsafdsafsda{self.client_address}")
        # print(f"this is afasdfsafdsafsda{self.request}")
        # print(f"this is afasdfsafdsafsda{self.server}")
        #response_html = "HTTP/1.1 200 OK\r\n"
    
        
        

if __name__ == "__main__":
    HOST, PORT = "localhost", 8080

    socketserver.TCPServer.allow_reuse_address = True
    # Create the server, binding to localhost on port 8080
    server = socketserver.TCPServer((HOST, PORT), MyWebServer)
    
    # Activate the server; this will keep running until you
    # interrupt the program with Ctrl-C
    server.serve_forever()
