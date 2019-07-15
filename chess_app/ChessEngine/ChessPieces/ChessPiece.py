class ChessPiece(object):
	
	def __init__(self):
		self.live_chessboard_matrix = None

	def moveArrayToBack(self, array):
		rem_length = 8 - len(array)
		rem_counter = 0
		new_array = ["" for x in range(8)]
		print("array length: %s"%len(new_array))
		for i in range(8): 
			if (rem_counter<rem_length):
				new_array[i] = ""
				rem_counter = rem_counter + 1
			else:
				new_array[i] = array[i-rem_length];
		
		return new_array

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

	def findPlaceCoordinates(self, parent_id):
		fstAttr = self.first_coordinate_gen(int(parent_id[0]))
		secAttr = self.second_coordinate_gen(parent_id[1])
		coordinates = [fstAttr, secAttr]
		
		return coordinates
	
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


	
	
	
