#  coding: utf-8 
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

        NOTFOUND = b"""HTTP/1.1 404 Not Found\r\n"""
        NOTGET = b"""HTTP/1.1 405 Not Allowed\r\n"""
        REDIRCT = b"""HTTP/1.1 301 Moved Permanently\r\n"""

        #get path
        def get_path(str):
            
            tempStr = str.split(" ")[1]
            path = tempStr.split(" HTTP")[0]
            if path == "/www/":
                return path
            return "./www" + path
        
        
        #send html content
        def html_part(path):
            html_content = b"""HTTP/1.1 200 OK\r\nContent-Type: text/html\r\n\r\n"""
            f= open(f"{path}",'rb')
            html_content = html_content + f.read()
            f.close()
            self.request.sendall(html_content)
            

        #send css content
        def css_part(path):
            css_content = b"""HTTP/1.1 200 OK\r\nContent-Type: text/css\r\n\r\n"""
            f = open(f"{path}",'rb')
            css_content = css_content + f.read()
            f.close()
            self.request.sendall(css_content)

    #https://www.geeksforgeeks.org/python-os-path-isdir-method/ reference
        path = get_path(str)
        def isDir(path1):
            if os.path.isdir(path1) and not path.endswith('/'):
                
                self.request.sendall(REDIRCT)
                return True
            else:
                return False
        isDir(path)
        def deal_etc(path):
            substring = '../'
            index = path.find(substring)
            if (index != -1):
                path = path[:index]
                self.request.sendall(NOTFOUND)
            return path
        
        path = deal_etc(path)

        
        
        def router(path1):

            if path1.endswith('/'):
                return path1 + "index.html"
            
            return path1
    #reference  https://www.geeksforgeeks.org/python-os-path-exists-method/#:~:text=os.-,path.,open%20file%20descriptor%20or%20not 
        path = router(path)
        def isValid(path1):
            exist = os.path.exists(f"{path1}")
            return exist
            
        #go to the final router
        def endswithwhich(path):

            if path.endswith('.css'):
                css_part(path)
           
            if path.endswith('.html'):
                html_part(path)


        #Test if it's get method
        def is_get(str):
            method = str[0:3]
            
            if method == "GET":
                return True
            else:
                return False

        #Test if it is 404
        if (not isValid(path)):
            self.request.sendall(NOTFOUND)
        #Test if it is 405
        elif (not is_get(str)):
            self.request.sendall(NOTGET)
            
        else:
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
    