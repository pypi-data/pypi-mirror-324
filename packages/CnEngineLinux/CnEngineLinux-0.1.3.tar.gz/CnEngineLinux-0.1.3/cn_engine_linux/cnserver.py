import socket
import os
import sys
from datetime import datetime

def main():
    def message(msg):
        current_time = datetime.now()
        formatted_time = current_time.strftime('[%a %b %d %H:%M:%S %Y]')
        print(f"{formatted_time} {msg}")

    def create_server(ip=""):
        server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server_socket.bind((ip, 60000))
        server_socket.listen(1)
        message(f"CN Engine 0.1.3 Server (cn://{ip}) started")
        message("The server listens to requests from: CN")

        try:
            while True:
                client_socket, client_address = server_socket.accept()
                message(f"{client_address} Accepted")
                request = client_socket.recv(1024).decode('utf-8')
                message(f"{client_address} Req: {request}")

                if request.startswith('cn:GET:/'):
                    file_name = request[8:]
                    if os.path.exists(file_name):
                        with open(file_name, "r") as f:
                            output_script = f.read()
                            client_socket.sendall(output_script.encode())
                    else:
                        client_socket.sendall(b"Error 404\n     Not Found")

                message(f"{client_address} Closing")
                client_socket.close()

        except KeyboardInterrupt:
            message("CTRL-C pressed, shutting down...")
            server_socket.close()  # Zavře serverový socket
            exit(0)

    if len(sys.argv) > 1:
        if sys.argv[1] == "version":
            print(f"Rasmnout CN Engine 0.1.3 Server")
        else:
            ip = sys.argv[1]
            create_server(ip=ip)
    else:
        message("Usage: cn-server <LISTEN IP>")
