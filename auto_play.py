import random

import pygame

import time
import chess
import chess.svg
from board_evaluator import Evaluation

############################################
#####SELECT LEVEL (EASY, MEDIUM or HARD)####
level = "HARD"
is_white_random = False
is_black_random = False
depth_white = 1
depth_black = 4
############################################

# Initialize Pygame
pygame.init()

# Constants
SCREEN_WIDTH = 512
SCREEN_HEIGHT = 512
BOARD_SIZE = 8
SQUARE_SIZE = SCREEN_WIDTH // BOARD_SIZE

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
HIGHLIGHT_COLOR = (0, 255, 0)

# Font
font = pygame.font.Font(None, 36)

# Create the screen
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Chess Game")

# Create a chess board
board = chess.Board()

EVAL = Evaluation(level)

# Function to highlight legal moves for the selected piece
def highlight_legal_moves(square):
    legal_moves = board.legal_moves
    for move in legal_moves:
        if move.from_square == square:
            file = chess.square_file(move.to_square)
            rank = 7 - chess.square_rank(move.to_square)
            rect = pygame.Rect(file * SQUARE_SIZE, rank * SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE)
            pygame.draw.rect(screen, HIGHLIGHT_COLOR, rect, 4)

# Function to make a random move for the AI side
def minimax(board, depth, maximizing_player, alpha, beta):
    if depth == 0 or board.is_game_over():
        return EVAL.evaluate(board)

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

def make_minimax_move(board, depth, is_white):
    best_move = None
    if is_white:
        best_eval = float('-inf')
        for move in board.legal_moves:
            if chess.square_rank(move.to_square) == 7 and board.piece_at(move.from_square).piece_type == chess.PAWN:
                move.promotion = chess.QUEEN
                print("promotion!")
            board.push(move)
            eval = minimax(board, depth - 1, False, -10000, 10000)
            board.pop()
            if eval > best_eval:
                best_eval = eval
                best_move = move    
    else:
        best_move = None
        best_eval = float('inf')
        for move in board.legal_moves:
            if chess.square_rank(move.to_square) == 7 and board.piece_at(move.from_square).piece_type == chess.PAWN:
                move.promotion = chess.QUEEN
                print("promotion!")
            board.push(move)
            eval = minimax(board, depth - 1, True, -10000, 10000)
            board.pop()
            if eval < best_eval:
                best_eval = eval
                best_move = move
    if best_move is not None:
        board.push(best_move)
    return best_move

def make_random_move(board):
    legal_moves = list(board.legal_moves)
    random_move = random.choice(legal_moves)
    board.push(random_move)
    return random_move

# Main loop
running = True
selected_square = None

while running and not board.is_game_over():
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    if (board.turn == chess.WHITE):
        if is_white_random:
            make_random_move(board)
        else:
            make_minimax_move(board, depth_white, board.turn == chess.WHITE)
    else:
        if is_black_random:
            make_random_move(board)
        else:
            make_minimax_move(board, depth_black, board.turn == chess.WHITE)

    # Draw the chessboard
    for file in range(BOARD_SIZE):
        for rank in range(BOARD_SIZE):
            color = BLACK if (file + rank) % 2 == 0 else WHITE
            rect = pygame.Rect(
                file * SQUARE_SIZE, (7 - rank) * SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE
            )
            pygame.draw.rect(screen, color, rect)

    # Draw the chess pieces
    for square in chess.SQUARES:
        piece = board.piece_at(square)
        if piece is not None:
            piece_img = pygame.image.load(
                f"pieces/{piece.symbol()}.png"
            ).convert_alpha()
            # Scale the image
            piece_img = pygame.transform.scale(piece_img, (SQUARE_SIZE, SQUARE_SIZE))
            screen.blit(
                piece_img,
                (
                    chess.square_file(square) * SQUARE_SIZE,
                    (7 - chess.square_rank(square)) * SQUARE_SIZE,
                ),
            )
    # Highlight selected square
    if selected_square is not None:
        highlight_rect = pygame.Rect(
            chess.square_file(selected_square) * SQUARE_SIZE,
            (7 - chess.square_rank(selected_square)) * SQUARE_SIZE,
            SQUARE_SIZE,
            SQUARE_SIZE,
        )
        pygame.draw.rect(screen, HIGHLIGHT_COLOR, highlight_rect, 4)

        #Draw possible mobe
        highlight_legal_moves(selected_square)
    # Update the display
    pygame.display.flip()
    # Check if the game is over
    if board.is_game_over():
        print(board.result())
        if board.outcome().winner == None:
            text = font.render(f"{board.outcome().termination}", True, (0, 255, 0))
        else:
            # Determine the winner
            (winner, color) = (
                ("Black", (255, 0, 0))
                if board.turn == chess.WHITE
                else ("White", (0, 255, 0))
            )
            # Create a text surface
            text = font.render(f"Game Over: {winner} wins!", True, color)

        # Get the size of the text surface
        text_rect = text.get_rect()

        # Center the text surface
        text_rect.center = (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)

        # Draw the text surface on the screen
        screen.blit(text, text_rect)

        pygame.display.flip()

        running = False

waiting = True
while waiting:
    for event in pygame.event.get():
        if event.type == pygame.MOUSEBUTTONDOWN:
            waiting = False
# Quit Pygame
pygame.quit()
