import socket
import threading
import re

def extract_host(request_data):
    # Extract host from HTTP request headers
    host = re.search(b'Host: (.+)\r\n', request_data)
    if host:
        return host.group(1).decode().strip()
    else:
        return None

def handle_client(client_socket):
    # Receive data from client
    request_data = client_socket.recv(4096)
    print("[*] Received request from client:")
    print(request_data)

    # Extract host from request
    host = extract_host(request_data)
    if not host:
        print("Failed to extract host from request.")
        client_socket.close()
        return

    try:
        # Write request to file
        with open("requests.txt", "a") as f:
            f.write("[*] Request from client to {}\n".format(host))
            f.write(request_data.decode() + "\n\n")

        # Forward the request to the remote server
        remote_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        remote_socket.connect((host, 80))
        remote_socket.send(request_data)

        # Receive response from the remote server
        remote_response = remote_socket.recv(4096)
        print("[*] Received response from server:")
        print(remote_response)

        # Write response to file
        with open("responses.txt", "a") as f:
            f.write("[*] Response from {}\n".format(host))
            f.write(remote_response.decode() + "\n\n")

        # Send the response back to the client
        client_socket.send(remote_response)
    except Exception as e:
        print("Error forwarding request:", e)

    # Close the sockets
    remote_socket.close()
    client_socket.close()

def start_proxy_server():
    proxy_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    proxy_socket.bind(("127.0.0.1", 4444))
    proxy_socket.listen(5)
    print("[*] Proxy server listening on port 4444")

    while True:
        client_socket, addr = proxy_socket.accept()
        print("[*] Accepted connection from %s:%d" % (addr[0], addr[1]))
        client_handler = threading.Thread(target=handle_client, args=(client_socket,))
        client_handler.start()

start_proxy_server()
