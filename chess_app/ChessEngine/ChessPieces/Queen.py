from ChessPiece import ChessPiece
from chess_app.ChessEngine.Selecter import Select 

class Queen(ChessPiece):
	
	def __init__(self):
		super(Queen, self).__init__()

	def movablePlaces(self, x, y):
		return self.shrinkContinuosArray(self.getQueenMovablePlaces(x, y))

	def getQueenMovablePlaces(self, x, y):
		rookPlaces = self.getRookMovablePlaces(x, y)
		bishopPlaces = self.getBishopMovablePlaces(x, y)
		place_ids = rookPlaces + bishopPlaces
		
		return place_ids

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
	
	def getRookMovablePlaces(self, x, y):
		matrix = self.live_chessboard_matrix
		placeIds = []
		left = ["" for a in range(8)]
		right = ["" for b in range(8)]
		up = ["" for c in range(8)]
		down = ["" for d in range(8)]
		rightCounter = 0
		downCounter = 0

		if x >= 0 and x <= 7 and y >= 0 and y <= 7:

			#Going Left
			for i in range(7, -1, -1):
				if i < x:
					rightSelect = Select()
					nextElement = rightSelect.selectFromParentId(matrix, self.id_gen(y, i))
					if nextElement.parent_id != None:
						right[rightCounter] = nextElement.parent_id
						if nextElement.piece_id != "" and nextElement.piece_id != None:
							break
						rightCounter = rightCounter + 1
					
	

			#Going Right
			for j in range(8):
				if j > x:
					leftSelect = Select()
					nextElement = leftSelect.selectFromParentId(matrix, self.id_gen(y, j))
					if nextElement.parent_id != None:
						left[j] = nextElement.parent_id
						if nextElement.piece_id != "" and nextElement.piece_id != None:
							break
					

			#Going Down
			for k in range(8):
				if k > y:
					upSelect = Select()
					nextElement = upSelect.selectFromParentId(matrix, self.id_gen(k, x))
					if nextElement.parent_id != None:
						up[k] = nextElement.parent_id
						if nextElement.piece_id != "" and nextElement.piece_id != None:
							break
					
					
				
			#Going Up
			for n in range(7, -1, -1):
				if n < y:
					downSelect = Select()
					nextElement = downSelect.selectFromParentId(matrix, self.id_gen(n, x))
					if nextElement.parent_id != None:
						down[downCounter] = nextElement.parent_id
						if nextElement.piece_id != "" and nextElement.piece_id != None:
							break
						downCounter = downCounter + 1
				
					
				
		left = self.moveArrayToBack(left)
		right = self.moveArrayToBack(right)
		up = self.moveArrayToBack(up)
		down = self.moveArrayToBack(down)

		horizontal = left + right
		vertical = up + down
		placeIds = horizontal + vertical
	
		return placeIds





	