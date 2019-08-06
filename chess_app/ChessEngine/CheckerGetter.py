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


	# Gets all the places that could be moved to to save the king
	def getPlacesUnderCheck(self):
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
		
		if len(attackingRookPlaces) != 0:
			for i in range(len(attackingRookPlaces)):
				attackingPlaces = attackingPlaces + self.getAttackingRookInbetweenPlaces(attackingRookPlaces[i], x, y)

		if len(queen1) != 0:
			for j in range(len(queen1)):
				attackingPlaces = attackingPlaces + self.getAttackingRookInbetweenPlaces(queen1[j], x, y)
				print("get places under check %s"%self.getAttackingRookInbetweenPlaces(queen1[j], x, y))

		if len(attackingBishopPlaces) != 0:
			for k in range(len(attackingBishopPlaces)):
				attackingPlaces = attackingPlaces + self.getAttackingBishopInbetweenPlaces(attackingBishopPlaces[k], x, y)

		if len(queen2) != 0:
			for m in range(len(queen2)):
				attackingPlaces = attackingPlaces + self.getAttackingBishopInbetweenPlaces(queen2[m], x, y)

		return attackingPlaces

	# Gets the attacking pieces between the rooks if there are any
	def getAttackingRookInbetweenPlaces(self, placeId, x, y):
		coordinates = self.chess_piece.findPlaceCoordinates(placeId)
		new_x = coordinates[1]
		new_y = coordinates[0]
		new_array = []
		

		down_next_y = new_y
		up_next_y = new_y
		right_next_x = new_x
		left_next_x = new_x
		if new_x == x:
			for i in range(8):
				if new_y > y:
					down_next_y = down_next_y - 1
					if down_next_y != y:
						down_next_place = self.chess_piece.id_gen(down_next_y, x)
						# print("get attacking rook inbetween %s %s"%(self.chess_piece.id_gen(down_next_y, x), self.chess_piece.id_gen(y, x)))
						new_array.append(down_next_place)
					else:
						break

				elif new_y < y:
					up_next_y = up_next_y + 1
					if up_next_y != y:
						up_next_place = self.chess_piece.id_gen(up_next_y, x)
						new_array.append(up_next_place)
					else:
						break
				else:
					break

		elif new_y == y:
			for j in range(8):
				if new_x > x:
					left_next_x = left_next_x - 1
					if left_next_x != x:
						left_next_place = self.chess_piece.id_gen(y, left_next_x)
						new_array.append(left_next_place)
					else:
						break
						
				elif new_x < x:
					right_next_x = right_next_x + 1
					if right_next_x != x:
						right_next_place = self.chess_piece.id_gen(y, right_next_x)
						new_array.append(right_next_place)
					else:
						break
				else:
					break

		return new_array

	# Gets the attacking places inbetween the bishop and the king
	def getAttackingBishopInbetweenPlaces(self, placeId, x, y):
		coordinates = self.chess_piece.findPlaceCoordinates(placeId)
		new_x = coordinates[1]
		new_y = coordinates[0]
		new_array = []

		right_down_next_x = new_x
		right_down_next_y = new_y
		right_up_next_x = new_x
		right_up_next_y = new_y
		left_down_next_x = new_x
		left_down_next_y = new_y
		left_up_next_x = new_x
		left_up_next_y = new_y
		if new_x > x and new_y > y:
			for i in range(8):

				right_down_next_x = right_down_next_x - 1
				right_down_next_y = right_down_next_y - 1
				if right_down_next_x != x and right_down_next_y != y:
					right_down_next_place = self.chess_piece.id_gen(right_down_next_y, right_down_next_x)
					new_array.append(right_down_next_place)
				else:
					break

		elif new_x > x and new_y < y:
			for j in range(8):

				right_up_next_x = right_up_next_x - 1
				right_up_next_y = right_up_next_y + 1
				if right_up_next_x != x and right_up_next_y != y:
					right_up_next_place = self.chess_piece.id_gen(right_up_next_y, right_up_next_x)
					new_array.append(right_up_next_place)
				else:
					break
					
		elif new_x < x and new_y > y:
			for k in range(8):

				left_down_next_x = left_down_next_x + 1
				left_down_next_y = left_down_next_y - 1
				if left_down_next_x != x and left_down_next_y != y:
					left_down_next_place = self.chess_piece.id_gen(left_down_next_y, left_down_next_x)
					new_array.append(left_down_next_place)
				else:
					break
					
		elif new_x < x and new_y < y:
			for m in range(8):

				left_up_next_x = left_up_next_x + 1
				left_up_next_y = left_up_next_y + 1
				if left_up_next_x != x and left_up_next_y != y:
					left_up_next_place = self.chess_piece.id_gen(left_up_next_y, left_up_next_x)
					new_array.append(left_up_next_place)
				else:
					break
					
		return new_array
	

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
	
	
	
