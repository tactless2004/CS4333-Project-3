'''
server.py
CS4333 Project 3
Leyton McKinney 
'''
import select
import sys
from socket import socket, AF_INET as ipv4, SOCK_STREAM as connected
from requests import parse_request, generate_response

class HTTPServer:
    '''
    Simple HTTP Server Implementation. Handles multiple users.
    Implements GET and HEAD requests.
    '''
    def __init__(self, port = 5000, backlog = 5):
        self.server = socket(ipv4, connected)
        self.server.bind(('', port))
        self.server.listen(backlog)

    def run(self):
        '''Start the HTTP server.'''
        sock_name = self.server.getsockname()
        print(f"http-server running on http://{sock_name[0]}:{sock_name[1]}")
        inputs = [self.server]
        running = True
        while running:
            input_handler, _, _ = select.select(inputs, [], [])
            if input_handler[0] == self.server:
                client, _ = self.server.accept()
                request = parse_request(client.recv(4096).decode())
                client.send(generate_response(request))
                client.close()
    def __str__(self):
        return f"{self.server.getsockname()}"

if __name__ == "__main__":
    s = HTTPServer()
    s.run()
