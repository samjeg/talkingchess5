from .ChessPieces.ChessPiece import ChessPiece
from chess_app.ChessEngine.Selecter import Select 
from .ChessPieces.Horse import Horse
from .ChessPieces.Bishop import Bishop
from .ChessPieces.Rook import Rook
from .ChessPieces.Queen import Queen
from .ChessPieces.Pawn import Pawn
from .ChessPieces.King import King

class CheckerGetter(object):

	def __init__(self):
		self.chess_piece = ChessPiece()
		self.live_chessboard_matrix = []
		self.horse = Horse()
		self.bishop = Bishop()
		self.rook = Rook()
		self.queen = Queen()
		self.pawn = Pawn()
		self.king = King()

	# gets the postions of all the pieces that are attacking the king
	def fromPiece(self):
		matrix = self.live_chessboard_matrix
		self.horse.live_chessboard_matrix = matrix
		self.bishop.live_chessboard_matrix = matrix
		self.rook.live_chessboard_matrix = matrix
		self.queen.live_chessboard_matrix = matrix
		self.pawn.live_chessboard_matrix = matrix
		self.king.live_chessboard_matrix = matrix
		selectKing = Select()
		king_piece = selectKing.selectFromPieceId(matrix, "comp_king")
		king_coordinates = self.chess_piece.findPieceCoordinates(king_piece)
		x = king_coordinates[1]
		y = king_coordinates[0]
		attackingPawnPlaces = self.pawn.attackingPlaces(x, y)
		attackingHorsePlaces = self.horse.attackingPlaces(x, y)
		attackingRookPlaces = self.rook.attackingPlaces(True, x, y)
		attackingBishopPlaces = self.bishop.attackingPlaces(True, x, y)
		queen1 = self.rook.attackingPlaces(False, x, y)
		queen2 = self.bishop.attackingPlaces(False, x, y)
		attackingQueenPlaces = queen1 + queen2
		attackingPlaces = attackingPawnPlaces + attackingHorsePlaces + attackingRookPlaces + attackingBishopPlaces + attackingQueenPlaces
		
		return attackingPlaces
	
	# gets the position of all the pieces that are attacking a place for checking castling 
	def fromPlace(self, placeId):
		attackingPlaces = []
		placeCoordinates = self.chess_piece.findPlaceCoordinates(placeId)
		x = placeCoordinates[1]
		y = placeCoordinates[0]
		attackingPawnPlaces = self.pawn.attackingPlaces(x, y)
		# print("Checker getter from place %s"%attackingPawnPlaces)
		attackingHorsePlaces = self.horse.attackingPlaces(x, y)
		attackingRookPlaces = self.rook.attackingPlaces(True, x, y)
		attackingBishopPlaces = self.bishop.attackingPlaces(True, x, y)
		queen1 = self.rook.attackingPlaces(False, x, y)
		queen2 = self.bishop.attackingPlaces(False, x, y)
		attackingQueenPlaces = queen1 + queen2
		attackingPlaces = attackingPawnPlaces + attackingHorsePlaces + attackingRookPlaces + attackingBishopPlaces + attackingQueenPlaces
		# print("Checker getter from place full array %s"%attackingPlaces)
		return attackingPlaces

	def placeHasCheck(self, placeId):
		attackingPlaces = self.fromPlace(placeId)
		# print("Checker getter placeHasCheck %s"%attackingPlaces)
		if len(attackingPlaces) > 0:
			return True
		
		return False
	
	
	def kingHasCheck(self):
		attackingPlaces = self.fromPiece()
		if len(attackingPlaces) > 0:
			return True
		
		return False
	
	# checks if the path to the left of the king to the rook is bieng checked for castling
	def toLeftRookHasCheck(self):
		toLeftRookPlaces = ["8F", "8G"]
		if self.placeHasCheck(toLeftRookPlaces[0]):
			return True
		
		if self.placeHasCheck(toLeftRookPlaces[1]):
			return True
		
		return False
	
	# checks if the path to the right of the king to the rook is bieng checked for castling
	def toRightRookHasCheck(self):
		toRightRookPlaces = ["8D", "8C", "8B"];
		if self.placeHasCheck(toRightRookPlaces[0]):
			return True
		
		if self.placeHasCheck(toRightRookPlaces[1]):
			return True
		
		if self.placeHasCheck(toRightRookPlaces[2]):
			return True
		
		return False

	# checks if the right rook is bieng checked for castling
	def rightRookHasCheck(self):
		if self.placeHasCheck("8H"):
			return True
		
		return False
	
	# checks if the left rook is bieng checked for castling
	def leftRookHasCheck(self):
		if self.placeHasCheck("8A"):
			return True
		
		return False

	# returns only positions that are not under check that the king can immediately move to
	def carefullKing(self, kingArray):
		newArray = [] 
		for i in range(len(kingArray)):
			next_val = kingArray[i]
			if not self.placeHasCheck(next_val):
				newArray.append(next_val)
			 
		return newArray
	
	
	
