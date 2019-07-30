from .ChessPieces.ChessPiece import ChessPiece

class Select(object):

	def __init__(self):
		self.piece_id = ""
		self.parent_id = ""
		self.chess_piece = ChessPiece()

	# create select from the parent id object with piece and parent id replaces getElementById in javascript frontend
	def selectFromParentId(self, matrix, par_id):
		# print("select %s"%par_id)
		coordinates = self.chess_piece.findPlaceCoordinates(par_id)
		if coordinates[0] >= 0 and coordinates[0] <= 7 and coordinates[1] >= 0 and coordinates[1] <= 7:
			self.parent_id = par_id
			self.piece_id = matrix[coordinates[0]][coordinates[1]]

		return self


	# create select from the piece id object with piece and parent id replaces getElementById in javascript frontend
	def selectFromPieceId(self, matrix, p_id):
		for i in range(len(matrix)):
			for j in range(len(matrix[i])):
				if matrix[i][j] == p_id:
					self.piece_id = p_id
					firstCoor = i
					secCoor = j
					coordinates = [i, j]
					self.parent_id = self.chess_piece.id_gen(i, j)

		return self

	# sets a position in a matrix to empty used for removing a piece from the live matrix
	def removePiece(self, matrix, par_id):
		coordinates = self.chess_piece.findPlaceCoordinates(par_id)
		if coordinates[0] >= 0 and coordinates[0] <= 7 and coordinates[1] >= 0 and coordinates[1] <= 7:
			matrix[coordinates[0]][coordinates[1]] = ""


	# sets a position in a matrix to the given piece id used in moving pieces
	def appendPiece(self, matrix, p_id, par_id):
		coordinates = self.chess_piece.findPlaceCoordinates(par_id)
		if coordinates[0] >= 0 and coordinates[0] <= 7 and coordinates[1] >= 0 and coordinates[1] <= 7:
			matrix[coordinates[0]][coordinates[1]] = p_id