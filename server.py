import select
from socket import socket, AF_INET as ipv4, SOCK_STREAM as connected
from parser import parse_http
from datetime import datetime
from server_response import generate_response
RESPONSE = '''HTTP/1.1 200 OK
Content-Type: text/html; charset=UTF-8
Content-Length: 167

<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <title>Success</title>
</head>
<body>
  <h1>200 OK</h1>
  <p>Successful Request.</p>
</body>
</html>
'''

class http_server:
    def __init__(self, port = 5000, backlog = 5):
        self.server = socket(ipv4, connected)
        self.server.bind(('', port))
        self.server.listen(backlog)

    def run(self):
        sock_name = self.server.getsockname()
        print(f"http-server running on http://{sock_name[0]}:{sock_name[1]}")
        inputs = [self.server]
        running = True
        while running:
            try:
                input_handler, _, _ = select.select(inputs, [], [])
            except Exception as e:
                print(e)
                break
            if input_handler[0] == self.server:
                client, client_addr = self.server.accept()
                request = parse_http(client.recv(4096).decode())
                client.send(generate_response(request))
                client.close()
                print(f"{client_addr[0]} - - [{datetime.now()}] \"{request.request_type} {request.request_target} {request.http_version}\"200")

if __name__ == "__main__":
    s = http_server()
    s.run()
