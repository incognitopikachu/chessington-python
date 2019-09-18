"""
Definitions of each of the different chess pieces.
"""

from abc import ABC, abstractmethod

from chessington.engine.data import Player, Square

class Piece(ABC):
    """
    An abstract base class from which all pieces inherit.
    """

    def __init__(self, player):
        self.player = player

    @abstractmethod
    def get_available_moves(self, board):
        """
        Get all squares that the piece is allowed to move to.
        """
        pass

    def move_to(self, board, new_square):
        """
        Move this piece to the given square on the board.
        """
        current_square = board.find_piece(self)
        board.move_piece(current_square, new_square)

    def position(self, board):
        return board.find_piece(self)

class Pawn(Piece):
    """
    A class representing a chess pawn.
    """

    def get_available_moves(self, board):
        if self.player == Player.WHITE:
            direction = 1
            start_row = 1
        else:
            direction = -1
            start_row = 6

        current_pos = board.find_piece(self)

        next_square = Square.at(current_pos.row + direction, current_pos.col)
        second_square = Square.at(current_pos.row + 2 * direction, current_pos.col)

        moveList = []
        if board.get_piece(next_square) is None:
            moveList.append(next_square)
        if board.get_piece(next_square) is None and board.get_piece(second_square) is None and current_pos.row == start_row:
            moveList.append(second_square)

        return moveList


class Knight(Piece):
    """
    A class representing a chess knight.
    """

    def get_available_moves(self, board):
        return []


class Bishop(Piece):
    """
    A class representing a chess bishop.
    """

    def get_available_moves(self, board):
        return []


class Rook(Piece):
    """
    A class representing a chess rook.
    """

    def get_available_moves(self, board):
        return []


class Queen(Piece):
    """
    A class representing a chess queen.
    """

    def get_available_moves(self, board):
        return []


class King(Piece):
    """
    A class representing a chess king.
    """

    def get_available_moves(self, board):
        return []