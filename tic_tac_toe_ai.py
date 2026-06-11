import tkinter as tk
from tkinter import messagebox
import math

player_symbol = "X"
ai_symbol = "O"

player_wins = 0
ai_wins = 0
draws = 0
games_played = 0

board = [""] * 9
buttons = []

root = tk.Tk()
root.title("Tic Tac Toe AI")
root.geometry("450x600")

score_label = None
status_label = None


def update_score():
    score_label.config(
        text=f"Player Wins: {player_wins}   AI Wins: {ai_wins}\nDraws: {draws}   Games: {games_played}"
    )


def check_winner(b, p):
    wins = [
        [0,1,2],[3,4,5],[6,7,8],
        [0,3,6],[1,4,7],[2,5,8],
        [0,4,8],[2,4,6]
    ]
    return any(all(b[i] == p for i in w) for w in wins)


def is_draw(b):
    return "" not in b


def minimax(b, maximizing):
    if check_winner(b, ai_symbol):
        return 1
    if check_winner(b, player_symbol):
        return -1
    if is_draw(b):
        return 0

    if maximizing:
        best = -math.inf
        for i in range(9):
            if b[i] == "":
                b[i] = ai_symbol
                best = max(best, minimax(b, False))
                b[i] = ""
        return best
    else:
        best = math.inf
        for i in range(9):
            if b[i] == "":
                b[i] = player_symbol
                best = min(best, minimax(b, True))
                b[i] = ""
        return best


def ai_move():
    best_score = -math.inf
    move = None

    for i in range(9):
        if board[i] == "":
            board[i] = ai_symbol
            score = minimax(board, False)
            board[i] = ""

            if score > best_score:
                best_score = score
                move = i

    if move is not None:
        board[move] = ai_symbol
        buttons[move].config(text=ai_symbol)

    finish_check()


def finish_check():
    global player_wins, ai_wins, draws, games_played

    if check_winner(board, player_symbol):
        player_wins += 1
        games_played += 1
        update_score()
        messagebox.showinfo("Game Over", "You Win!")
        reset_board()
        return True

    if check_winner(board, ai_symbol):
        ai_wins += 1
        games_played += 1
        update_score()
        messagebox.showinfo("Game Over", "AI Wins!")
        reset_board()
        return True

    if is_draw(board):
        draws += 1
        games_played += 1
        update_score()
        messagebox.showinfo("Game Over", "Draw!")
        reset_board()
        return True

    return False


def player_click(idx):
    if board[idx] != "":
        return

    board[idx] = player_symbol
    buttons[idx].config(text=player_symbol)

    if not finish_check():
        ai_move()


def reset_board():
    global board
    board = [""] * 9

    for btn in buttons:
        btn.config(text="")

    if player_symbol == "O":
        root.after(300, ai_move)


def new_match():
    global player_wins, ai_wins, draws, games_played
    player_wins = ai_wins = draws = games_played = 0
    update_score()
    reset_board()


def quit_game():
    global player_wins, ai_wins, draws, games_played
    player_wins = ai_wins = draws = games_played = 0
    root.destroy()


def choose_symbol(symbol):
    global player_symbol, ai_symbol

    player_symbol = symbol
    ai_symbol = "O" if symbol == "X" else "X"

    choice_frame.pack_forget()
    game_frame.pack(fill="both", expand=True)

    status_label.config(text=f"Player: {player_symbol}    AI: {ai_symbol}")
    update_score()

    if player_symbol == "O":
        ai_move()


choice_frame = tk.Frame(root)
choice_frame.pack(expand=True)

tk.Label(choice_frame, text="Choose Your Symbol", font=("Arial", 18, "bold")).pack(pady=20)

tk.Button(choice_frame, text="X", width=10, height=2,
          command=lambda: choose_symbol("X")).pack(pady=10)

tk.Button(choice_frame, text="O", width=10, height=2,
          command=lambda: choose_symbol("O")).pack(pady=10)

game_frame = tk.Frame(root)

status_label = tk.Label(game_frame, font=("Arial", 14, "bold"))
status_label.pack(pady=10)

score_label = tk.Label(game_frame, font=("Arial", 12))
score_label.pack(pady=10)

board_frame = tk.Frame(game_frame)
board_frame.pack()

for i in range(9):
    btn = tk.Button(
        board_frame,
        text="",
        font=("Arial", 24, "bold"),
        width=4,
        height=2,
        command=lambda i=i: player_click(i)
    )
    btn.grid(row=i//3, column=i%3)
    buttons.append(btn)

control_frame = tk.Frame(game_frame)
control_frame.pack(pady=20)

tk.Button(control_frame, text="Restart", command=reset_board).grid(row=0, column=0, padx=5)
tk.Button(control_frame, text="New Match", command=new_match).grid(row=0, column=1, padx=5)
tk.Button(control_frame, text="Quit", command=quit_game).grid(row=0, column=2, padx=5)

root.mainloop()
