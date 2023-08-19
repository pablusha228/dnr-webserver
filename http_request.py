import os
import json

def load_cfg():
    with open("config.json", "r") as cfg:
        data = json.load(cfg)
    return data

config = load_cfg()

def handle_request(client_socket, DIRECTORY, INDEX_FILE, SERVER_DIR):
    try:
        request_data = client_socket.recv(1024).decode('utf-8')
        request_path = request_data.split(' ')[1]
        if request_path == '/':
            file_path = os.path.join(DIRECTORY, INDEX_FILE)
        else:
            file_path = os.path.join(DIRECTORY, request_path[1:])

        if os.path.isfile(file_path):
            with open(file_path, 'rb') as file:
                file_data = file.read()
                response = 'HTTP/1.1 200 OK\r\nContent-Type: text/html; charset=utf-8\r\nServer: DNR Server\r\n\r\n'
                client_socket.sendall(response.encode('utf-8') + file_data)
        else:
            if os.path.isfile(os.path.join(SERVER_DIR, 'error_404.html')):
                with open(os.path.join(SERVER_DIR, 'error_404.html'), 'rb') as file:
                    file_data = file.read()
                    response = 'HTTP/1.1 404 Not Found\r\nContent-Type: text/html; charset=utf-8\r\nServer: DNR Server\r\n\r\n'
                    client_socket.sendall(response.encode('utf-8') + file_data)
            else:
                response = 'HTTP/1.1 404 Not Found\r\nContent-Type: text/html; charset=utf-8\r\nServer: DNR Server\r\n\r\nFile not found'
                client_socket.sendall(response.encode('utf-8'))

        client_socket.close()
    except:
        pass