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
    dict = {}
    (method, file, version) = read_request(request_socket)
    print(file)
    if file == '/':
        file = 'index.html'
    else:
        file = file[1:]
    header = read_header(request_socket)
    while(header != b'\r\n'):
        parse_header(header.decode(), dict)
        header = read_header(request_socket)
    if(os.path.isfile(file)):
        request_socket.send(version.encode() + b' 200 OK\r\n')
        timestamp = datetime.datetime.utcnow()
        timestring = timestamp.strftime('%a, %d %b %Y %H:%M:%S GMT')
        request_socket.send(b'Date: ' + timestring.encode() + b'\r\n')
        request_socket.send(b'Connection: close\r\n')
        request_socket.send(b"Content-Type: " + get_mime_type(file).encode() + b"\r\n")
        request_socket.send(b"Content-Length: " + str(get_file_size(file)).encode() + b"\r\n")
        request_socket.send(b'\r\n')

        output_file = open(file, 'rb')
        i = 0
        size = get_file_size(file)
        while i < size:
            next_byte = output_file.read(1)
            request_socket.send(next_byte)
            i += 1
        output_file.close()
    else:
        request_socket.send(version.encode() + b' 404 Not Found\r\n')
    request_socket.close()

def parse_header(header, dict):
    header = header[:len(header)-2]
    print(header)
    parts = header.split(':')
    dict[parts[0]] = parts[1].lstrip()

def read_header(request_socket):
    header_bytes = b''
    next_byte = b''
    while next_byte != b'\n':
        next_byte = request_socket.recv(1)
        header_bytes += next_byte
    return header_bytes

def read_request(request_socket):
    request_bytes = b''
    next_byte = request_socket.recv(1)
    while (next_byte != b'\n'):
        if next_byte != b'\r' or next_byte != b'\n':
            request_bytes += next_byte
        next_byte = request_socket.recv(1)
    request = request_bytes.decode()
    parts = request.split()
    print(request)
    return (parts[0], parts[1], parts[2])




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