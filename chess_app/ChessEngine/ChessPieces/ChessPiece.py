class ChessPiece(object):
	
	def __init__(self):
		self.live_chessboard_matrix = None

	# Move the items in the array to the end  of array of 
	# size 8 so continious movements like rook can be searched in 8's
	def moveArrayToBack(self, array):
		rem_length = 8 - len(array)
		rem_counter = 0
		new_array = ["" for x in range(8)]
		for i in range(8): 
			if (rem_counter<rem_length):
				new_array[i] = ""
				rem_counter = rem_counter + 1
			else:
				new_array[i] = array[i-rem_length];
		return new_array

	# shrinks movements so there are no gaps and it is selectable
	def shrinkContinuosArray(self, array):
		new_array = []
		for i in range(len(array)):
			next_val = array[i]
			
			if(next_val!=None):
				if(next_val!=""):
					new_array.append(next_val)
				
		return new_array

	def first_coordinate_gen(self, fstAttr):
		row_num = 8 - (int(fstAttr))
		return row_num

	def second_coordinate_gen(self, secAttr):
		col_num = ord(secAttr) - 65
		return col_num

	# uses the place position id and gives the coordinates of that place
	def findPlaceCoordinates(self, parent_id):
		fstAttr = self.first_coordinate_gen(int(parent_id[0]))
		secAttr = self.second_coordinate_gen(parent_id[1])
		coordinates = [fstAttr, secAttr]
		
		return coordinates
	
	# checks if one string is the similar to another for piece types and comp vs player types
	def isType(self, pieceId, target_piece):
		new_target_piece = target_piece

		for j in range(len(pieceId)):
			if pieceId[j]==new_target_piece[0]:
				new_target_piece = new_target_piece[1:]
			
			if new_target_piece=="":
				return True
	
		return False


	def id_gen(self, row_num, col_num):
		secAttr = chr(65 + col_num)
		fstAttr = 8 - (row_num)
		chess_id = str(fstAttr) + str(secAttr)
		
		return chess_id

	# compares 2 matrices to see if there the same if not can do an action
	def matrixSame(self, matrix1, matrix2):
		for i in range(len(matrix1)):
			for j in range(len(matrix1[i])):
				if matrix1[i][j] != matrix2[i][j]:
					return False;
			
		return True

	# finds a single different piece if 2 matrices are not the same to make a movement
	def findDiffentPiece(self, live_matrix, new_matrix):
		for i in range(len(live_matrix)):
			for j in range(len(live_matrix[i])):
				if live_matrix[i][j] != new_matrix[i][j]:
					if live_matrix[i][j] != None:
						return live_matrix[i][j]
					elif new_matrix[i][j] != None:
						return new_matrix[i][j]
	
		return ""

	# finds all the different pieces for testing positioning movement
	def findMultipleDifferentPieces(self, live_matrix, new_matrix):
		new_array = []

		for i in range(len(live_matrix)):
			for j in range(len(live_matrix[i])):
				if live_matrix[i][j] != new_matrix[i][j]:
					if live_matrix[i][j] != None:
						new_array.append(live_matrix[i][j])
					elif new_matrix[i][j] != None:
						new_array.append(new_matrix[i][j])
					
		return new_array;

	# finds the coordinates of a piece in a matrix
	def findBoardCoordinates(self, new_matrix, value):
		for i in range(len(new_matrix)):
			for j in range(len(new_matrix[i])):
				if new_matrix[i][j] == value and value != "":
					return [i, j]
		
		return []
	
	# finds coordintaes of a selcted piece if it exists
	def findPieceCoordinates(self, select):
		if select != None:
			parent_id = select.parent_id
			fstAttr = self.first_coordinate_gen(int(parent_id[0]))
			secAttr =  self.second_coordinate_gen(parent_id[1])
			coordinates = [fstAttr, secAttr]
			return coordinates

	# returns a matrix based on place ands and piece ids given in order so that the live chessboard can be setup
	def live_chessboard_matrix_gen(self, place_ids, piece_ids):
		place_coordinates = []
		live_matrix = [
			[ "", "", "", "", "", "", "", ""],
			[ "", "", "", "", "", "", "", ""],
			[ "", "", "", "", "", "", "", ""],
			[ "", "", "", "", "", "", "", ""],
			[ "", "", "", "", "", "", "", ""],
			[ "", "", "", "", "", "", "", ""],
			[ "", "", "", "", "", "", "", ""],
			[ "", "", "", "", "", "", "", ""]
		]
		
		for i in range(len(place_ids)):
			fstAttr = self.first_coordinate_gen(int(place_ids[i][0]))
			secAttr = self.second_coordinate_gen(place_ids[i][1])
			place_coordinates.append([fstAttr, secAttr])
			current_piece = piece_ids[i]
			current_place = place_coordinates[i]
			live_matrix[current_place[0]][current_place[1]] = current_piece
		
		return live_matrix
	
	
	
	
	
