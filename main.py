from http.server import HTTPServer, BaseHTTPRequestHandler
import urllib.parse
import mimetypes
import pathlib
import json
import datetime
import socket
import os
from threading import Thread

# Constants for server configuration
HOST = ''
SERVER_PORT = 3000
CLIENT_PORT = 5000


def check_storage():
    """
    Function to check and create a storage directory and a data file if they
    don't exist.
    """
    storage_path = 'storage'
    data_file_path = os.path.join(storage_path, 'data.json')

    if not os.path.exists(storage_path):
        os.makedirs(storage_path)
    if not os.path.isfile(data_file_path):
        with open(data_file_path, 'w') as file:
            json.dump({}, file)


class HttpHandler(BaseHTTPRequestHandler):
    """
    Handles HTTP requests by serving static files and managing data submission.
    """
    def do_GET(self):
        """
        Handle the HTTP GET request.
        Parses the URL and determines the appropriate action based on the path.
        """
        pr_url = urllib.parse.urlparse(self.path)
        if pr_url.path == '/':
            self.send_html_file('index.html')
        elif pr_url.path == '/message':
            self.send_html_file('message.html')
        else:
            path = pathlib.Path(pr_url.path[1:])
            if path.exists() and path.is_file():
                self.send_static(path)
            else:
                self.send_html_file('error.html', 404)

    def do_POST(self):
        """
        Handles the POST request by reading the data, parsing it, sending it
        to a socket server, and updating the local data.json file.
        """
        data = self.rfile.read(int(self.headers['Content-Length']))
        data_parse = urllib.parse.unquote_plus(data.decode())
        time = datetime.datetime.now()
        data_dict = {
            str(time): {
                key: value
                for key, value in (
                    el.split('=') for el in data_parse.split('&')
                )
            }
        }

        self.send_data_to_socket_server(json.dumps(data_dict))

        file_path = 'storage/data.json'
        if not os.path.isfile(file_path):
            existing_data = {}
        else:
            with open(file_path, 'r') as json_file:
                try:
                    existing_data = json.load(json_file)
                except json.JSONDecodeError:
                    existing_data = {}

        existing_data.update(data_dict)
        with open(file_path, 'w') as json_file:
            json.dump(existing_data, json_file, indent=4)

        self.send_response(302)
        self.send_header('Location', '/message')
        self.end_headers()

    def send_data_to_socket_server(self, data):
        """
        Sends data to a socket server using UDP protocol.

        Args:
            data (str): The data to be sent.
        """
        with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as s:
            s.sendto(data.encode(), (HOST, CLIENT_PORT))

    def send_html_file(self, filename, status=200):
        """
        Sends an HTML file with the specified filename and status code.

        Args:
            filename (str): The name of the HTML file to be sent.
            status (int, optional): The HTTP status code to be sent.
                                    Defaults to 200.
        """
        self.send_response(status)
        self.send_header('Content-type', 'text/html')
        self.end_headers()
        with open(filename, 'rb') as file:
            self.wfile.write(file.read())

    def send_static(self, path):
        """
        Sends a static file (e.g., CSS, images) to the client.

        Args:
            path (str): The path of the static file to be sent.
        """
        mime_type, _ = mimetypes.guess_type(path)
        self.send_response(200)
        self.send_header('Content-type', mime_type or
                         'application/octet-stream')
        self.end_headers()
        with open(path, 'rb') as file:
            self.wfile.write(file.read())


def run_web_server():
    """
    Runs the HTTP server.
    """
    check_storage()
    server_address = (HOST, SERVER_PORT)
    httpd = HTTPServer(server_address, HttpHandler)
    print(f'Running web server on port {SERVER_PORT}...')
    httpd.serve_forever()


def run_socket_server():
    """
    Runs the socket server.
    """
    check_storage()
    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as server:
        server.bind((HOST, CLIENT_PORT))
        print(f'Socket server running on port {CLIENT_PORT}...')
        while True:
            data, address = server.recvfrom(1024)
            print(f'Received data: {data.decode()} from {address}')


if __name__ == '__main__':
    """
    Starting both web and socket servers in separate threads
    """
    web_server_thread = Thread(target=run_web_server, daemon=True)
    socket_server_thread = Thread(target=run_socket_server, daemon=True)

    web_server_thread.start()
    socket_server_thread.start()

    try:
        while True:
            continue
    except KeyboardInterrupt:
        print('Stopping servers...')
