import socket
import threading
from logic.logic import TicTacToe
from logic.logicExceptions import (
    InvalidMoveError,
    OutOfRangeError,
    CellOccupiedError,
    NotYourTurnError,
    GameOverError,
    PlayerNotRecognizedError
)

HOST = "127.0.0.1"
PORT = 5000

clients_waiting = []
lock = threading.Lock()


def handle_game(p1, p2):
    game = TicTacToe(p1, p2)

    for sock in [p1, p2]:
        sock.send(f"Game start! You are {game.symbols[sock]}\n".encode())

    while True:
        try:
            current = game.turn
            other = p2 if current == p1 else p1

            current.send("Your move (0-8): ".encode())
            other.send("Waiting for opponent...\n".encode())

            move = current.recv(1024).decode().strip()
            if not move:
                break

            try:
                game.make_move(current, move)
            except InvalidMoveError as e:
                current.send(f"Invalid move: {e}\n".encode())
                continue
            except OutOfRangeError as e:
                current.send(f"Out of range: {e}\n".encode())
                continue
            except CellOccupiedError as e:
                current.send(f"Cell occupied: {e}\n".encode())
                continue
            except NotYourTurnError as e:
                current.send(f"Not your turn: {e}\n".encode())
                continue
            except PlayerNotRecognizedError as e:
                current.send(f"Error: {e}\n".encode())
                break
            except GameOverError as e:
                current.send(f"Game over: {e}\n".encode())
                break

            board_state = game.print_board()
            for sock in [p1, p2]:
                sock.send(f"{board_state}\n".encode())

            if game.winner:
                msg = f"Game over! Winner: {game.winner}\n"
                for sock in [p1, p2]:
                    sock.send(msg.encode())
                    sock.close()
                print(msg)
                break

        except Exception as e:
            print(f"Unexpected Error: {e}")
            break


def client_thread(conn, addr):
    print(f"Connected by {addr}")
    conn.send("Welcome! Waiting for opponent...\n".encode())

    with lock:
        clients_waiting.append(conn)
        if len(clients_waiting) >= 2:
            p1 = clients_waiting.pop(0)
            p2 = clients_waiting.pop(0)
            threading.Thread(target=handle_game, args=(p1, p2), daemon=True).start()


def main():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        s.bind((HOST, PORT))
        s.listen()
        print(f"Server running on {HOST}:{PORT}")

        while True:
            conn, addr = s.accept()
            threading.Thread(target=client_thread, args=(conn, addr), daemon=True).start()


if __name__ == "__main__":
    main()
