import socket
import os
import json
import http_request

def load_cfg():
    with open("config.json", "r") as cfg:
        data = json.load(cfg)
    return data

config = load_cfg()

HOST = config["HOST"]
PORT = config["PORT"]
DIRECTORY = config["DIRECTORY"]
INDEX_FILE = config["INDEX_FILE"]
ERROR_404 = config["404"]

SERVER_DIR = os.path.dirname(os.path.realpath(__file__))

def run_server():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server_socket:
        server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        server_socket.bind((HOST, PORT))
        server_socket.listen(1)
        print(f"Сервер запущен на порту {PORT}")
        print(f"Рабочая директория: {DIRECTORY}")
        os.chdir(DIRECTORY)

        while True:
            client_socket, addr = server_socket.accept()
            http_request.handle_request(client_socket, DIRECTORY, INDEX_FILE, ERROR_404, SERVER_DIR)

run_server()