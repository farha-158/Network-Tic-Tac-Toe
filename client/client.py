import os
import socket
from client.exceptions import *
from dotenv import load_dotenv

class client :
    load_dotenv()
    SERVER_HOST = os.getenv("HOST", "127.0.0.1")
    SERVER_PORT = int(os.getenv("PORT", "5000"))

    def __init__(self):
        try:
            self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        except (socket.timeout, socket.error) as e:
            raise NetworkError(f"Unexpected network error: {e}")

    def connect(self, SERVER_HOST =SERVER_HOST, SERVER_PORT = SERVER_PORT):
        try:
            self.sock.connect((SERVER_HOST, SERVER_PORT))
        except ConnectionRefusedError:
             raise ConnectionFailedError("Server refused the connection or not found.")
        except TimeoutError:
            raise TimeoutNetworkError("Connection attempt timed out.")
        except OSError as e:
            raise NetworkError(f"Unexpected network error: {e}") 
    
    def close(self):
        try:
            self.sock.close()
        except OSError as e:
            raise NetworkError(f"Unexpected network error or alerady closed: {e}")
        
    def send(self, message):
        try:
             self.sock.send(message.encode())
        except BrokenPipeError:
            raise ConnectionLostError("Connection lost.")
        except ValueError:
            raise SendDataError("data format error.")
        except OSError as e:
            raise NetworkError(f"Unexpected network error: {e}")
    
    def receive(self):    
         while True:
            try:
                data = data.append(self.sock.recv(1024))
                if not data:
                    break
                print(data)
            except ConnectionRefusedError:
                raise ConnectionFailedError("Server refused the connection or not found.")
            except ValueError:
                raise ReceiveDataError("data format error.")
         return data
