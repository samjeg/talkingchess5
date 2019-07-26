from ChessPiece import ChessPiece
from chess_app.ChessEngine.Selecter import Select 

class Rook(ChessPiece):
	
	def __init__(self):
		super(Rook, self).__init__()

	def movablePlaces(self, x, y):
		return self.shrinkContinuosArray(self.getRookMovablePlaces(x, y))
	

	def getRookMovablePlaces(self, x, y):
		matrix = self.live_chessboard_matrix
		placeIds = []
		left = []
		right = []
		up = []
		down = []
		leftCounter = 0
		upCounter = 0

		if x >= 0 and x <= 7 and y >= 0 and y <= 7:

			#Going Left
			for i in range(7, -1, -1):
				if i < x:
					leftSelect = Select()
					nextElement = leftSelect.selectFromParentId(matrix, self.id_gen(y, i))
					if nextElement.parent_id != None:
						left.append(nextElement.parent_id)
						if nextElement.piece_id != "" and nextElement.piece_id != None:
							break
	

			#Going Right
			for j in range(8):
				if j > x:
					rightSelect = Select()
					nextElement = rightSelect.selectFromParentId(matrix, self.id_gen(y, j))
					if nextElement.parent_id != None:
						right.append(nextElement.parent_id)
						if nextElement.piece_id != "" and nextElement.piece_id != None:
							break
					

			#Going Down
			for k in range(8):
				if k > y:
					downSelect = Select()
					nextElement = downSelect.selectFromParentId(matrix, self.id_gen(k, x))
					if nextElement.parent_id != None:
						down.append(nextElement.parent_id)
						if nextElement.piece_id != "" and nextElement.piece_id != None:
							break
					
				
			

			#Going Up
			for n in range(7, -1, -1):
				if n < y:
					upSelect = Select()
					nextElement = upSelect.selectFromParentId(matrix, self.id_gen(n, x))
					if nextElement.parent_id != None:
						up.append(nextElement.parent_id)
						if nextElement.piece_id != "" and nextElement.piece_id != None:
							break
					
				
			
		
		
		left = self.moveArrayToBack(left)
		right = self.moveArrayToBack(right)
		up = self.moveArrayToBack(up)
		down = self.moveArrayToBack(down)

		horizontal = left + right
		vertical = up + down
		placeIds = horizontal + vertical
		# // console.log("Rook Place Ids: "+placeIds)
	
		return placeIds
	

	# placeHasCheck(placeId){
	# 	attackingPlaces = self.checkerGetter.fromPlace(placeId)
	# 	if(attackingPlaces.length>0){
	# 		return true
	# 	}
	# 	return false
	# }

	def rightRookHasMoved(self, movedPieces):
		for i in range(len(movedPieces)):
			next_val = movedPieces[i]
			if self.isType(next_val, "player_rook2"):
				return True
			
		return False
	

	def leftRookHasMoved(movedPieces):
		for i in range(len(movedPieces)):
			next_val = movedPieces[i]
			if self.isType(next_val, "player_rook1"):
				return True
		
		return False
	

	def toRightRookHasPieces(self):
		matrix = self.live_chessboard_matrix
		toRightRookPlaces = ["1F", "1G"]
		
		rightRookSelect1 = Select()
		first = rightRookSelect1.selectFromParentId(matrix, toRightRookPlaces[0])
		if first.parent_id != None:
			if first.piece_id != None and first.piece_id != "":
				return True
		
		rightRookSelect2 = Select()
		second = rightRookSelect2.selectFromParentId(matrix, toRightRookPlaces[1])
		if second.parent_id != None:
			if second.piece_id != None and second.piece_id != "":
				return True
			
		return False
	

	def toLeftRookHasPieces(self):
		matrix = self.live_chessboard_matrix
		toLeftRookPlaces = ["1D", "1C", "1B"]
		
		leftRookSelect1 = Select()		
		first = leftRookSelect1.selectFromParentId(matrix, toLeftRookPlaces[0])
		if first.parent_id != None:
			if first.piece_id != None and first.piece_id != "":
				return True

		leftRookSelect2 = Select()
		second = leftRookSelect2.selectFromParentId(matrix, toLeftRookPlaces[1])
		if second.parent_id != None:
			if second.piece_id != None and second.piece_id != "":
				return True

		leftRookSelect3 = Select()
		third = leftRookSelect3.selectFromParentId(matrix, toLeftRookPlaces[2])
		if third.parent_id != None:
			if third.piece_id != None and third.piece_id != "":
				return True

		return False
		

	def attackingPlaces(self, isRook, x, y):
		attackingRookPlaces = self.getRookMovablePlaces(x, y)
		rookFwdAttacking = attackingRookPlaces[23]
		rookBkwdAttacking = attackingRookPlaces[31]
		rookRightAttacking = attackingRookPlaces[7]
		rookLeftAttacking = attackingRookPlaces[15]
		newAttackingRookPlaces = []
		if isRook == True:
			self.getAttackingPiecesPlaces(rookFwdAttacking, newAttackingRookPlaces, "comp_rook", "")
			self.getAttackingPiecesPlaces(rookBkwdAttacking, newAttackingRookPlaces, "comp_rook", "")
			self.getAttackingPiecesPlaces(rookRightAttacking, newAttackingRookPlaces, "comp_rook", "")
			self.getAttackingPiecesPlaces(rookLeftAttacking, newAttackingRookPlaces, "comp_rook", "")
		else:
			self.getAttackingPiecesPlaces(rookFwdAttacking, newAttackingRookPlaces, "", "comp_queen")
			self.getAttackingPiecesPlaces(rookBkwdAttacking, newAttackingRookPlaces, "", "comp_queen")
			self.getAttackingPiecesPlaces(rookRightAttacking, newAttackingRookPlaces, "", "comp_queen")
			self.getAttackingPiecesPlaces(rookLeftAttacking, newAttackingRookPlaces, "", "comp_queen")
		
		return newAttackingRookPlaces
	

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
				
			
		
	