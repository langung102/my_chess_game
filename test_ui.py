import random

import pygame

import chess
import chess.svg
from board_evaluator import evaluate

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


# Function to make a random move for the AI side
def minimax(board, depth, maximizing_player, alpha, beta):
    if depth == 0 or board.is_game_over():
        return evaluate(board)

    if maximizing_player:
        max_eval = float("-inf")
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
        min_eval = float("inf")
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
    # Enemy if BLACK
    best_move = None
    best_eval = float("inf")
    for move in board.legal_moves:
        board.push(move)
        eval = minimax(board, depth - 1, True, -10000, 10000)
        board.pop()
        if eval < best_eval:
            best_eval = eval
            best_move = move
    board.push(best_move)


# Main loop
running = True
selected_square = None

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif (
            event.type == pygame.MOUSEBUTTONDOWN and board.turn == chess.WHITE
        ):  # Human player's turn
            mouse_pos = pygame.mouse.get_pos()
            file = mouse_pos[0] // SQUARE_SIZE
            rank = (
                7 - mouse_pos[1] // SQUARE_SIZE
            )  # Flip rank because chessboard is drawn from top to bottom
            square = chess.square(file, rank)

            if selected_square is None:
                if (
                    board.piece_at(square) is not None
                    and board.piece_at(square).color == chess.WHITE
                ):
                    selected_square = square
            else:
                move = chess.Move(selected_square, square)
                if move in board.legal_moves:
                    board.push(move)
                selected_square = None
        elif board.turn == chess.BLACK:  # AI's turn
            make_minimax_move(board, 3)

    # Draw the chessboard
    for file in range(BOARD_SIZE):
        for rank in range(BOARD_SIZE):
            color = WHITE if (file + rank) % 2 == 0 else BLACK
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

    # Update the display
    pygame.display.flip()

# Quit Pygame
pygame.quit()
