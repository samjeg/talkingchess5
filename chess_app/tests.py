# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.test import TestCase
from .ChessEngine.ChessPieces.ChessPiece import ChessPiece

class ChessPieceTestCase(TestCase):
	def setUp(self):
		self.chess_piece = ChessPiece()

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
	
	
	
	