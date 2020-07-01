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
		self.kingRescuePosition = ""
		self.kingRescueChessPiece = ""
		self.current_selected_piece = None
		self.current_selected_coordinates = ["" for a in range(2)]
		self.current_selected_movable_ids = []
		self.king_piece = None
		self.king_coordinates = []
		self.kingInCheck = False
		self.movedPieces = []
		self.kingMovedRight = False
		self.kingMovedLeft = False
		self.playerPawnStartingPositions = ["2A", "2B", "2C", "2D", "2E", "2F", "2G", "2H"]
		self.compPawnStartingPositions = ["7A", "7B", "7C", "7D", "7E", "7F", "7G", "7H"]
		self.playerPawnsHasMoved = [False for a in range(8)]
		self.compPawnsHasMoved = [False for a in range(8)]
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
		self.checkerGetter.live_chessboard_matrix = matrix
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
				self.playerPawnStartingPositions, 
				self.currentEnPassantPlaceId,
				self.enPassantOpponentLeft, 
				self.enPassantOpponentRight, 
				self.isEnPassant, 
				self.currentEnPassantOpponentPlaceId,
				self.current_selected_piece,
				self.compPawnsHasMoved,
				x, 
				y
			)
			self.currentEnPassantPlaceId = self.pawn.getEnPassantPlace()
			self.currentEnPassantOpponentPlaceId = self.pawn.getEnPassantOpponentPlace()
		
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
		enPassantOpponentPlaceId = self.chessPiece.id_gen(currentCoordinates[0] - 1, currentCoordinates[1])
		enPassantOpponentSelect = Select()
		enPassantOpponentElement = enPassantOpponentSelect.selectFromParentId(matrix, enPassantOpponentPlaceId)

		if enPassantOpponentElement != None:
			enPassantOpponent = enPassantOpponentElement.piece_id
			if enPassantOpponent != None and enPassantOpponent != "":
				self.removeEnPassantOpponentHelper(enPassantOpponent)
			
		
		self.currentEnPassantPlaceId = ""
	

	def removeEnPassantOpponentHelper(self, pieceId):
		matrix = self.chessPiece.live_chessboard_matrix
		current_select = Select()
		current_element = current_select.selectFromPieceId(matrix, pieceId)
		parent_id = current_element.parent_id

		if current_element != None:
			if self.currentEnPassantOpponentPlaceId != "" or self.currentEnPassantOpponentPlaceId != None:
					if parent_id == self.currentEnPassantOpponentPlaceId:
						current_element.removePiece(matrix, parent_id)

	def setCompPawnsHasMoved(self, pieceId):
		if self.chessPiece.isType(pieceId, "comp_pawn"):
			for i in range(len(self.compPawnsHasMoved)):
				if self.chessPiece.isType(pieceId, str(i+1)):
					self.compPawnsHasMoved[i] = True

	# sets pawn has moved for the enPassant move
	def setPlayerPawnsHasMoved(self, pieceId):
		if self.chessPiece.isType(pieceId, "player_pawn"):
			for i in range(len(self.playerPawnsHasMoved)):
				if self.chessPiece.isType(pieceId, String(i+1)):
					self.compPawnsHasMoved[i] = True

	def setAllcompPawnsHaveMoved(self):
		pawnComps = self.chessPiece.getAllPawnLocations()
		for i in range(len(pawnComps)):
			pieceId = pawnComps[i]
			setCompPawnsHasMoved(pieceId)
		
	def getPawnHasMoved(self, select, array):
		pieceId = select.piece_id
		if self.chessPiece.isType(pieceId, "comp_pawn"):
			for i in range(len(self.compPawnsHasMoved)):
				if self.chessPiece.isType(pieceId, str(i+1)):
					if self.compPawnsHasMoved[i]:
						del array[-1]
					
		return array
				
		
				
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

			


	def rookCanSaveKing(self, movablePlaces):
		rooks = self.chessPiece.getAllRookLocationsAndIds()

		rookPlaces = []
		
		for n in range(len(rooks)):
			currentRookPlaces = self.rookExtraMoves(self.rook.movablePlaces(rooks[n][1], rooks[n][2]))
			for i in range(len(movablePlaces)):
				for j in range(len(currentRookPlaces)):
					if movablePlaces[i] == currentRookPlaces[j]:
						self.kingRescueChessPiece = rooks[n][0]
						self.kingRescuePosition = movablePlaces[i]

						return True


		return False

	def bishopCanSaveKing(self, movablePlaces):
		bishops = self.chessPiece.getAllBishopLocationsAndIds()
		bishopPlaces = []
		
		for n in range(len(bishops)):
			currentBishopPlaces = self.bishop.movablePlaces(bishops[n][1], bishops[n][2])
		
			for i in range(len(movablePlaces)):
				for j in range(len(currentBishopPlaces)):
					if movablePlaces[i] == currentBishopPlaces[j]:
						self.kingRescueChessPiece = bishops[n][0]
						self.kingRescuePosition = movablePlaces[i]

						return True

		return False

	def horseCanSaveKing(self, movablePlaces):
		horses = self.chessPiece.getAllHorseLocationsAndIds()

		horsePlaces = []
		
		for n in range(len(horses)):
			currentHorsePlaces = self.horse.movablePlaces(horses[n][1], horses[n][2])
		
			for i in range(len(movablePlaces)):
				for j in range(len(currentHorsePlaces)):
					if movablePlaces[i] == currentHorsePlaces[j]:
						self.kingRescueChessPiece = horses[n][0]
						self.kingRescuePosition = movablePlaces[i]

						return True

		return False

	def queenCanSaveKing(self, movablePlaces):
		queens = self.chessPiece.getAllQueenLocationsAndIds()

		queenPlaces = []
		
		for n in range(len(queens)):
			currentQueenPlaces = self.queen.movablePlaces(queens[n][1], queens[n][2])
		
			for i in range(len(movablePlaces)):
				for j in range(len(currentQueenPlaces)):
					if movablePlaces[i] == currentQueenPlaces[j]:
						self.kingRescueChessPiece = queens[n][0]
						self.kingRescuePosition = movablePlaces[i]

						return True


		return False

	def pawnCanSaveKing(self, movablePlaces):
		pawns = self.chessPiece.getAllPawnLocationsAndIds()

		pawnPlaces = []
		
		for n in range(len(pawns)):
			current_pawn = Pawn()
			current_pawn.live_chessboard_matrix = self.chessPiece.live_chessboard_matrix
			currentPawnPlaces = current_pawn.movablePlaces(
				self.playerPawnStartingPositions, 
				self.currentEnPassantPlaceId,
				self.enPassantOpponentLeft, 
				self.enPassantOpponentRight, 
				self.isEnPassant, 
				self.currentEnPassantOpponentPlaceId,
				self.current_selected_piece,
				self.compPawnsHasMoved,
				pawns[n][1], 
				pawns[n][2]
			)
			
			for i in range(len(movablePlaces)):
				for j in range(len(currentPawnPlaces)):
					if movablePlaces[i] == currentPawnPlaces[j]:
						self.kingRescueChessPiece = pawns[n][0]
						self.kingRescuePosition = movablePlaces[i]

						return True
			if current_pawn.rightIsEnPassant or current_pawn.leftIsEnPassant:
				leftOfPawn = self.chessPiece.id_gen(pawns[n][2], pawns[n][1] + 1)
				rightOfPawn = self.chessPiece.id_gen(pawns[n][2], pawns[n][1] - 1)
				for k in range(len(movablePlaces)):
					if movablePlaces[k] == leftOfPawn:
						self.kingRescueChessPiece = pawns[n][0]
						self.kingRescuePosition = self.chessPiece.id_gen(pawns[n][2] + 1, pawns[n][1] + 1)

						return True
					
					elif movablePlaces[k] == rightOfPawn:
						self.kingRescueChessPiece = pawns[n][0]
						self.kingRescuePosition = self.chessPiece.id_gen(pawns[n][2] + 1, pawns[n][1] - 1)

						return True
			    

		return False


	def isCheckMate(self, x, y):
		if self.checkerGetter.kingHasCheck():
			movablePlaces = self.checkerGetter.carefullKing(self.kingExtraMoves(self.king.getKingMovablePlaces(x, y)))
			rookMovablePlaces = movablePlaces + self.rookExtraMoves(self.rook.movablePlaces(x, y))
			bishopMovablePlaces = movablePlaces + self.bishop.movablePlaces(x, y)
			queenMovablePlaces = movablePlaces + self.queen.movablePlaces(x, y)
			horseMovablePlaces = movablePlaces + self.horse.movablePlaces(x, y)
			pawn = Pawn()
			pawn.live_chessboard_matrix = self.chessPiece.live_chessboard_matrix
			pawnMovablePlaces = movablePlaces + pawn.movablePlaces(
				self.playerPawnStartingPositions, 
				self.currentEnPassantPlaceId,
				self.enPassantOpponentLeft, 
				self.enPassantOpponentRight, 
				self.isEnPassant, 
				self.currentEnPassantOpponentPlaceId,
				self.current_selected_piece,
				self.compPawnsHasMoved,
				x, 
				y
			)

			if len(rookMovablePlaces) > 0:
				if self.rookCanSaveKing(rookMovablePlaces):
					return False

			if len(bishopMovablePlaces) > 0:
				if self.bishopCanSaveKing(bishopMovablePlaces):
					return False

			if len(horseMovablePlaces) > 0:
				if self.horseCanSaveKing(horseMovablePlaces):
					return False

			if len(queenMovablePlaces) > 0:
				if self.queenCanSaveKing(queenMovablePlaces):
					return False

			if len(pawnMovablePlaces) > 0:
				if self.pawnCanSaveKing(pawnMovablePlaces):
					return False
			
		return True



	
	
	
	