import socket
import threading
from utils import parse_request 

class HTTPProxy:
    def __init__(self, host, port):
        self.host = host
        self.port = port
        self.proxy_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.proxy_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        
        # Bind the socket to the given host and port
        self.proxy_socket.bind((self.host, self.port))
    
    def handle_client(self, client_socket):
        # Receive data from the client
        request_data = client_socket.recv(4096)
        req = parse_request(request_data)
        print("[Received Request]:\n", req)
        
        # Extract the destination host and port from the request
        try:
            host, port = self.extract_host_port(request_data)
        except ValueError:
            client_socket.close()
            return
        
        # Connect to the destination server
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server_socket:
            server_socket.connect((host, port))
            server_socket.sendall(request_data)
            
            while True:
                # Receive data from the server
                server_response = server_socket.recv(4096)
                if not server_response:
                    break
                
                # Send the server response back to the client
                client_socket.sendall(server_response)
                # print("[Received Response]:\n", server_response.decode(encoding="utf8", errors='ignore'))
        
        # Close the connection
        client_socket.close()
    
    def extract_host_port(self, request_data):
        lines = request_data.decode().split('\r\n')
        first_line_tokens = lines[0].split(' ')
        if len(first_line_tokens) < 2:
            raise ValueError("Invalid HTTP request")
        
        method = first_line_tokens[0]
        url = first_line_tokens[1]
        if method == 'CONNECT':
            host, port = url.split(':')
            return host, int(port)
        else:
            # Extract host and port from Host header
            for line in lines[1:]:
                if line.startswith('Host:'):
                    host_port = line.split(' ')[1].split(':')
                    if len(host_port) == 2:
                        return host_port[0], int(host_port[1])
                    else:
                        return host_port[0], 80  # Default HTTP port
    
    def start(self):
        self.proxy_socket.listen(5)
        print(f"Proxy server is listening on {self.host}:{self.port}")
        
        while True:
            client_socket, client_addr = self.proxy_socket.accept()
            print(f"Accepted connection from {client_addr[0]}:{client_addr[1]}")
            client_handler = threading.Thread(target=self.handle_client, args=(client_socket,))
            client_handler.start()

if __name__ == "__main__":
    proxy = HTTPProxy("127.0.0.1", 8888)  # Change the host and port as needed
    proxy.start()
