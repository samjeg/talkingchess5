from ChessPiece import ChessPiece
from chess_app.ChessEngine.Selecter import Select 

class Bishop(ChessPiece):
	
	def __init__(self):
		super(Bishop, self).__init__()

	def movablePlaces(self, x, y):
		return self.shrinkContinuosArray(self.getBishopMovablePlaces(x, y))

	def getBishopMovablePlaces(self, x, y):
		matrix = self.live_chessboard_matrix
		placeIds = []
		leftUp = ["" for a in range(8)]
		rightUp = ["" for b in range(8)]
		leftDown = ["" for c in range(8)]
		rightDown = ["" for d in range(8)]
		
		if x >= 0 and x <= 7 and y >= 0 and y <= 7:
			
			for i in range(8):
				b_x = x - i
				b_y = y - i
				
				if b_x <= 7 and b_x >= 0 and b_y <= 7 and b_y >= 0:
					if b_x < x and b_y < y:
						rightDownSelect = Select()
						nextElement = rightDownSelect.selectFromParentId(matrix, self.id_gen(b_y, b_x))
						
						if nextElement.parent_id != None:
							rightDown[i] = nextElement.parent_id
							if nextElement.piece_id != "" and nextElement.piece_id != None:
								break
									
					
			for j in range(8):
				b_x = x + j
				b_y = y - j
				
				if b_x <= 7 and b_x >= 0 and b_y <= 7 and b_y >= 0:
					if b_x > x and b_y < y:
						leftDownSelect = Select()
						nextElement = leftDownSelect.selectFromParentId(matrix, self.id_gen(b_y, b_x))
						
						if nextElement.parent_id != None:
							leftDown[j] = nextElement.parent_id
							if nextElement.piece_id != "" and nextElement.piece_id != None:
								break
							
			for k in range(8):
				b_x = x - k
				b_y = y + k
				
				if b_x <= 7 and b_x >= 0 and b_y <= 7 and b_y >= 0:
					if b_x < x and b_y > y:
						rightUpSelect = Select()
						nextElement = rightUpSelect.selectFromParentId(matrix, self.id_gen(b_y, b_x))
						
						if nextElement.parent_id!= None:
							rightUp[k] = nextElement.parent_id
							if nextElement.piece_id != "" and nextElement.piece_id != None:
								break						
					
			for n in range(8):
				b_x = x + n
				b_y = y + n
				
				if b_x <= 7 and b_x >= 0 and b_y <= 7 and b_y >= 0:
					if b_x > x and b_y > y:
						leftUpSelect = Select()
						nextElement = leftUpSelect.selectFromParentId(matrix, self.id_gen(b_y, b_x))
						
						if nextElement.parent_id!= None:
							leftUp[n] = nextElement.parent_id
							if nextElement.piece_id != "" and nextElement.piece_id != None:
								break
					
		leftUp = self.moveArrayToBack(leftUp)
		rightUp = self.moveArrayToBack(rightUp)
		leftDown = self.moveArrayToBack(leftDown)
		rightDown = self.moveArrayToBack(rightDown)
		
		leftToRight = leftDown + rightUp
		rightToLeft = rightDown + leftUp
		placeIds = leftToRight + rightToLeft
		
		return placeIds
	

	def attackingPlaces(self, isBishop, x, y):
		attackingBishopPlaces = self.getBishopMovablePlaces(x, y)
		RightDownAttacking = attackingBishopPlaces[23]
		LeftUpAttacking = attackingBishopPlaces[31]
		LeftDownAttacking = attackingBishopPlaces[7]
		RightUpAttacking = attackingBishopPlaces[15]
		newAttackingBishopPlaces = []
		if isBishop == True:
			self.getAttackingPiecesPlaces(RightDownAttacking, newAttackingBishopPlaces, "player_bishop", "")
			self.getAttackingPiecesPlaces(LeftUpAttacking, newAttackingBishopPlaces, "player_bishop", "")
			self.getAttackingPiecesPlaces(LeftDownAttacking, newAttackingBishopPlaces, "player_bishop", "")
			self.getAttackingPiecesPlaces(RightUpAttacking, newAttackingBishopPlaces, "player_bishop", "")
		else: 
			self.getAttackingPiecesPlaces(RightDownAttacking, newAttackingBishopPlaces, "", "player_queen")
			self.getAttackingPiecesPlaces(LeftUpAttacking, newAttackingBishopPlaces, "", "player_queen")
			self.getAttackingPiecesPlaces(LeftDownAttacking, newAttackingBishopPlaces, "", "player_queen")
			self.getAttackingPiecesPlaces(RightUpAttacking, newAttackingBishopPlaces, "", "player_queen")
		
		return newAttackingBishopPlaces
	

	def getAttackingPiecesPlaces(self, placeId, array, type1, type2):
		matrix = self.live_chessboard_matrix
		piece_type = type1
		if type1 == "":
			piece_type = type2
		
		if placeId != "":
			typeSelect = Select()
			nextPlace = typeSelect.selectFromParentId(matrix, placeId)
			
			if nextPlace.piece_id != None and nextPlace.piece_id != "":
				nextPiece = nextPlace.piece_id
				if self.isType(nextPiece, piece_type):
					array.append(placeId)
				
