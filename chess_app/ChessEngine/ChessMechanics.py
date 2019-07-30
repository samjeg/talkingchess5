from .Selecter import Select 
from .CheckerGetter import CheckerGetter 
from ChessPieces.ChessPiece import ChessPiece
from ChessPieces.Pawn import Pawn
from ChessPieces.King import King
from ChessPieces.Queen import Queen
from ChessPieces.Rook import Rook
from ChessPieces.Bishop import Bishop
from ChessPieces.Horse import Horse

class ChessMechanics(object):
	
	def __init__(self):
		self.current_selected_piece = None
		self.current_selected_coordinates = ["" for a in range(2)]
		self.current_selected_movable_ids = []
		self.king_piece = None
		self.king_coordinates = []
		self.kingInCheck = False
		self.movedPieces = []
		self.kingMovedRight = False
		self.kingMovedLeft = False
		self.playerPawnStartingPositions = ["" for a in range(8)]
		self.compPawnStartingPositions = ["" for a in range(8)]
		self.playerPawnsHasMoved = ["" for a in range(8)]
		self.compPawnsHasMoved = ["" for a in range(8)]
		self.enPassantOpponentLeft = ""
		self.enPassantOpponentRight = ""
		self.currentEnPassantOpponentPlaceId = ""
		self.currentEnPassantPlaceId = ""
		self.selectedHighlights = []
		self.selectedHighlightMovableIds = []
		self.canMovePawn = False
		self.isEnPassant = False
		self.checkerGetter = CheckerGetter()
		self.chessPiece = ChessPiece()
		self.rook = Rook()
		self.bishop = Bishop()
		self.queen = Queen()
		self.king = King()
		self.pawn = Pawn()
		self.horse = Horse()

	# allows the comp to select a piece to play
	def select(self, pieceId):
		matrix = self.chessPiece.live_chessboard_matrix
		self.prevSelectedHighlightIds = self.current_selected_movable_ids
		currentSelect = Select()
		self.current_selected_piece = currentSelect.selectFromPieceId(matrix, pieceId)
		self.rook.live_chessboard_matrix = self.chessPiece.live_chessboard_matrix
		self.bishop.live_chessboard_matrix = self.chessPiece.live_chessboard_matrix
		self.queen.live_chessboard_matrix = self.chessPiece.live_chessboard_matrix
		self.king.live_chessboard_matrix = self.chessPiece.live_chessboard_matrix
		self.pawn.live_chessboard_matrix = self.chessPiece.live_chessboard_matrix
		self.horse.live_chessboard_matrix = self.chessPiece.live_chessboard_matrix
		self.current_selected_coordinates = self.chessPiece.findPieceCoordinates(self.current_selected_piece)
		self.currentEnPassantOpponentPlaceId = ""
		
		self.current_selected_movable_ids = self.getMovable(
			self.current_selected_piece.piece_id,
			self.current_selected_coordinates[1],
			self.current_selected_coordinates[0]
		)

		current_king_place_id_select = Select()
		current_king_place_id = current_king_place_id_select.selectFromPieceId(matrix, "player_king").parent_id


	def canCastleRight(self):
		if  all( [
			not self.king.kingHasMoved(self.movedPieces),
			not self.checkerGetter.kingHasCheck(),
			not self.rook.rightRookHasMoved(self.movedPieces),
			not self.checkerGetter.toRightRookHasCheck(),
			not self.rook.toRightRookHasPieces() 
		]):
			return True
		
		return False
	

	def canCastleLeft(self):
		if all([
			not self.king.kingHasMoved(self.movedPieces),
			not self.checkerGetter.kingHasCheck(),
			not self.rook.leftRookHasMoved(self.movedPieces),
			not self.checkerGetter.toLeftRookHasCheck(),
			not self.rook.toLeftRookHasPieces()
		]):
			return True
		
		return False

	# gives castling moves if kingCanCastle functions are true
	def kingExtraMoves(self, kingArray):
		if self.canCastleRight():
			kingArray.append("1G")
			
		if self.canCastleLeft():
			kingArray.append("1C")
		
		return kingArray
	
	# gives castling moves if the king has initiated a castling move
	def rookExtraMoves(self, rookArray):
		if self.kingMovedRight:
			rookArray.append("1F")
		
		if self.kingMovedLeft:
			rookArray.append("1D")
		
		return rookArray

	# gets all posible moves depending on the piece and the circumstance that a chesspiece can make
	def getMovable(self, pieceId, x, y):
		movablePlaces = []
		if self.chessPiece.isType(pieceId, "pawn"):
			movablePlaces = self.pawn.movablePlaces(
				self.compPawnStartingPositions, 
				self.currentEnPassantPlaceId,
				self.enPassantOpponentLeft, 
				self.enPassantOpponentRight, 
				self.isEnPassant, 
				self.currentEnPassantOpponentPlaceId,
				x, 
				y
			)
			self.currentEnPassantPlaceId = self.pawn.getEnPassantPlace()
			self.currentEnPassantOpponentPlaceId = self.pawn.getEnPassantOpponentPlace()
			print("Movable: %s"%movablePlaces)
		
		elif self.chessPiece.isType(pieceId, "rook"):
			movablePlaces = self.rookExtraMoves(self.rook.movablePlaces(x, y))
		
		elif self.chessPiece.isType(pieceId, "bishop"):
			movablePlaces = self.bishop.movablePlaces(x, y)
		
		elif self.chessPiece.isType(pieceId, "queen"):
			movablePlaces = self.queen.movablePlaces(x, y)
		
		elif self.chessPiece.isType(pieceId, "horse"):
			movablePlaces = self.horse.movablePlaces(x, y)
		
		elif self.chessPiece.isType(pieceId, "king"):
			movablePlaces = self.checkerGetter.carefullKing(self.kingExtraMoves(self.king.getKingMovablePlaces(x, y)))
		
		return movablePlaces

	# place a piece in a position that is given in params
	def moveTo(self, placeId):
		matrix = self.chessPiece.live_chessboard_matrix
		selectedId = ""
		if self.current_selected_piece != None:

			if len(self.current_selected_movable_ids) != 0:
				for i in range(len(self.current_selected_movable_ids)):
					if placeId == self.current_selected_movable_ids[i]:
						current_select = Select()
						current_place = current_select.selectFromParentId(matrix, placeId)
						current_place.appendPiece(matrix, self.current_selected_piece, placeId)
						selectedId = self.current_selected_piece.piece_id
						self.movedPieces.append(selectedId)
			
						if selectedId == "player_king" and placeId == "1G":
							self.kingMovedRight = True
						
						if selectedId == "player_king" and placeId == "1C":
							self.kingMovedLeft = True
						
						if self.chessPiece.isType(selectedId, "player_rook"):
							self.kingMovedRight = False
							self.kingMovedLeft = False
					
						if self.currentEnPassantPlaceId != "" or self.currentEnPassantPlaceId != None:
							if placeId == self.currentEnPassantPlaceId:
								self.removeEnPassantOpponent(placeId)	
							
						self.setPlayerPawnsHasMoved(selectedId)
	
	def removeEnPassantOpponent(self, placeId):
		matrix = self.chessPiece.live_chessboard_matrix
		currentCoordinates = self.chessPiece.findPlaceCoordinates(placeId)
		enPassantOpponentPlaceId = self.chessPiece.id_gen(currentCoordinates[0] + 1, currentCoordinates[1])
		enPassantOpponentSelect = Select()
		enPassantOpponentPlace = enPassantOpponentSelect.selectFromParentId(matrix, enPassantOpponentPlaceId)

		if enPassantOpponentPlace != None:
			enPassantOpponent = enPassantOpponentPlace.piece_id
			if enPassantOpponent != None and enPassantOpponent != "":
				self.removeEnPassantOpponentHelper(enPassantOpponent)
			
		
		self.currentEnPassantPlaceId = ""
	

	def removeEnPassantOpponentHelper(pieceId):
		matrix = self.chessPiece.live_chessboard_matrix
		current_select = Select()
		current_element = current_select.selectFromPieceId(matrix, pieceId)
		parent_id = current_element.parent_id

		if current_element != None:
			if self.currentEnPassantOpponentPlaceId != "" or self.currentEnPassantOpponentPlaceId != None:
					if parent_id == self.currentEnPassantOpponentPlaceId:
						current_element.removePiece(matrix, parent_id)

	# sets pawn has moved for the enPassant move
	def setCompPawnsHasMoved(self, pieceId):
		if self.chessPiece.isType(pieceId, "comp_pawn"):
			for i in range(len(self.compPawnsHasMoved)):
				if self.chessPiece.isType(pieceId, str(i+1)):
					self.compPawnsHasMoved[i] = True
				
	# removes the piece the position given replaceses it with the selected piece for taking pieces
	def remove(self, pieceId):
		matrix = self.live_chessboard_matrix
		current_select = Select()
		current_element = current_select.selectFromPieceId(matrix, pieceId)
		parent_id = current_element.parent_id
		if self.current_selected_piece != None:
			if len(self.current_selected_movable_ids) != 0:
				for i in range(len(self.current_selected_movable_ids)):
					if parent_id == self.current_selected_movable_ids[i]:
						current_element.appendPiece(matrix, piece_id, parent_id)

			
		
	

	
	
	
	