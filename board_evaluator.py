import chess
from board_pieces_tables import *

class Evaluation:
    def __init__(self, level):
        if (level == "EASY"):
            self.PAWN_TABLE = PAWN_TABLE
            self.KNIGHTS_TABLE = KNIGHTS_TABLE
            self.BISHOPS_TABLE = BISHOPS_TABLE
            self.ROOKS_TABLE = ROOKS_TABLE
            self.QUEENS_TABLE = QUEENS_TABLE
            self.KINGS_TABLE = KINGS_TABLE  
        elif (level == "MEDIUM"):
            return
        elif (level == "HARD"):
            self.PAWN_TABLE = PAWN_TABLE_HARD
            self.KNIGHTS_TABLE = KNIGHTS_TABLE_HARD
            self.BISHOPS_TABLE = BISHOPS_TABLE_HARD
            self.ROOKS_TABLE = ROOKS_TABLE_HARD
            self.QUEENS_TABLE = QUEENS_TABLE_HARD
            self.KINGS_TABLE = KINGS_TABLE_HARD

    def evaluate(self, board):
        """
        Given a particular board, evaluates it and gives it a score.
        A higher score indicates it is better for white.
        A lower score indicates it is better for black.

        Args:
            board (chess.Board): A chess board.

        Returns:
            int: A score indicating the state of the board (higher is good for white, lower is good for black)
        """    

        boardvalue = 0
        
        wp = len(board.pieces(chess.PAWN, chess.WHITE))
        bp = len(board.pieces(chess.PAWN, chess.BLACK))
        wn = len(board.pieces(chess.KNIGHT, chess.WHITE))
        bn = len(board.pieces(chess.KNIGHT, chess.BLACK))
        wb = len(board.pieces(chess.BISHOP, chess.WHITE))
        bb = len(board.pieces(chess.BISHOP, chess.BLACK))
        wr = len(board.pieces(chess.ROOK, chess.WHITE))
        br = len(board.pieces(chess.ROOK, chess.BLACK))
        wq = len(board.pieces(chess.QUEEN, chess.WHITE))
        bq = len(board.pieces(chess.QUEEN, chess.BLACK))

        material = 100 * (wp - bp) + 300 * (wn - bn) + 300 * (wb - bb) + 500 * (wr - br) + 900 * (wq - bq)
        pawn_sum = sum([self.PAWN_TABLE[i] for i in board.pieces(chess.PAWN, chess.WHITE)])
        pawn_sum = pawn_sum + sum([-self.PAWN_TABLE[chess.square_mirror(i)] for i in board.pieces(chess.PAWN, chess.BLACK)])
        knight_sum = sum([self.KNIGHTS_TABLE[i] for i in board.pieces(chess.KNIGHT, chess.WHITE)])
        knight_sum = knight_sum + sum([-self.KNIGHTS_TABLE[chess.square_mirror(i)] for i in board.pieces(chess.KNIGHT, chess.BLACK)])
        bishop_sum = sum([self.BISHOPS_TABLE[i] for i in board.pieces(chess.BISHOP, chess.WHITE)])
        bishop_sum = bishop_sum + sum([-self.BISHOPS_TABLE[chess.square_mirror(i)] for i in board.pieces(chess.BISHOP, chess.BLACK)])
        rook_sum = sum([self.ROOKS_TABLE[i] for i in board.pieces(chess.ROOK, chess.WHITE)]) 
        rook_sum = rook_sum + sum([-self.ROOKS_TABLE[chess.square_mirror(i)] for i in board.pieces(chess.ROOK, chess.BLACK)])
        queens_sum = sum([self.QUEENS_TABLE[i] for i in board.pieces(chess.QUEEN, chess.WHITE)]) 
        queens_sum = queens_sum + sum([-self.QUEENS_TABLE[chess.square_mirror(i)] for i in board.pieces(chess.QUEEN, chess.BLACK)])
        kings_sum = sum([self.KINGS_TABLE[i] for i in board.pieces(chess.KING, chess.WHITE)]) 
        kings_sum = kings_sum + sum([-self.KINGS_TABLE[chess.square_mirror(i)] for i in board.pieces(chess.KING, chess.BLACK)])
        
        boardvalue = material + pawn_sum + knight_sum + bishop_sum + rook_sum + queens_sum + kings_sum
        
        return boardvalue