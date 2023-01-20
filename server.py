#  coding: utf-8 
import socketserver

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
        requestString = str(self.data)
        requestString = requestString[2:requestString.find("HTTP")]
        print ("Got a request of: %s\n" % requestString)
        requestArray = requestString.split()
        if requestArray[0] == "GET":
            self.sendGetResponse(requestArray[1])
        else:
            print("Requests other than GET are not supported")
        self.request.sendall(bytearray("OK",'utf-8'))

    def sendGetResponse(self, requestedPath):
        print("Handling GET request for route " + requestedPath)
        pathArray = requestedPath.split("/")
        #requested index
        if (pathArray[-1] == ""):
            print("Requested Directory, returning ./www" + requestedPath +"index.html")
        elif (not pathArray[-1].find(".")):
            print("Redirect to path " + requestedPath +"/")      
        #requested file
        else:
            print("Requesting file ./www" + requestedPath)




        

if __name__ == "__main__":
    HOST, PORT = "localhost", 8080

    socketserver.TCPServer.allow_reuse_address = True
    # Create the server, binding to localhost on port 8080
    server = socketserver.TCPServer((HOST, PORT), MyWebServer)

    # Activate the server; this will keep running until you
    # interrupt the program with Ctrl-C
    server.serve_forever()
