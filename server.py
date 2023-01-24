#  coding: utf-8 
import socketserver
import os

# Copyright 2013 Abram Hindle, Eddie Antonio Santos
# Copyright 2023 Jason Kim
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

# Sources:
# https://www.geeksforgeeks.org/python-check-if-a-file-or-directory-exists/
# https://uofa-cmput404.github.io/cmput404-slides/04-HTTP
# https://www.w3.org/Protocols/HTTP/1.0/spec.html
# https://tecfa.unige.ch/moo/book2/node93.html
# https://stackoverflow.com/questions/3812849/how-to-check-whether-a-directory-is-a-sub-directory-of-another-directory


class MyWebServer(socketserver.BaseRequestHandler):
    
    def handle(self):
        self.data = self.request.recv(1024).strip()
        requestString = str(self.data)
        requestString = requestString[2:requestString.find("HTTP")]
        print ("Got a request of: %s\n" % requestString)
        if (requestString == ""):
            return
        requestArray = requestString.split()
        response = ""
        if requestArray[0] == "GET":
            response = self.returnResponse(requestArray[1])
        else:
            print("Requests other than GET are not supported")
            response = "HTTP/1.1 405 Method Not Allowed\r\n"
        self.request.sendall(bytearray(response,'utf-8'))

    def serveFileRequest(self, pathToFile, fileType):
        response = """HTTP/1.1 200 OK \r\nContent-type: {contentType}\r\nConnection:keep-alive\r\n\r\n"""
        if fileType == ".html":
            response = response.format(contentType="text/html")
            file = open(pathToFile, "r")
            response += file.read()
            file.close()
            return response
        elif fileType == ".css":
            response = response.format(contentType="text/css")
            file = open(pathToFile, "r")
            response += file.read()
            file.close()
            return response
        return ""


    def returnResponse(self, requestedPath):
        print("Handling GET request for route " + requestedPath)
        # Create an array of the different levels of the requested path, last element of the path
        # is either the requested file or directory
        pathArray = requestedPath.split("/")
        # Clean the array to account for mutiple / 
        self.cleanPathArray(pathArray)
        # Check if requested path is in ./www directory
        if (not self.checkPathSecurity(requestedPath)):
            print("Attempting to access path outside of www directory, forbidden")
            return "HTTP/1.1 404 Not Found \r\n"
        # Check if requested path exists, return 404 if not
        if (not os.path.exists("./www" + requestedPath)):
            print("Attempting to access a non-existent path")
            return "HTTP/1.1 404 Not Found \r\n"
        else:
            # Check if requested path is a file, and return that file
            if (os.path.isfile("./www" + requestedPath)):
                print("Requesting file ./www" + requestedPath)
                # Check extension of file to detrimine mime types
                fileExt = ""
                if pathArray[-1].find(".html") != -1:
                    fileExt = ".html"
                elif pathArray[-1].find(".css") != -1:
                    fileExt = ".css"
                return self.serveFileRequest("./www" + requestedPath, fileExt)
            # Path is a directory
            else:
                # Check if path ends with /, redirect if not
                if (requestedPath[-1] == "/"):
                    print("Requested ./www" + requestedPath +"index.html")
                    return self.serveFileRequest("./www" + requestedPath + "index.html", ".html")
                else:
                    print("Redirect to path " + requestedPath +"/")   
                    return "HTTP/1.1 301 Moved Permanently\r\nLocation:http://127.0.0.1:8080" + requestedPath + "/"   
                

    def cleanPathArray(self, pathArray):
        counter = 0
        for i in range(0, len(pathArray)-1):
            if pathArray[i] == "":
                counter += 1
        while counter > 0:
            pathArray.remove("")
            counter -= 1

    # Based of off:
    # https://stackoverflow.com/questions/3812849/how-to-check-whether-a-directory-is-a-sub-directory-of-another-directory
    def checkPathSecurity(self, requestedPath):
        absPathofWWW = os.path.abspath("./www")
        print("www's abs path is " + absPathofWWW)
        absPathOfRequest = os.path.abspath( "./www" + requestedPath)
        print("Requested abs path is " + absPathOfRequest)
        return os.path.commonpath([absPathofWWW, absPathOfRequest]) == absPathofWWW



        

if __name__ == "__main__":
    HOST, PORT = "localhost", 8080

    socketserver.TCPServer.allow_reuse_address = True
    # Create the server, binding to localhost on port 8080
    server = socketserver.TCPServer((HOST, PORT), MyWebServer)

    # Activate the server; this will keep running until you
    # interrupt the program with Ctrl-C
    server.serve_forever()
