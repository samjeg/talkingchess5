from ChessPiece import ChessPiece
from chess_app.ChessEngine.Selecter import Select


class King(ChessPiece):

	def __init__(self):
		super(King, self).__init__()

	# gets all the possible positions that can moved by the king without special moves and seeing if the position is bieng checked
	def getKingMovablePlaces(self, x, y):
		matrix = self.live_chessboard_matrix;
		placeIds = []
		if x >= 0 and x <= 7 and y >= 0 and y <= 7:
			rightBkwdSelect = Select()
			rightBkwdElement = rightBkwdSelect.selectFromParentId(matrix, self.id_gen(y-1, x-1))
			leftBkwdSelect = Select()
			leftBkwdElement = leftBkwdSelect.selectFromParentId(matrix, self.id_gen(y-1, x+1))
			rightFwdSelect = Select()
			rightFwdElement = rightFwdSelect.selectFromParentId(matrix, self.id_gen(y+1, x-1))
			leftFwdSelect = Select()
			leftFwdElement = leftFwdSelect.selectFromParentId(matrix, self.id_gen(y+1, x+1))
			bkwdSelect = Select()
			bkwdElement = bkwdSelect.selectFromParentId(matrix, self.id_gen(y-1, x))
			fwdSelect = Select()
			fwdElement = fwdSelect.selectFromParentId(matrix, self.id_gen(y+1, x))
			leftSelect = Select()
			leftElement = leftSelect.selectFromParentId(matrix, self.id_gen(y, x+1))
			rightSelect = Select()
			rightElement = rightSelect.selectFromParentId(matrix, self.id_gen(y, x-1))

			if fwdElement.parent_id != None and fwdElement.parent_id != "":
				placeIds.append(fwdElement.parent_id)
			
			if bkwdElement.parent_id != None and  bkwdElement.parent_id != "":
				placeIds.append(bkwdElement.parent_id)
			
			if rightElement.parent_id != None and rightElement.parent_id != "":
				placeIds.append(rightElement.parent_id);
			
			if leftElement.parent_id != None and leftElement.parent_id != "":
				placeIds.append(leftElement.parent_id);
			
			if leftBkwdElement.parent_id != None and leftBkwdElement.parent_id != "":
				placeIds.append(leftBkwdElement.parent_id);
			
			if leftFwdElement.parent_id != None and leftFwdElement.parent_id != "":
				placeIds.append(leftFwdElement.parent_id)
			
			if rightBkwdElement.parent_id != None and rightBkwdElement.parent_id != "":
				placeIds.append(rightBkwdElement.parent_id)
			
			if rightFwdElement.parent_id != None and rightFwdElement.parent_id != "":
				placeIds.append(rightFwdElement.parent_id)
		
		return placeIds

	def kingHasMoved(self, movedPieces):
		for i in range(len(movedPieces)):
			next_val = movedPieces[i]
			if self.isType(next_val, "comp_king"):
				return True
		
		return False
	
	



