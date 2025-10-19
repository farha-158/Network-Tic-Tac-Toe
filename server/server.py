import socket
from logic.logic import TicTacToe

SERVER_HOST = "127.0.0.1"
SERVER_PORT = 5000

def main():
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    server_socket.bind((SERVER_HOST, SERVER_PORT))
    print(f"Server running on {SERVER_HOST}:{SERVER_PORT}")

    print("Waiting for players to join...")

    # استقبال أول لاعبين
    data1, addr1 = server_socket.recvfrom(1024)
    print(f"Player 1 connected from {addr1}")
    server_socket.sendto("Welcome! Waiting for opponent...\n".encode(), addr1)

    data2, addr2 = server_socket.recvfrom(1024)
    print(f"Player 2 connected from {addr2}")
    server_socket.sendto("Welcome! You are connected!\n".encode(), addr2)

    # بدء اللعبة
    game = TicTacToe(addr1, addr2)

    # إرسال رسائل البداية لكل لاعب
    msg1 = f"Game start! You are {game.symbols[addr1]}\n{game.print_board()}"
    msg2 = f"Game start! You are {game.symbols[addr2]}\n{game.print_board()}"

    server_socket.sendto(msg1.encode(), addr1)
    server_socket.sendto(msg2.encode(), addr2)

    current_player = addr1

    while True:
        # إخطار اللاعب الحالي بدوره
        server_socket.sendto("Your move (0-8): ".encode(), current_player)

        # استقبال الحركة
        move_data, addr = server_socket.recvfrom(1024)
        move = move_data.decode().strip()

        try:
            game.make_move(current_player, move)
        except Exception as e:
            # في حالة الخطأ، نبلغ اللاعب الحالي فقط
            server_socket.sendto(f"{str(e)}\n".encode(), current_player)
            continue

        # طباعة البورد الجديد
        board_state = game.print_board()

        # إرسال البورد للحالتين
        for addr in [addr1, addr2]:
            full_message = f"{board_state}\n"
            server_socket.sendto(full_message.encode(), addr)

        # تحقق من الفائز
        winner = game.check_winner()
        if winner:
            if winner == "Draw":
                result = "It's a draw!\n"
            else:
                result = f"Player {winner} wins!\n"

            for addr in [addr1, addr2]:
                server_socket.sendto(result.encode(), addr)
            break

        # تبديل الدور
        current_player = addr2 if current_player == addr1 else addr1

    server_socket.close()

if __name__ == "__main__":
    main()
