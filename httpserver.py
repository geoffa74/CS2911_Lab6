#: ## Lab 6 ##
#:
#: CS-2911 Network Protocols
#: Dr. Yoder
#: Fall quarter 2016-2017
#:
#: | Team members (usernames)   |
#: |:---------------------------|
#: | Geoff Appelbaum (appelbaumgl)     |
#: | Jon Sonderman (sondermanjj) |
#:

import socket
import re
import threading
import os
import mimetypes
import datetime


def main():
    http_server_setup(8080)


# Start the HTTP server
#   Open the listening socket
#   Accept connections and spawn processes to handle requests
#   port -- listening port number
def http_server_setup(port):
    num_connections = 10
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    listen_address = ('', port)
    server_socket.bind(listen_address)
    server_socket.listen(num_connections)
    try:
        while True:
            request_socket, request_address = server_socket.accept()
            print('connection from {0} {1}'.format(request_address[0], request_address[1]))
            # Create a new thread, and set up the handle_request method and its argument (in a tuple)
            request_handler = threading.Thread(target=handle_request, args=(request_socket,))
            # Start the request handler thread.
            request_handler.start()
            # Just for information, display the running threads (including this main one)
            print('threads: ', threading.enumerate())
    # Set up so a Ctrl-C should terminate the server; this may have some problems on Windows
    except KeyboardInterrupt:
        print("HTTP server exiting . . .")
        print('threads: ', threading.enumerate())
        server_socket.close()


# Handle a single HTTP request, running on a newly started thread.
#   request_socket -- socket representing TCP connection from the HTTP client_socket
#   Returns: nothing
#       Closes request socket after sending response.
#       Should include a response header indicating NO persistent connection
def handle_request(request_socket):
    request_bytes = b''
    exit_bytes = b''
    next_byte = request_socket.recv(1)
    while(exit_bytes != b'\r\n'):
        if next_byte == b'\r' or next_byte == b'\n':
            exit_bytes += next_byte
        else:
            request_bytes += next_byte
    (method, parameter, version) = parseRequestLine()

    #stuff

    sendResponce(request_socket)


def parseRequestLine():

    pass

def sendResponce(request_socket):

    pass

# ** Do not modify code below this line.  You should add additional helper methods above this line.

# Utility functions
# You may use these functions to simplify your code.

# Try to guess the MIME type of a file (resource), given its path (primarily its file extension)
#   file_path -- string containing path to (resource) file, such as './abc.html'
#   Returns:
#       If successful in guessing the MIME type, a string representing the content type, such as 'text/html'
#       Otherwise, None
def get_mime_type(file_path):
    mime_type_and_encoding = mimetypes.guess_type(file_path)
    mime_type = mime_type_and_encoding[0]
    return mime_type


# Try to get the size of a file (resource) as number of bytes, given its path
#   file_path -- string containing path to (resource) file, such as './abc.html'
#   Returns:
#       If file_path designates a normal file, an integer value representing the the file size in bytes
#       Otherwise (no such file, or path is not a file), None
def get_file_size(file_path):
    # Initially, assume file does not exist
    file_size = None
    if os.path.isfile(file_path):
        file_size = os.stat(file_path).st_size
    return file_size


main()

# Replace this line with your comments on the lab