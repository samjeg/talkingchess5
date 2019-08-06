from .ChessPieces.ChessPiece import ChessPiece
from .ChessPieces.Horse import Horse
from .ChessPieces.Rook import Rook
from .ChessPieces.Bishop import Bishop
from .ChessPieces.Queen import Queen
from .ChessPieces.Pawn import Pawn
from .ChessPieces.King import King
from .Selecter import Select
from .CheckerGetter import CheckerGetter
from .ChessMechanics import ChessMechanics


class RobotMovement(object):

	def __init__(self):
		self.chess_mech = ChessMechanics()
		self.chess_piece = ChessPiece()
		self.current_chess_piece_ids = []


	# Gets the current chess piece id's so that later on can check if a piece has been captured
	def getChessPieces(self, matrix):
		array = []

		for i in range(8):
			for j in range(8):
				if self.chess_piece.isType(matrix[i][j], "comp_") or self.chess_piece.isType(matrix[i][j], "player_"):
					array.append(matrix[i][j])

		return array


	# Returns true if it can't find a piece from the old chessboard state in the new chessboard
	def pieceIsMissing(self, new_matrix):
		
		new_chess_pieces = self.getChessPieces(new_matrix)
		old_chess_pieces = self.current_chess_piece_ids

		for i in range(len(old_chess_pieces)):
			for j in range(len(new_chess_pieces)):
				if old_chess_pieces[i] == new_chess_pieces[j]:
					break

			if j == len(new_chess_pieces) - 1 and i != len(old_chess_pieces) -1:
				return True
		
		return False	


	# Returns the missing piece that was gone from the old chessboard state so can assign points for capturing	
	def getMissingPiece(self, new_matrix):
		
		new_chess_pieces = self.getChessPieces(new_matrix)
		old_chess_pieces = self.current_chess_piece_ids

		for i in range(len(old_chess_pieces)):
			for j in range(len(new_chess_pieces)):
				if old_chess_pieces[i] == new_chess_pieces[j]:
					break

			if j == len(new_chess_pieces) - 1 and i != len(old_chess_pieces) -1:
				return old_chess_pieces[i]

		return ""

	# Collects the points of the from taking the missing piece
	def getPoints(self, piece):
		points = 0

		if self.chess_piece.isType(piece, "pawn"):
		 	points = 10

		elif self.chess_piece.isType(piece, "bishop"):
			points = 30

	 	elif self.chess_piece.isType(piece, "horse"):
			points = 30

		elif self.chess_piece.isType(piece, "rook"):
			points = 50

		elif self.chess_piece.isType(piece, "queen"):
			points = 90


		if self.chess_piece.isType(piece, "comp"):
			points = - points

		return points





