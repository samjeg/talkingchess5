# -*- coding: utf-8 -*-
from __future__ import unicode_literals


from django.test import TestCase
from .ChessEngine.ChessPieces.ChessPiece import ChessPiece
from .ChessEngine.Selecter import Select
# from .tests import *

class SelectTestCase(TestCase):
	def setUp(self):
		self.select = Select()


	def testSelectFromParentId(self):
		new_chessboard_matrix = [
			["comp_rook1", "comp_horse1", "comp_bishop1", "comp_queen", "comp_king", "comp_bishop2", "comp_horse2", "comp_rook2"],
			[ "comp_pawn1", "", "comp_pawn3", "comp_pawn4", "comp_pawn5", "comp_pawn6", "comp_pawn7", "comp_pawn8" ],
			[ "", "", "", "", "", "", "", ""],
			[ "", "comp_pawn2", "", "", "", "", "", ""],
			[ "", "", "", "", "", "", "", ""],
			[ "", "", "", "", "", "", "", ""],
			[ "player_pawn1", "player_pawn2", "player_pawn3", "player_pawn4", "player_pawn5", "player_pawn6", "player_pawn7", "player_pawn8" ],
			["player_rook1", "player_horse1", "player_bishop1", "player_queen", "player_king", "player_bishop2", "player_horse2", "player_rook2"]
		]

		self.select.selectFromParentId(new_chessboard_matrix, "5B")

		self.assertEqual(self.select.parent_id, "5B")
		self.assertEqual(self.select.piece_id, "comp_pawn2")

	def testSelectFromPieceId(self):
		new_chessboard_matrix = [
			["comp_rook1", "comp_horse1", "comp_bishop1", "comp_queen", "comp_king", "comp_bishop2", "comp_horse2", "comp_rook2"],
			[ "comp_pawn1", "", "comp_pawn3", "comp_pawn4", "comp_pawn5", "comp_pawn6", "comp_pawn7", "comp_pawn8" ],
			[ "", "", "", "", "", "", "", ""],
			[ "", "comp_pawn2", "", "", "", "", "", ""],
			[ "", "", "", "", "", "", "", ""],
			[ "", "", "", "", "", "", "", ""],
			[ "player_pawn1", "player_pawn2", "player_pawn3", "player_pawn4", "player_pawn5", "player_pawn6", "player_pawn7", "player_pawn8" ],
			["player_rook1", "player_horse1", "player_bishop1", "player_queen", "player_king", "player_bishop2", "player_horse2", "player_rook2"]
		]

		self.select.selectFromPieceId(new_chessboard_matrix, "comp_pawn2")

		self.assertEqual(self.select.parent_id, "5B")
		self.assertEqual(self.select.piece_id, "comp_pawn2")

