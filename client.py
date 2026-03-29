import socket
import ssl
import json

HOST = "localhost"
PORT = 8443

context = ssl.SSLContext(ssl.PROTOCOL_TLS_CLIENT)
context.verify_mode = ssl.CERT_REQUIRED
context.check_hostname = True
context.load_verify_locations("server.crt")

with socket.create_connection((HOST, PORT)) as sock:
    with context.wrap_socket(sock, server_hostname=HOST) as ssock:
        request = {"command": "GET_TIME"}
        ssock.sendall(json.dumps(request).encode())
        
        response = ssock.recv(4096)
        print("Server response:", response.decode())