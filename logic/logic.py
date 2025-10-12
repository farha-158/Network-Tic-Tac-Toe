class TicTacToe:
    def __init__(self):
        # Initialize a 3x3 empty game board
        self.board = [[" " for _ in range(3)] for _ in range(3)]
        # Set the starting player to "X"
        self.current_player = "X"
        # Store the winner once the game ends
        self.winner = None
        # Flag to indicate if the game is finished
        self.game_over = False

    def reset(self):
        """Reset the game to its initial state."""
        self.board = [[" " for _ in range(3)] for _ in range(3)]
        self.current_player = "X"
        self.winner = None
        self.game_over = False

    def make_move(self, position):
        """
        Attempt to make a move on the board.
        :param position: An integer from 0 to 8 representing the cell on the 3x3 board.
        :return: Tuple (success: bool, message: str)
        """
        # Prevent moves if the game has already ended
        if self.game_over:
            return False, "Game is over"

        # Check if the position is valid
        if position < 0 or position > 8:
            return False, "Invalid position"

        # Convert position (0–8) into (row, col)
        row, col = divmod(position, 3)

        # Ensure the chosen cell is empty
        if self.board[row][col] != " ":
            return False, "Position already taken"

        # Place the player's symbol on the board
        self.board[row][col] = self.current_player

        # Check if this move caused a win
        if self.check_win():
            self.winner = self.current_player
            self.game_over = True
            return True, f"Winner: {self.current_player}"

        # Check if the board is full (draw)
        if self.is_draw():
            self.game_over = True
            return True, "Draw!"

        # Switch to the other player and continue the game
        self.switch_player()
        return True, f"Player {self.current_player}'s turn"

    def check_win(self):
        """Check if the current player has won the game."""
        # Check rows
        for row in self.board:
            if row[0] == row[1] == row[2] != " ":
                return True

        # Check columns
        for col in range(3):
            if self.board[0][col] == self.board[1][col] == self.board[2][col] != " ":
                return True

        # Check diagonals
        if self.board[0][0] == self.board[1][1] == self.board[2][2] != " ":
            return True
        if self.board[0][2] == self.board[1][1] == self.board[2][0] != " ":
            return True

        return False

    def is_draw(self):
        """Return True if all cells are filled and there is no winner."""
        return all(cell != " " for row in self.board for cell in row)

    def switch_player(self):
        """Switch turn between X and O."""
        self.current_player = "O" if self.current_player == "X" else "X"

    def print_board(self):
        """Return the current board state (for debugging or display purposes)."""
        return self.board

    def display_board(self):
        """Print the current board in a 3x3 grid format."""
        print("\n")
        for i in range(3):
            print(" | ".join(self.board[i]))
            if i < 2:
                print("-" * 9)
        print("\n")
