import os
import socket
from dotenv import load_dotenv

class Client:
    load_dotenv()
    SERVER_HOST = os.getenv("HOST", "127.0.0.1")
    SERVER_PORT = int(os.getenv("PORT", "5000"))

    def __init__(self):
        try:
            self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            self.server_address = (self.SERVER_HOST, self.SERVER_PORT)
        except (socket.timeout, socket.error) as e:
            print(f"Error creating socket: {e}")
            raise

    def send(self, message):
        try:
            self.sock.sendto(message.encode(), self.server_address)
        except OSError as e:
            print(f"Send error: {e}")

    def receive(self):
        try:
            data, _ = self.sock.recvfrom(4096)
            return data.decode()
        except OSError as e:
            print(f"Receive error: {e}")
            return ""

    def close(self):
        try:
            self.sock.close()
        except OSError as e:
            print(f"Socket close error: {e}")

def main():
    c = Client()
    # إرسال رسالة للانضمام للسيرفر
    c.send("join")

    try:
        while True:
            response = c.receive()
            if not response:
                break
            print(response, end="")  # نطبعها كما هي للمحافظة على شكل اللعبة

            if "Your move" in response:
                move = input("Enter your move (0-8): ")
                c.send(move)

    except KeyboardInterrupt:
        print("\nDisconnected by user.")
    finally:
        c.close()

if __name__ == "__main__":
    main()
