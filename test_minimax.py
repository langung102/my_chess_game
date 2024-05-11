import chess
import chess.engine
import random
import time
from board_evaluator import evaluate
import tkinter as tk

def make_random_move(board):
    legal_moves = list(board.legal_moves)
    random_move = random.choice(legal_moves)
    board.push(random_move)
    return random_move

def minimax(board, depth, maximizing_player, alpha, beta):
    if depth == 0 or board.is_game_over():
        return evaluate(board)

    if maximizing_player:
        max_eval = float('-inf')
        for move in board.legal_moves:
            board.push(move)
            eval = minimax(board, depth - 1, False, alpha, beta)
            board.pop()
            max_eval = max(max_eval, eval)
            alpha = max(alpha, max_eval)
            if beta <= alpha:
                break
        return max_eval
    else:
        min_eval = float('inf')
        for move in board.legal_moves:
            board.push(move)
            eval = minimax(board, depth - 1, True, alpha, beta)
            board.pop()
            min_eval = min(min_eval, eval)
            beta = min(beta, min_eval)
            if beta <= alpha:
                break
        return min_eval

def make_minimax_move(board, depth):
    #Enemy if BLACK
    best_move = None
    best_eval = float('inf')
    for move in board.legal_moves:
        board.push(move)
        eval = minimax(board, depth - 1, True, -10000, 10000)
        board.pop()
        if eval < best_eval:
            best_eval = eval
            best_move = move
    board.push(best_move)
    return best_move

board = chess.Board()

while not board.is_game_over():
    if board.turn == chess.WHITE:
        print("White's turn")
        make_random_move(board)
        # make_minimax_move(board, 3)  # You can adjust the depth here
    else:
        print("Black's turn")
        # make_random_move(board)
        make_minimax_move(board, 5)  # You can adjust the depth here
    print(board)

print("Game Over")
print("Result:", board.outcome())