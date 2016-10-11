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

    print('Server listening on port: 8080')
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

    request = read_http_headers(request_socket)
    type = request[0].split()[0]
    if (type == 'GET'):
        file_path = request[0].split()[1]
        print('GET REQUEST')
        print(get_file_size(file_path))
        print(get_mime_type(file_path))
    request_socket.close()
    return  # Replace this line with your code

# Reads the headers of the response.
#       data_socket -- The socket for which the response containing the header information is contained.
#
# Returns a list of all the Headers
#@author: appelbaumgl
def read_http_headers(data_socket):
    headers = []
    header = ""
    trigger = 0
    while header != b'\r\n':
        header = read_http_line(data_socket)
        headers.append(header.decode("utf-8", "replace"))

    print(headers) #DEBUG CODE
    return headers

# Reads a single line of a http header
#       data_socket -- The socket for which the responce containing the header information is contained.
#
# Returns the line read that contains a http header.
#@author sondermanjj
def read_http_line(data_socket):
    b = b''
    line = b''
    while b != b'\n':
        b = next_byte(data_socket)
        line += b
    return line

# Used to skip over bytes by reading them and doing nothing with them.
#       number -- The number of bytes to skip.
#       data_socket -- Socket where data is read from.
#@author: appelbaumgl
def skip_byte(number, data_socket):
    for x in range(0, number):
        next_byte(data_socket)
    return

# Read the next byte from the socket data_socket.
#       data_socket -- Socket where data is read from.
#
# Returns the next byte, as a bytes object with a single byte in it.
#@author: appelbaumgl
def next_byte(data_socket):
    return data_socket.recv(1)

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