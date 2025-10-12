import socket
import threading

HOST = "127.0.0.1"
PORT = 5000

clients_waiting = []
lock = threading.Lock()

def print_board(board):
    def cell(i):
        return f"  {board[i] if board[i] != ' ' else ' '}  "
    
    line = "_____|_____|_____"
    empty_line = "     |     |     "
    
    return (
        f"\n{empty_line}\n"
        f"{cell(0)}|{cell(1)}|{cell(2)}\n"
        f"{line}\n"
        f"{empty_line}\n"
        f"{cell(3)}|{cell(4)}|{cell(5)}\n"
        f"{line}\n"
        f"{empty_line}\n"
        f"{cell(6)}|{cell(7)}|{cell(8)}\n"
        f"{empty_line}\n\n"
    )

def check_winner(board):
    combos = [
        (0,1,2), (3,4,5), (6,7,8),
        (0,3,6), (1,4,7), (2,5,8),
        (0,4,8), (2,4,6)
    ]
    for a,b,c in combos:
        if board[a] == board[b] == board[c] and board[a] != " ":
            return board[a]
    if " " not in board:
        return "Draw"
    return None

def handle_game(p1, p2):
    board = [" "] * 9
    turn = p1
    symbols = {p1: "X", p2: "O"}

    for sock in [p1, p2]:
        sock.send(f"Game start! You are {symbols[sock]}\n".encode())

    while True:
        try:
            current = turn
            other = p2 if turn == p1 else p1

            current.send("Your move (0-8): ".encode())
            other.send("Waiting for opponent...\n".encode())

            move = current.recv(1024).decode().strip()
            if not move:
                break

            if not move.isdigit() or not (0 <= int(move) <= 8):
                current.send("Invalid input. Try again.\n".encode())
                continue

            move = int(move)
            if board[move] != " ":
                current.send("Cell taken! Try another.\n".encode())
                continue

            board[move] = symbols[current]
            winner = check_winner(board)

            board_state = print_board(board)
            for sock in [p1, p2]:
                sock.send(f"{board_state}\n".encode())

            if winner:
                msg = f"Game over! Winner: {winner}\n"
                for sock in [p1, p2]:
                    sock.send(msg.encode())
                    sock.close()
                print(msg)
                break

            turn = other

        except Exception as e:
            print(f"Error: {e}")
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
