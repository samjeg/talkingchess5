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
	