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
        self.hasMoved = False

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
        player = self.player
        current_square = board.find_piece(self)
        board.move_piece(current_square, new_square)


    def position(self, board):
        return board.find_piece(self)

    def get_linear_moves(self, board, vectors, isKingOrKnight = False):
        moveList = []

        for vector in vectors:
            moveList = self.addDirection(board, vector, moveList, isKingOrKnight)

        return moveList

    def addDirection(self, board, vector, moveList, isKingOrKnight = False):
        new_square = board.find_piece(self)
        while True:
            new_square = new_square.applyVector(vector)

            if not new_square.squareOnBoard():
                return moveList

            if new_square.isEmpty(board):
                moveList.append(new_square)
                if isKingOrKnight:
                    return moveList
            else:
                otherPiece = board.get_piece(new_square)
                if otherPiece.player != self.player:
                    moveList.append(new_square)
                    return moveList
                else:
                    return moveList


class Pawn(Piece):
    """
    A class representing a chess pawn.
    """
    def __init__(self, player):
        Piece.__init__(self, player)
        self.enPassant = False

    def GetPotentialCaptureSquares(self, direction, current_pos, board):
        potentialCaptureSquares = []
        rightDiagonal = Square.at(current_pos.row + direction, current_pos.col + 1)
        if rightDiagonal.squareOnBoard():
            potentialCaptureSquares.append(rightDiagonal)
        leftDiagonal = Square.at(current_pos.row + direction, current_pos.col - 1)
        if leftDiagonal.squareOnBoard():
            potentialCaptureSquares.append(leftDiagonal)

        return potentialCaptureSquares

    def ValidateCaptureSquares(self, listOfSquares, board):
        CaptureSquares = []
        for square in listOfSquares:

            if square.isEmpty(board) == False:
                piece = board.get_piece(square)
                if self.player != piece.player:
                    CaptureSquares.append(square)

        return CaptureSquares

    def get_available_moves(self, board):
        if self.player == Player.WHITE:
            direction = 1
            start_row = 1
        else:
            direction = -1
            start_row = 6

        current_pos = board.find_piece(self)
        fowardMoveList = self.FowardMoves(board, current_pos, direction, start_row)
        captureSquares = self.GetPotentialCaptureSquares(direction, current_pos, board)
        captureSquares =  self.ValidateCaptureSquares(captureSquares, board)
        moveList = fowardMoveList + captureSquares + self.checkEnPessant(board)

        return moveList

    def checkEnPessant(self, board):

        lastPiece = board.lastPieceMoved

        if not isinstance(lastPiece, Pawn):
            return []

        if not lastPiece.enPassant:
            return []

        current_square = board.find_piece(self)
        opponent_square = board.find_piece(lastPiece)

        if current_square.row != opponent_square.row:
            return []
        if (current_square.col - opponent_square.col) != 1 or -1:
            return []

        if self.player == Player.WHITE:
            direction = 1
        else:
            direction = -1

        enPessantSquare = Square.at(opponent_square.row + direction, opponent_square.col)

        return [enPessantSquare]

    def FowardMoves(self, board, current_pos, direction,  start_row):
        moveList = []
        next_square = Square.at(current_pos.row + direction, current_pos.col)
        second_square = Square.at(current_pos.row + 2 * direction, current_pos.col)
        if next_square.squareOnBoard():
            if board.get_piece(next_square) is None:  # next square free
                moveList.append(next_square)
        if board.get_piece(next_square) is None and board.get_piece(
                second_square) is None and current_pos.row == start_row:
            moveList.append(second_square)
        return moveList

    def move_to(self, board, new_square):
        """
        Move this piece to the given square on the board.
        """
        current_square = board.find_piece(self)
        if current_square.row - new_square.row == 2 or -2:
            self.enPassant = True
        board.move_piece(current_square, new_square)


class Knight(Piece):
    """
    A class representing a chess knight.
    """

    def get_available_moves(self, board):
        return []
    vectors = [[1, 2], [1, -2], [-1, 2], [-1, -2], [2, 1], [2, -1], [-2, 1], [-2, -1]]

    def get_available_moves(self, board):
        isKnight = True
        moveList = self.get_linear_moves(board, self.vectors, isKnight)
        return moveList


class Bishop(Piece):
    """
    A class representing a chess bishop.
    """
    vectors = [[1, 1], [1, -1], [-1, 1], [-1, -1]]

    def get_available_moves(self, board):
        moveList = self.get_linear_moves(board, self.vectors)
        return moveList


class Rook(Piece):
    """
    A class representing a chess rook.
    """
    vectors = [[1, 0], [-1, 0], [0, 1], [0, -1]]


    def get_available_moves(self, board):
        moveList = self.get_linear_moves(board, self.vectors)

        return moveList

class Queen(Piece):
    """
    A class representing a chess queen.
    """
    vectors = Rook.vectors + Bishop.vectors

    def get_available_moves(self, board):
        moveList = self.get_linear_moves(board, self.vectors)
        return moveList


class King(Piece):
    """
    A class representing a chess king.
    """
    vectors = Queen.vectors
    # todo add castling
    def get_available_moves(self, board):
        isKing = True
        moveList = self.get_linear_moves(board, self.vectors, isKing)
        return moveList

    # def checkCastling(self, board):
    #     if self.hasMoved == True:
    #         return []
    # 
    #     row = board.find_piece(self).row
    #     leftCorner = Square.at(row, 0)
    #     rightCorner = Square.at(row, 7)
    #     if leftCorner.isEmpty(board) or rightCorner.isEmpty(board):
    #         return []
    #
    #     leftRook = board.get_piece(leftCorner)
    #     leftList = self.checkLeftRook(board, leftRook)
    #
    #
    # def checkLeftRook(self, board, leftRook, row):
    #     if leftRook.hasMoved:
    #         return []