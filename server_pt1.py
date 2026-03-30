import socket
import ssl
import json
import datetime
import logging

logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(message)s")

HOST = "localhost"
PORT = 8443

# Bind TCP Socket
with socket.socket(socket.AF_INET, socket.SOCK_STREAM, 0) as sock:
    sock.bind((HOST, PORT))
    sock.listen(5)
    print(f"Secure server listening on {PORT}")
    
    context = ssl.SSLContext(ssl.PROTOCOL_TLS_SERVER)
    context.load_cert_chain(certfile="server.crt", keyfile="server.key")
    wrapped_socket = context.wrap_socket(sock, server_side=True)

    conn, addr = wrapped_socket.accept()
    print("Connection from", addr)
    
    tls_version = conn.version()
    cipher_info = conn.cipher()
    
    logging.info("Negotiated TLS version: %s", tls_version)
    logging.info("Negotiated cipher suite: %s", cipher_info[0])

    data = conn.recv(4096)
    request = json.loads(data.decode())

    if request.get("command") == "GET_TIME":
        response = {"time": datetime.datetime.now(
            datetime.timezone.utc).isoformat()}
    else:
        response = {"error": "Unknown command"}

    conn.sendall(json.dumps(response).encode())