class ChessPieceTestCase(TestCase):
	def setUp(self):
		self.chess_piece = ChessPiece()

	def testFindPieceCoordinates(self):
		new_chessboard_matrix = [
			["comp_rook1", "comp_horse1", "comp_bishop1", "comp_queen", "comp_king", "comp_bishop2", "comp_horse2", "comp_rook2"],
			[ "comp_pawn1", "", "comp_pawn3", "comp_pawn4", "comp_pawn5", "comp_pawn6", "comp_pawn7", "comp_pawn8" ],
			[ "", "", "", "", "", "", "", ""],
			[ "", "comp_pawn2", "", "", "", "", "", ""],
			[ "", "", "", "", "", "", "", ""],
			[ "", "", "", "", "", "", "", ""],
			[ "player_pawn1", "player_pawn2", "player_pawn3", "player_pawn4", "player_pawn5", "player_pawn6", "player_pawn7", "player_pawn8" ],
			["player_rook1", "player_horse1", "player_bishop1", "player_queen", "player_king", "player_bishop2", "player_horse2", "player_rook2"]
		]

		select = Select()
		select.selectFromPieceId(new_chessboard_matrix, "comp_pawn2")
		coordinates = self.chess_piece.findPieceCoordinates(select)

		self.assertEqual(coordinates[1], 1)
		self.assertEqual(coordinates[0], 3)

	def testMoveArrayToBack(self):
		array = ["5A", "4A", "3A", "5A", "4A", "3A"];

		array_after = self.chess_piece.moveArrayToBack(array)
		expected_array = ["", "", "5A", "4A", "3A", "5A", "4A", "3A"]

		for x in range(len(expected_array)):
			self.assertEqual(array_after[x], expected_array[x])

	def testShrinkContinuosArray(self):
		array = ["A", "", "B", "C", "", ""]
		shrunkenArray = ["A", "B", "C"]
		arrayAfter = self.chess_piece.shrinkContinuosArray(array)

		self.assertEqual(len(arrayAfter), len(shrunkenArray))

	def testFirstCoordinateGen(self):
		input_val = "5"
		expectedResult = 3

		self.assertEqual(self.chess_piece.first_coordinate_gen(input_val), expectedResult)
	
	def testSecondCoordinateGen(self):
		input_val = "F"
		expectedResult = 5

		self.assertEqual(self.chess_piece.second_coordinate_gen(input_val), expectedResult)

	def testFindPlaceCoordinates(self):
		placeId = "2C"
		expectedCoordinates = [6, 2]
		coordinates = self.chess_piece.findPlaceCoordinates(placeId);
		self.assertEqual(expectedCoordinates[0], coordinates[0])
		self.assertEqual(expectedCoordinates[1], coordinates[1])

	def testIsType(self):
		pieceId1 = "player_rook1"
		pieceId2 = "comp_king"
		pieceId3 = "player_pawn5"

		self.assertTrue(self.chess_piece.isType(pieceId1, "rook"))
		self.assertTrue(self.chess_piece.isType(pieceId2, "comp_"))
		self.assertTrue(self.chess_piece.isType(pieceId3, "5"))

	def testIdGen(self):
		input_val = [6, 2]
		expectedResult = "2C"

		self.assertEqual(self.chess_piece.id_gen(input_val[0], input_val[1]), expectedResult)
	
	
	def testMatrixSame(self):
		first_chessboard_matrix = [
			["comp_rook1", "comp_horse1", "comp_bishop1", "comp_queen", "comp_king", "comp_bishop2", "comp_horse2", "comp_rook2"],
			[ "comp_pawn1", "", "comp_pawn3", "comp_pawn4", "comp_pawn5", "comp_pawn6", "comp_pawn7", "comp_pawn8" ],
			[ "", "", "", "", "", "", "", ""],
			[ "", "comp_pawn2", "", "", "", "", "", ""],
			[ "", "", "", "", "", "", "", ""],
			[ "player_horse1", "", "", "", "", "", "", ""],
			[ "player_pawn1", "player_pawn2", "player_pawn3", "player_pawn4", "player_pawn5", "player_pawn6", "player_pawn7", "player_pawn8" ],
			["player_rook1", "", "player_bishop1", "player_queen", "player_king", "player_bishop2", "player_horse2", "player_rook2"]
		]

		second_chessboard_matrix = [
			["comp_rook1", "comp_horse1", "comp_bishop1", "comp_queen", "comp_king", "comp_bishop2", "comp_horse2", "comp_rook2"],
			[ "comp_pawn1", "comp_pawn2", "comp_pawn3", "comp_pawn4", "comp_pawn5", "comp_pawn6", "comp_pawn7", "comp_pawn8" ],
			[ "", "", "", "", "", "", "", ""],
			[ "", "", "", "", "", "", "", ""],
			[ "", "", "", "", "", "", "", ""],
			[ "player_horse1", "", "", "", "", "", "", ""],
			[ "player_pawn1", "player_pawn2", "player_pawn3", "player_pawn4", "player_pawn5", "player_pawn6", "player_pawn7", "player_pawn8" ],
			["player_rook1", "", "player_bishop1", "player_queen", "player_king", "player_bishop2", "player_horse2", "player_rook2"]
		]

		third_chessboard_matrix = [
			["comp_rook1", "comp_horse1", "comp_bishop1", "comp_queen", "comp_king", "comp_bishop2", "comp_horse2", "comp_rook2"],
			[ "comp_pawn1", "", "comp_pawn3", "comp_pawn4", "comp_pawn5", "comp_pawn6", "comp_pawn7", "comp_pawn8" ],
			[ "", "", "", "", "", "", "", ""],
			[ "", "comp_pawn2", "", "", "", "", "", ""],
			[ "", "", "", "", "", "", "", ""],
			[ "player_horse1", "", "", "", "", "", "", ""],
			[ "player_pawn1", "player_pawn2", "player_pawn3", "player_pawn4", "player_pawn5", "player_pawn6", "player_pawn7", "player_pawn8" ],
			["player_rook1", "", "player_bishop1", "player_queen", "player_king", "player_bishop2", "player_horse2", "player_rook2"]
		]

		self.assertTrue(not (self.chess_piece.matrixSame(first_chessboard_matrix, second_chessboard_matrix)))
		self.assertTrue(self.chess_piece.matrixSame(first_chessboard_matrix, third_chessboard_matrix))		
	

	def testFindDiffentPiece(self):
		first_chessboard_matrix = [
			["comp_rook1", "comp_horse1", "comp_bishop1", "comp_queen", "comp_king", "comp_bishop2", "comp_horse2", "comp_rook2"],
			[ "comp_pawn1", "", "comp_pawn3", "comp_pawn4", "comp_pawn5", "comp_pawn6", "comp_pawn7", "comp_pawn8" ],
			[ "", "", "", "", "", "", "", ""],
			[ "", "comp_pawn2", "", "", "", "", "", ""],
			[ "", "", "", "", "", "", "", ""],
			[ "player_horse1", "", "", "", "", "", "", ""],
			[ "player_pawn1", "player_pawn2", "player_pawn3", "player_pawn4", "player_pawn5", "player_pawn6", "player_pawn7", "player_pawn8" ],
			["player_rook1", "", "player_bishop1", "player_queen", "player_king", "player_bishop2", "player_horse2", "player_rook2"]
		]

		second_chessboard_matrix = [
			["comp_rook1", "comp_horse1", "comp_bishop1", "comp_queen", "comp_king", "comp_bishop2", "comp_horse2", "comp_rook2"],
			[ "comp_pawn1", "comp_pawn2", "comp_pawn3", "comp_pawn4", "comp_pawn5", "comp_pawn6", "comp_pawn7", "comp_pawn8" ],
			[ "", "", "", "", "", "", "", ""],
			[ "", "", "", "", "", "", "", ""],
			[ "", "", "", "", "", "", "", ""],
			[ "player_horse1", "", "", "", "", "", "", ""],
			[ "player_pawn1", "player_pawn2", "player_pawn3", "player_pawn4", "player_pawn5", "player_pawn6", "player_pawn7", "player_pawn8" ],
			["player_rook1", "", "player_bishop1", "player_queen", "player_king", "player_bishop2", "player_horse2", "player_rook2"]
		]

		expectedResult = "comp_pawn2";

		self.assertEqual(self.chess_piece.findDiffentPiece(second_chessboard_matrix, first_chessboard_matrix), expectedResult)
	
	def testFindMultipleDifferentPieces(self):
		first_chessboard_matrix = [
			["comp_rook1", "comp_horse1", "", "comp_queen", "comp_king", "comp_bishop2", "", "comp_rook2"],
			[ "comp_pawn1", "", "comp_pawn3", "comp_pawn4", "comp_pawn5", "comp_pawn6", "comp_pawn7", "comp_pawn8" ],
			[ "comp_bishop1", "", "", "", "", "", "", ""],
			[ "", "comp_pawn2", "", "comp_horse2", "", "", "", ""],
			[ "", "", "", "", "", "", "", ""],
			[ "player_horse1", "", "", "", "", "", "", ""],
			[ "player_pawn1", "player_pawn2", "player_pawn3", "player_pawn4", "player_pawn5", "player_pawn6", "player_pawn7", "player_pawn8" ],
			["player_rook1", "", "player_bishop1", "player_queen", "player_king", "player_bishop2", "player_horse2", "player_rook2"]
		]

		second_chessboard_matrix = [
			["comp_rook1", "comp_horse1", "comp_bishop1", "comp_queen", "comp_king", "comp_bishop2", "comp_horse2", "comp_rook2"],
			[ "comp_pawn1", "comp_pawn2", "comp_pawn3", "comp_pawn4", "comp_pawn5", "comp_pawn6", "comp_pawn7", "comp_pawn8" ],
			[ "", "", "", "", "", "", "", ""],
			[ "", "", "", "", "", "", "", ""],
			[ "", "", "", "", "", "", "", ""],
			[ "player_horse1", "", "", "", "", "", "", ""],
			[ "player_pawn1", "player_pawn2", "player_pawn3", "player_pawn4", "player_pawn5", "player_pawn6", "player_pawn7", "player_pawn8" ],
			["player_rook1", "", "player_bishop1", "player_queen", "player_king", "player_bishop2", "player_horse2", "player_rook2"]
		]
 
		expectedResult = ["comp_bishop1", "comp_horse2", "comp_pawn2"]
		differentPieces = self.chess_piece.shrinkContinuosArray(
			self.chess_piece.findMultipleDifferentPieces(second_chessboard_matrix, first_chessboard_matrix)
		)

		for i in range(len(differentPieces)):
			if differentPieces[i] != expectedResult[i]:
				self.assertEqual(differentPieces[i], expectedResult[i])


	def testFindBoardCoordinates(self):
		first_chessboard_matrix = [
			["comp_rook1", "comp_horse1", "comp_bishop1", "comp_queen", "comp_king", "comp_bishop2", "comp_horse2", "comp_rook2"],
			[ "comp_pawn1", "", "comp_pawn3", "comp_pawn4", "comp_pawn5", "comp_pawn6", "comp_pawn7", "comp_pawn8" ],
			[ "", "", "", "", "", "", "", ""],
			[ "", "comp_pawn2", "", "", "", "", "", ""],
			[ "", "", "", "", "", "", "", ""],
			[ "", "", "", "", "", "", "", ""],
			[ "player_pawn1", "player_pawn2", "player_pawn3", "player_pawn4", "player_pawn5", "player_pawn6", "player_pawn7", "player_pawn8" ],
			["player_rook1", "player_horse1", "player_bishop1", "player_queen", "player_king", "player_bishop2", "player_horse2", "player_rook2"]
		]

		input2 = "comp_pawn2"
		expectedResult = [3, 1]

		self.assertTrue(self.chess_piece.findBoardCoordinates(first_chessboard_matrix, input2))

	def testLiveChessboardMatrixGen(self):
		chess_piece_ids = [ 
			"comp_pawn1", "comp_pawn2", "comp_pawn3", "comp_pawn4", "comp_pawn5", "comp_pawn6", "comp_pawn7", "comp_pawn8", 
			"comp_rook1", "comp_horse1", "comp_bishop1", "comp_queen", "comp_king", "comp_bishop2", "comp_horse2", "comp_rook2",
			"player_pawn1", "player_pawn2", "player_pawn3", "player_pawn4", "player_pawn5", "player_pawn6", "player_pawn7", "player_pawn8",
			"player_rook1", "player_horse1", "player_bishop1", "player_queen", "player_king", "player_bishop2", "player_horse2", "player_rook2",
		]

		chess_place_ids = [
			"7A", "5B", "7C", "7D", "7E", "7F", "7G", "7H",
			"8A", "8B", "8C", "8D", "8E", "8F", "8G", "8H",
			"2A", "2B", "2C", "2D", "2E", "2F", "2G", "2H",
			"1A", "1B", "1C", "1D", "1E", "1F", "1G", "1H"	
		]

		expectedResult = [
			["comp_rook1", "comp_horse1", "comp_bishop1", "comp_queen", "comp_king", "comp_bishop2", "comp_horse2", "comp_rook2"],
			[ "comp_pawn1", "", "comp_pawn3", "comp_pawn4", "comp_pawn5", "comp_pawn6", "comp_pawn7", "comp_pawn8" ],
			[ "", "", "", "", "", "", "", ""],
			[ "", "comp_pawn2", "", "", "", "", "", ""],
			[ "", "", "", "", "", "", "", ""],
			[ "", "", "", "", "", "", "", ""],
			[ "player_pawn1", "player_pawn2", "player_pawn3", "player_pawn4", "player_pawn5", "player_pawn6", "player_pawn7", "player_pawn8" ],
			["player_rook1", "player_horse1", "player_bishop1", "player_queen", "player_king", "player_bishop2", "player_horse2", "player_rook2"]
		]

		matrixAfter = self.chess_piece.live_chessboard_matrix_gen(chess_place_ids, chess_piece_ids);

		for i in range(len(expectedResult)):
			for j in range(len(expectedResult[i])):
				print("Data %s %s"%(matrixAfter[i][j], expectedResult[i][j]))
				self.assertEquals(matrixAfter[i][j], expectedResult[i][j])
		
		