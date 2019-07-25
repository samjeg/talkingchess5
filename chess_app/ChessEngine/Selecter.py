from ChessPieces.ChessPiece import ChessPiece

class Select(object):

	def __init__(self):
		self.piece_id = ""
		self.parent_id = ""
		self.chess_piece = ChessPiece()

	def selectFromParentId(self, matrix, par_id):
		self.parent_id = par_id
		coordinates = self.chess_piece.findPlaceCoordinates(par_id)
		self.piece_id = matrix[coordinates[0]][coordinates[1]]

	def selectFromPieceId(self, matrix, p_id):
		self.piece_id = p_id

		for i in range(len(matrix)):
			for j in range(len(matrix[i])):
				if matrix[i][j] == p_id:
					firstCoor = i
					secCoor = j
					coordinates = [i, j]
					self.parent_id = self.chess_piece.id_gen(i, j)
