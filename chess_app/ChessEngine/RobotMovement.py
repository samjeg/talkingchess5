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


	# Gets the current chess piece id's do that later on can check if a piece has been captured
	def getCurrentChessPieces(self):
		matrix = self.chess_mech.chessPiece.live_chessboard_matrix
		array = []

		for i in range(8):
			for j in range(8):
				if self.chess_piece.isType(matrix[i][j], "comp_") or self.chess_piece.isType(matrix[i][j], "player_"):
					array.append(matrix[i][j])

		self.current_chess_piece_ids = array

		return array


	# def checkCaptured(self, matrix):
	# 	chess_piece_ids = [ 
	# 		"comp_pawn1", "comp_pawn2", "comp_pawn3", "comp_pawn4", "comp_pawn5", "comp_pawn6", "comp_pawn7", "comp_pawn8", 
	# 		"comp_rook1", "comp_horse1", "comp_bishop1", "comp_queen", "comp_king", "comp_bishop2", "comp_horse2", "comp_rook2",
	# 		"player_pawn1", "player_pawn2", "player_pawn3", "player_pawn4", "player_pawn5", "player_pawn6", "player_pawn7", "player_pawn8",
	# 		"player_rook1", "player_horse1", "player_bishop1", "player_queen", "player_king", "player_bishop2", "player_horse2", "player_rook2",
	# 	]

	# 	for i in range(8):
	# 		for j in range(8):
	# 			for k in range(len(chess_piece_ids)):


