from ChessPiece import ChessPiece
from chess_app.ChessEngine.Selecter import Select 

class Horse(ChessPiece):
	
	def __init__(self):
		super(Horse, self).__init__()

	# gets all the possible positions that can moved by the horse
	def movablePlaces(self, x, y):
		matrix = self.live_chessboard_matrix
		placeIds = []
		if x >= 0 and x <= 7 and y >= 0 and y <= 7:
			select1 = Select()
			topThenRightElement = select1.selectFromParentId(matrix ,self.id_gen(y+2, x-1))
			select2 = Select()
			topThenLeftElement = select2.selectFromParentId(matrix ,self.id_gen(y+2, x+1))
			select3 = Select()
			bottomThenRightElement = select3.selectFromParentId(matrix ,self.id_gen(y-2, x+1))
			select4 = Select()
			bottomThenLeftElement = select4.selectFromParentId(matrix ,self.id_gen(y-2, x-1))
			select5 = Select()
			rightThenTopElement = select5.selectFromParentId(matrix ,self.id_gen(y+1, x-2))
			select6 = Select()
			rightThenBottomElement = select6.selectFromParentId(matrix ,self.id_gen(y-1, x-2))
			select7 = Select()
			leftThenTopElement = select7.selectFromParentId(matrix ,self.id_gen(y+1, x+2))
			select8 = Select()
			leftThenBottomElement = select8.selectFromParentId(matrix ,self.id_gen(y-1, x+2))
			
			if topThenRightElement.parent_id != None and topThenRightElement.parent_id != "":
				if not self.isType(topThenRightElement.piece_id, "comp_"):
					placeIds.append(topThenRightElement.parent_id)	
			
			if topThenLeftElement.parent_id != None and topThenLeftElement.parent_id != "": 
				if not self.isType(topThenLeftElement.piece_id, "comp_"):
					placeIds.append(topThenLeftElement.parent_id)		
			
			if bottomThenRightElement.parent_id != None and bottomThenRightElement.parent_id != "":
				if not self.isType(bottomThenRightElement.piece_id, "comp_"):
					placeIds.append(bottomThenRightElement.parent_id)
			
			if bottomThenLeftElement.parent_id != None and bottomThenLeftElement.parent_id != "":
				if not self.isType(bottomThenLeftElement.piece_id, "comp_"):
					placeIds.append(bottomThenLeftElement.parent_id)
			
			if rightThenTopElement.parent_id != None and rightThenTopElement.parent_id != "":
				if not self.isType(rightThenTopElement.piece_id, "comp_"):
					placeIds.append(rightThenTopElement.parent_id)
			
			if rightThenBottomElement.parent_id != None and rightThenBottomElement.parent_id != "":
				if not self.isType(rightThenBottomElement.piece_id, "comp_"):
					placeIds.append(rightThenBottomElement.parent_id)
			
			if leftThenTopElement.parent_id != None and leftThenTopElement.parent_id != "":
				if not self.isType(leftThenTopElement.piece_id, "comp_"):
					placeIds.append(leftThenTopElement.parent_id)
			
			if leftThenBottomElement.parent_id != None and leftThenBottomElement.parent_id != "":
				if not self.isType(leftThenBottomElement.piece_id, "comp_"):
					placeIds.append(leftThenBottomElement.parent_id)
			
		
		return placeIds
	
	# checkes if a position is being attcked by the horse
	def attackingPlaces(self, x, y):
		matrix = self.live_chessboard_matrix
		horseMovablePlaces = self.movablePlaces(x, y)
		attackingHorsePlaces = []
		
		for i in range(len(horseMovablePlaces)):
			attackingSelect = Select()
			next_val = attackingSelect.selectFromParentId(matrix, horseMovablePlaces[i])
			
			if next_val!=None:
				if next_val.piece_id != 0 or next_val.piece_id != None:
					if self.isType(next_val.piece_id, "player_horse"):
							attackingHorsePlaces.append(next_val.parent_id)
						
					
		return attackingHorsePlaces
	
