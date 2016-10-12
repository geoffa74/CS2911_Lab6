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
    while header != b'':
        parse_header(header.decode(), dict)
        header = read_header(request_socket)
    if os.path.isfile(file) and version == "HTTP/1.1" and method == "GET":
        reply(request_socket, version, file)
    elif not os.path.isfile(file):
        request_socket.send(version.encode() + b' 404 Not Found\r\n\r\n')
        print("File not found")
    elif version != "HTTP/1.1":
        request_socket.send(version.encode() + b' 505 Version Not Supported\r\n\r\n')
        print("Wrong-Version")
    else:
        request_socket.send(version.encode() + b' 400 Bad-Request\r\n\r\n')
        print("Bad Request")

    request_socket.close()


# Reply to the client, sending the header information
#   request_socket: The socket we're getting data from, and that we'll respond to
#   version: The version of the code we're using
#   file: File name
#   Returns: nothing
def reply(request_socket, version, file):
    send_response_head(request_socket, version, file)
    output_file = open(file, 'rb')
    i = 0
    size = get_file_size(file)
    while i < size:
        request_socket.send(output_file.read(1))
        i += 1
    output_file.close()

# Reply to the client, sending the header information
#   request_socket: The socket we're getting data from, and that we'll respond to
#   version: The version of the code we're using
#   file: File name
#   Returns: nothing
def send_response_head(request_socket, version, file):
    request_socket.send(version.encode() + b' 200 OK\r\n')
    response = create_response(file)

    for header in response:
        head = str.encode(header + ": " + response[header])
        request_socket.send(head)
    request_socket.send(b'\r\n')
    return

# creates the response headers, getting them ready to be sent
#   file: File name
#   Returns: the dictionary response of headers
def create_response(file):
    timestamp = datetime.datetime.utcnow()
    timestring = timestamp.strftime('%a, %d %b %Y %H:%M:%S GMT')

    response = {}
    response["Date"] = timestring + "\r\n"
    response["Connection"] = 'close\r\n'
    response["Content-Type"] = get_mime_type(file) + '\r\n'
    response["Content-Length"] = str(get_file_size(file)) + '\r\n'

    return response


# Parse a single header, adding it to the dictionary
#   header - Header to be added to the dictionary
#   dict - dictionary reference that we are changing
#   Returns: nothing
def parse_header(header, dict):
    print(header)
    parts = header.split(':')
    dict[parts[0]] = parts[1].lstrip()


# Reads a single header
#   request_socket: socket that we are getting the information from
#   Returns: The header in byte form
def read_header(request_socket):
    header_bytes = b''
    next_byte = b''
    exit_bytes = b''
    while exit_bytes != b'\r\n':
        next_byte = request_socket.recv(1)
        if next_byte == b'\r' or next_byte == b'\n':
            exit_bytes += next_byte
        else:
            header_bytes += next_byte
    return header_bytes


# Reads the first line of the request
#   request_socket: socket that we are getting the information from
#   Returns: The request line in all its parts
def read_request(request_socket):
    request_bytes = b''
    exit_bytes = b''
    while exit_bytes != b'\r\n':
        next_byte = request_socket.recv(1)
        if next_byte == b'\r' or next_byte == b'\n':
            exit_bytes += next_byte
        else:
            request_bytes += next_byte
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
