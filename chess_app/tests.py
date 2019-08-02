# -*- coding: utf-8 -*-
from __future__ import unicode_literals


from django.test import TestCase
from .ChessEngine.ChessPieces.ChessPiece import ChessPiece
from .ChessEngine.ChessPieces.Horse import Horse
from .ChessEngine.ChessPieces.Rook import Rook
from .ChessEngine.ChessPieces.Bishop import Bishop
from .ChessEngine.ChessPieces.Queen import Queen
from .ChessEngine.ChessPieces.Pawn import Pawn
from .ChessEngine.ChessPieces.King import King
from .ChessEngine.Selecter import Select
from .ChessEngine.CheckerGetter import CheckerGetter
from .ChessEngine.ChessMechanics import ChessMechanics

class ChessMechanicsTestCase(TestCase):
    
    def setUp(self):
        self.checker_getter = CheckerGetter()
        self.king = King()
        self.pawn = Pawn()
        self.chess_mech = ChessMechanics()
    

    def testCarefullKing(self):
        chessboard_matrix = [
            ["comp_rook1", "", "", "", "comp_king", "", "", "comp_rook2"],
            [ "comp_pawn1", "comp_pawn2", "comp_pawn3", "", "", "", "comp_pawn7", "comp_pawn8" ],
            [ "", "", "", "", "", "", "", ""],
            [ "comp_horse2", "player_bishop1", "player_bishop2", "comp_queen", "comp_bishop1", "comp_horse1", "", ""],
            [ "comp_pawn6", "", "", "", "", "", "", ""],
            [ "comp_pawn5", "comp_pawn4", "", "", "", "", "", ""],
            [ "player_pawn1", "player_pawn2", "player_pawn3", "player_pawn4", "player_pawn5", "player_pawn6", "player_pawn7", "player_pawn8" ],
            ["player_rook1", "player_horse1", "", "player_queen", "player_king", "player_bishop2", "player_horse2", "player_rook2"]
        ]
        

        self.king.live_chessboard_matrix = chessboard_matrix
        self.checker_getter.live_chessboard_matrix = chessboard_matrix
        self.checker_getter.pawn.live_chessboard_matrix = chessboard_matrix
        self.checker_getter.king.live_chessboard_matrix = chessboard_matrix
        self.checker_getter.queen.live_chessboard_matrix = chessboard_matrix
        self.checker_getter.rook.live_chessboard_matrix = chessboard_matrix
        self.checker_getter.bishop.live_chessboard_matrix = chessboard_matrix
        self.checker_getter.horse.live_chessboard_matrix = chessboard_matrix
        

        movable = self.checker_getter.carefullKing(self.king.getKingMovablePlaces(4, 0))
        expectedResult = ["8D", "7F"]

        for i in range(len(movable)):
            if movable[i] != expectedResult[i]:
                self.assertEqual(movable[i], expectedResult[i])
    

    def testEnPassant(self):
        
        chessboard_matrix = [
            ["comp_rook1", "comp_horse1", "comp_bishop1", "comp_queen", "comp_king", "comp_bishop2", "comp_horse2", "comp_rook2"],
            [ "comp_pawn1", "", "comp_pawn3", "comp_pawn4", "comp_pawn5", "comp_pawn6", "comp_pawn7", "comp_pawn8" ],
            [ "", "", "", "", "", "", "", ""],
            [ "", "", "", "", "", "", "", ""],
            [ "", "player_pawn2", "comp_pawn2", "", "", "", "", ""],
            [ "", "", "", "", "", "", "", ""],
            [ "player_pawn1", "", "player_pawn3", "player_pawn4", "player_pawn5", "player_pawn6", "player_pawn7", "player_pawn8" ],
            ["player_rook1", "player_horse1", "player_bishop1", "player_queen", "player_king", "player_bishop2", "player_horse2", "player_rook2"]
        ]

       
        
        self.chess_mech.playerPawnStartingPositions = ["2A", "2B", "2C", "2D", "2E", "2F", "2G", "2H"]
        self.chess_mech.compPawnStartingPositions = ["7A", "7B", "7C", "7D", "7E", "7F", "7G", "7H"]
    
        
        self.chess_mech.chessPiece.live_chessboard_matrix = chessboard_matrix
        
        enPassantOpponentSelect = Select()
        enPassantOpponent = enPassantOpponentSelect.selectFromParentId(chessboard_matrix, "4B")
        if enPassantOpponent.parent_id != None:
            if enPassantOpponent.piece_id != None:
                self.assertEqual(enPassantOpponent.piece_id, "player_pawn2")
            
    

        self.chess_mech.select("comp_pawn2")
        self.chess_mech.moveTo("3B")

        enPassantOpponentAfterSelect = Select()
        enPassantOpponentAfter = enPassantOpponentAfterSelect.selectFromParentId(chessboard_matrix, "4B")
        if enPassantOpponentAfter != None:
            self.assertEqual(enPassantOpponentAfter.piece_id, "")
        
      

    

class CastlingTestcase(TestCase):
    
    def setUp(self):
        self.chess_mech = ChessMechanics();
    

    def testCanCastleLeft(self):
        chessboard_matrix = [
            ["comp_rook1", "comp_horse1", "comp_bishop1", "comp_queen", "comp_king", "", "", "comp_rook2"],
            [ "comp_pawn1", "comp_pawn2", "comp_pawn3", "comp_pawn4", "comp_pawn5", "comp_pawn6", "comp_pawn7", "comp_pawn8" ],
            [ "", "", "", "", "", "", "", ""],
            [ "", "comp_bishop2", "comp_horse2", "", "", "", "", ""],
            [ "", "", "", "", "", "", "", ""],
            [ "", "", "", "", "", "", "", ""],
            [ "player_pawn1", "player_pawn2", "player_pawn3", "player_pawn4", "player_pawn5", "player_pawn6", "player_pawn7", "player_pawn8" ],
            ["player_rook1", "player_horse1", "player_bishop1", "player_queen", "player_king", "player_bishop2", "player_horse2", "player_rook2"]
        ]

        self.chess_mech.rook.live_chessboard_matrix = chessboard_matrix
        self.chess_mech.chessPiece.live_chessboard_matrix = chessboard_matrix
        self.chess_mech.checkerGetter.live_chessboard_matrix = chessboard_matrix
        self.assertTrue(self.chess_mech.canCastleLeft())
    

    def testCannotCastleLeft(self):
        chessboard_matrix = [
            ["comp_rook1", "comp_horse1", "comp_bishop1", "comp_queen", "comp_king", "", "", "comp_rook2"],
            [ "comp_pawn1", "comp_pawn2", "comp_pawn3", "comp_pawn4", "", "comp_pawn6", "comp_pawn7", "comp_pawn8" ],
            [ "", "", "", "", "", "", "", ""],
            [ "", "", "player_bishop1", "", "", "", "", ""],
            [ "", "", "", "", "", "", "", ""],
            [ "comp_bishop2", "comp_horse2", "comp_pawn5", "", "", "", "", ""],
            [ "player_pawn1", "player_pawn2", "player_pawn3", "player_pawn4", "player_pawn5", "player_pawn6", "player_pawn7", "player_pawn8" ],
            ["player_rook1", "player_horse1", "player_bishop1", "", "player_king", "player_bishop2", "player_horse2", "player_rook2"]
        ]

        self.chess_mech.rook.live_chessboard_matrix = chessboard_matrix
        self.chess_mech.chessPiece.live_chessboard_matrix = chessboard_matrix
        self.chess_mech.checkerGetter.live_chessboard_matrix = chessboard_matrix
        self.assertTrue(not self.chess_mech.canCastleLeft())
        

    def testCanCastleRight(self):
        chessboard_matrix = [
            ["comp_rook1", "", "", "", "comp_king", "comp_bishop2", "comp_horse2", "comp_rook2"],
            [ "comp_pawn1", "comp_pawn2", "comp_pawn3", "comp_pawn4", "comp_pawn5", "comp_pawn6", "comp_pawn7", "comp_pawn8" ],
            [ "", "", "", "", "", "", "", ""],
            [ "comp_queen", "comp_bishop1", "comp_horse1", "", "", "", "", ""],
            [ "", "", "", "", "", "", "", ""],
            [ "", "", "", "", "", "", "", ""],
            [ "player_pawn1", "player_pawn2", "player_pawn3", "player_pawn4", "player_pawn5", "player_pawn6", "player_pawn7", "player_pawn8" ],
            ["player_rook1", "player_horse1", "player_bishop1", "player_queen", "player_king", "player_bishop2", "player_horse2", "player_rook2"]
        ]

        
        self.chess_mech.rook.live_chessboard_matrix = chessboard_matrix
        self.chess_mech.chessPiece.live_chessboard_matrix = chessboard_matrix
        self.chess_mech.checkerGetter.live_chessboard_matrix = chessboard_matrix      
        self.assertTrue(self.chess_mech.canCastleRight())
    

    def testCannotCastleRight(self):
        chessboard_matrix = [
            ["comp_rook1", "", "", "", "comp_king", "comp_bishop2", "comp_horse2", "comp_rook2"],
            [ "comp_pawn1", "comp_pawn2", "comp_pawn3", "comp_pawn4", "", "comp_pawn6", "comp_pawn7", "comp_pawn8" ],
            [ "comp_pawn5", "", "", "", "", "", "", ""],
            [ "comp_queen", "comp_bishop1", "comp_horse1", "", "", "", "player_queen", ""],
            [ "", "", "", "", "", "", "", ""],
            [ "", "", "", "", "", "", "", ""],
            [ "player_pawn1", "player_pawn2", "player_pawn3", "player_pawn4", "player_pawn5", "player_pawn6", "player_pawn7", "player_pawn8" ],
            ["player_rook1", "player_horse1", "player_bishop1", "", "player_king", "player_bishop2", "player_horse2", "player_rook2"]
        ]

   
        self.chess_mech.rook.live_chessboard_matrix = chessboard_matrix
        self.chess_mech.chessPiece.live_chessboard_matrix = chessboard_matrix
        self.chess_mech.checkerGetter.live_chessboard_matrix = chessboard_matrix
        self.assertTrue(not self.chess_mech.canCastleRight())
    

class CheckerGetterTestCase(TestCase):

    def setUp(self):
        self.checker_getter = CheckerGetter()

    def testKingCanCheck(self):
        first_chessboard_matrix = [
            ["comp_rook1", "comp_horse1", "comp_bishop1", "comp_queen", "comp_king", "comp_bishop2", "comp_horse2", "comp_rook2"],
            [ "comp_pawn1", "comp_pawn2", "comp_pawn3", "", "comp_pawn5", "player_rook2", "comp_pawn6", "comp_pawn8" ],
            [ "", "", "", "", "", "", "", ""],
            [ "", "player_bishop1", "", "comp_pawn4", "", "comp_pawn7", "", ""],
            [ "", "", "", "", "", "", "", ""],
            [ "", "", "", "", "", "", "", ""],
            [ "player_pawn1", "player_pawn2", "player_pawn3", "player_pawn4", "player_pawn5", "player_pawn6", "player_pawn7", "player_pawn8" ],
            ["player_rook1", "player_horse1", "", "player_queen", "player_king", "player_bishop2", "player_horse2", ""]
        ]

        self.checker_getter.live_chessboard_matrix = first_chessboard_matrix 
    
        self.assertTrue(self.checker_getter.kingHasCheck())
    

class KingTestCase(TestCase):

    def setUp(self):
        self.king = King()

    def testMovablePlaces(self):
        new_chessboard_matrix = [
            ["comp_rook1", "comp_horse1", "comp_bishop1", "comp_queen",
                "comp_king", "comp_bishop2", "comp_horse2", "comp_rook2"],
            ["comp_pawn1", "", "comp_pawn3", "comp_pawn4",
                "comp_pawn5", "comp_pawn6", "comp_pawn7", "comp_pawn8"],
            ["", "", "", "", "", "", "", ""],
            ["", "comp_pawn2", "", "", "", "", "", ""],
            ["", "", "", "", "", "", "", ""],
            ["", "", "", "", "", "", "", ""],
            ["player_pawn1", "player_pawn2", "player_pawn3", "player_pawn4",
                "player_pawn5", "player_pawn6", "player_pawn7", "player_pawn8"],
            ["player_rook1", "player_horse1", "player_bishop1", "player_queen",
                "player_king", "player_bishop2", "player_horse2", "player_rook2"]
        ]

        self.king.live_chessboard_matrix = new_chessboard_matrix
        expectedResult = ['2C', '4C', '3B', '3D', '4D', '2D', '4B', '2B']
        movable = self.king.getKingMovablePlaces(2, 5)

        for i in range(len(movable)):
			if movable[i] != expectedResult[i]:
				self.assertEqual(movable[i], expectedResult[i])

	

class PawnTestCase(TestCase):
    
    def setUp(self):
        self.pawn = Pawn()
        self.chess_piece = ChessPiece()
        self.chess_mech = ChessMechanics()

    def testGetMovablePlaces(self):
        new_chessboard_matrix = [
            ["comp_rook1", "comp_horse1", "comp_bishop1", "comp_queen",
                "comp_king", "comp_bishop2", "comp_horse2", "comp_rook2"],
            ["comp_pawn1", "comp_pawn2", "comp_pawn3", "comp_pawn4",
                "comp_pawn5", "comp_pawn6", "comp_pawn7", "comp_pawn8"],
            ["", "", "", "", "", "", "", ""],
            ["", "", "", "", "", "", "", ""],
            ["", "player_pawn2", "", "", "", "", "", ""],
            ["", "", "", "", "", "", "", ""],
            ["player_pawn1", "", "player_pawn3", "player_pawn4",
                "player_pawn5", "player_pawn6", "player_pawn7", "player_pawn8"],
            ["player_rook1", "player_horse1", "player_bishop1", "player_queen",
                "player_king", "player_bishop2", "player_horse2", "player_rook2"]
        ]

        select = Select()
        select.piece_id = "comp_pawn6"
        select.parent_id = "7F"
        self.pawn.currentPiece = select
        self.pawn.live_chessboard_matrix = new_chessboard_matrix
        movable = self.pawn.getPawnMovablePlaces(5, 1)
        movable2 = self.pawn.getPawnMovablePlaces(2, 5)
        expectedMovable = ['', '', '6F', '5F']
        expectedMovable2 = ["2D", "", "", ""]


        for i in range(len(movable)):
            if movable[i] != expectedMovable[i]:
                self.assertEqual(movable[i], expectedMovable[i])

		for j in range(len(movable2)):
			if movableWithPawn[j] != expectedMovable2[j]:
				self.assertEqual(movable2[j], expectedMovable2[j])


        self.chess_mech.chessPiece.live_chessboard_matrix = new_chessboard_matrix
        self.chess_mech.select("comp_pawn8")
        pawnMovableBefore = self.chess_mech.current_selected_movable_ids
        

        self.chess_mech.moveTo("6H")
        self.chess_mech.select("comp_pawn8")
        pawnMovableAfter = self.chess_mech.current_selected_movable_ids
        
        self.assertNotEqual(pawnMovableBefore, pawnMovableAfter)





class QueenTestCase(TestCase):

    def setUp(self):
        self.queen = Queen()

    def testMovablePlaces(self):
        new_chessboard_matrix = [
            ["comp_rook1", "comp_horse1", "comp_bishop1", "comp_queen",
                "comp_king", "comp_bishop2", "comp_horse2", "comp_rook2"],
            ["comp_pawn1", "", "comp_pawn3", "comp_pawn4",
                "comp_pawn5", "comp_pawn6", "comp_pawn7", "comp_pawn8"],
            ["", "", "", "", "", "", "", ""],
            ["", "comp_pawn2", "", "", "", "", "", ""],
            ["", "", "", "", "", "", "", ""],
            ["", "", "", "", "", "", "", ""],
            ["player_pawn1", "player_pawn2", "player_pawn3", "player_pawn4",
                "player_pawn5", "player_pawn6", "player_pawn7", "player_pawn8"],
            ["player_rook1", "player_horse1", "player_bishop1", "player_queen",
                "player_king", "player_bishop2", "player_horse2", "player_rook2"]
        ]

        self.queen.live_chessboard_matrix = new_chessboard_matrix
        expectedResult = [
            '3D', '3E', '3F', '3G', '3H', '3B', '3A', '2C', '4C', '5C', 
            '6C', '4D', '5E', '6F', '2B', '4B', '5A', '2D'
        ]
        movable = self.queen.movablePlaces(2, 5)
    
        
        for i in range(len(movable)):
            if movable[i] != expectedResult[i]:
                self.assertEqual(movable[i], expectedResult[i])


class BishopTestCase(TestCase):

    def setUp(self):
        self.bishop = Bishop()

    def testMovablePlaces(self):
        new_chessboard_matrix = [
            ["comp_rook1", "comp_horse1", "comp_bishop1", "comp_queen",
                "comp_king", "comp_bishop2", "comp_horse2", "comp_rook2"],
            ["comp_pawn1", "", "comp_pawn3", "comp_pawn4",
                "comp_pawn5", "comp_pawn6", "comp_pawn7", "comp_pawn8"],
            ["", "", "", "", "", "", "", ""],
            ["", "comp_pawn2", "", "", "", "", "", ""],
            ["", "", "", "", "", "", "", ""],
            ["", "", "", "", "", "", "", ""],
            ["player_pawn1", "player_pawn2", "player_pawn3", "player_pawn4",
                "player_pawn5", "player_pawn6", "player_pawn7", "player_pawn8"],
            ["player_rook1", "player_horse1", "player_bishop1", "player_queen",
                "player_king", "player_bishop2", "player_horse2", "player_rook2"]
        ]
        self.bishop.live_chessboard_matrix = new_chessboard_matrix
        expectedResult = ['4D', '5E', '6F', '2B', '4B', '5A', '2D']
        movable = self.bishop.movablePlaces(2, 5)

        for i in range(len(movable)):
            if movable[i] != expectedResult[i]:
                self.assertEqual(movable[i], expectedResult[i])


class RookTestCase(TestCase):

    def setUp(self):
        self.rook = Rook()

    def testMovablePlaces(self):
        new_chessboard_matrix = [
            ["comp_rook1", "comp_horse1", "comp_bishop1", "comp_queen",
                "comp_king", "comp_bishop2", "comp_horse2", "comp_rook2"],
            ["comp_pawn1", "", "comp_pawn3", "comp_pawn4",
                "comp_pawn5", "comp_pawn6", "comp_pawn7", "comp_pawn8"],
            ["", "", "", "", "", "", "", ""],
            ["", "comp_pawn2", "", "", "", "", "", ""],
            ["", "", "", "", "", "", "", ""],
            ["", "", "", "", "", "", "", ""],
            ["player_pawn1", "player_pawn2", "player_pawn3", "player_pawn4",
                "player_pawn5", "player_pawn6", "player_pawn7", "player_pawn8"],
            ["player_rook1", "player_horse1", "player_bishop1", "player_queen",
                "player_king", "player_bishop2", "player_horse2", "player_rook2"]
        ]
        self.rook.live_chessboard_matrix = new_chessboard_matrix
        expectedResult = ['3D', '3E', '3F', '3G', '3H', '3B', '3A', '2C', '4C', '5C', '6C']
        movable = self.rook.movablePlaces(2, 5)
        
        for i in range(len(movable)):
            if movable[i] != expectedResult[i]:
                self.assertEqual(movable[i], expectedResult[i])


class HorseTestCase(TestCase):

    def setUp(self):
        self.horse = Horse()

    def testMovablePlaces(self):
        new_chessboard_matrix = [
            ["comp_rook1", "comp_horse1", "comp_bishop1", "comp_queen",
                "comp_king", "comp_bishop2", "comp_horse2", "comp_rook2"],
            ["comp_pawn1", "", "comp_pawn3", "comp_pawn4",
                "comp_pawn5", "comp_pawn6", "comp_pawn7", "comp_pawn8"],
            ["", "", "", "", "", "", "", ""],
            ["", "comp_pawn2", "", "", "", "", "", ""],
            ["", "", "", "", "", "", "", ""],
            ["", "", "", "", "", "", "", ""],
            ["player_pawn1", "player_pawn2", "player_pawn3", "player_pawn4",
                "player_pawn5", "player_pawn6", "player_pawn7", "player_pawn8"],
            ["player_rook1", "player_horse1", "player_bishop1", "player_queen",
                "player_king", "player_bishop2", "player_horse2", "player_rook2"]
        ]
        self.horse.live_chessboard_matrix = new_chessboard_matrix
        expectedResult = ['3G', '4F', '6F']
        movable = self.horse.movablePlaces(7, 3)

        for i in range(len(movable)):
            if movable[i] != expectedResult[i]:
                self.assertEqual(movable[i], expectedResult[i])


class SelectTestCase(TestCase):
    def setUp(self):
        self.select = Select()

    def testSelectFromParentId(self):
        new_chessboard_matrix = [
            ["comp_rook1", "comp_horse1", "comp_bishop1", "comp_queen",
                "comp_king", "comp_bishop2", "comp_horse2", "comp_rook2"],
            ["comp_pawn1", "", "comp_pawn3", "comp_pawn4",
                "comp_pawn5", "comp_pawn6", "comp_pawn7", "comp_pawn8"],
            ["", "", "", "", "", "", "", ""],
            ["", "comp_pawn2", "", "", "", "", "", ""],
            ["", "", "", "", "", "", "", ""],
            ["", "", "", "", "", "", "", ""],
            ["player_pawn1", "player_pawn2", "player_pawn3", "player_pawn4",
                "player_pawn5", "player_pawn6", "player_pawn7", "player_pawn8"],
            ["player_rook1", "player_horse1", "player_bishop1", "player_queen",
                "player_king", "player_bishop2", "player_horse2", "player_rook2"]
        ]

        self.select.selectFromParentId(new_chessboard_matrix, "5B")

        self.assertEqual(self.select.parent_id, "5B")
        self.assertEqual(self.select.piece_id, "comp_pawn2")

    def testSelectFromPieceId(self):
        new_chessboard_matrix = [
            ["comp_rook1", "comp_horse1", "comp_bishop1", "comp_queen",
                "comp_king", "comp_bishop2", "comp_horse2", "comp_rook2"],
            ["comp_pawn1", "", "comp_pawn3", "comp_pawn4",
                "comp_pawn5", "comp_pawn6", "comp_pawn7", "comp_pawn8"],
            ["", "", "", "", "", "", "", ""],
            ["", "comp_pawn2", "", "", "", "", "", ""],
            ["", "", "", "", "", "", "", ""],
            ["", "", "", "", "", "", "", ""],
            ["player_pawn1", "player_pawn2", "player_pawn3", "player_pawn4",
                "player_pawn5", "player_pawn6", "player_pawn7", "player_pawn8"],
            ["player_rook1", "player_horse1", "player_bishop1", "player_queen",
                "player_king", "player_bishop2", "player_horse2", "player_rook2"]
        ]

        self.select.selectFromPieceId(new_chessboard_matrix, "comp_pawn2")

        self.assertEqual(self.select.parent_id, "5B")
        self.assertEqual(self.select.piece_id, "comp_pawn2")


class ChessPieceTestCase(TestCase):
    def setUp(self):
        self.chess_piece = ChessPiece()

    def testFindPieceCoordinates(self):
        new_chessboard_matrix = [
            ["comp_rook1", "comp_horse1", "comp_bishop1", "comp_queen",
                "comp_king", "comp_bishop2", "comp_horse2", "comp_rook2"],
            ["comp_pawn1", "", "comp_pawn3", "comp_pawn4",
                "comp_pawn5", "comp_pawn6", "comp_pawn7", "comp_pawn8"],
            ["", "", "", "", "", "", "", ""],
            ["", "comp_pawn2", "", "", "", "", "", ""],
            ["", "", "", "", "", "", "", ""],
            ["", "", "", "", "", "", "", ""],
            ["player_pawn1", "player_pawn2", "player_pawn3", "player_pawn4",
                "player_pawn5", "player_pawn6", "player_pawn7", "player_pawn8"],
            ["player_rook1", "player_horse1", "player_bishop1", "player_queen",
                "player_king", "player_bishop2", "player_horse2", "player_rook2"]
        ]

        select = Select()
        select.selectFromPieceId(new_chessboard_matrix, "comp_pawn2")
        coordinates = self.chess_piece.findPieceCoordinates(select)

        self.assertEqual(coordinates[1], 1)
        self.assertEqual(coordinates[0], 3)

    def testMoveArrayToBack(self):
        array = ["5A", "4A", "3A", "5A", "4A", "3A"]

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

        self.assertEqual(self.chess_piece.first_coordinate_gen(
            input_val), expectedResult)

    def testSecondCoordinateGen(self):
        input_val = "F"
        expectedResult = 5

        self.assertEqual(self.chess_piece.second_coordinate_gen(
            input_val), expectedResult)

    def testFindPlaceCoordinates(self):
        placeId = "2C"
        expectedCoordinates = [6, 2]
        coordinates = self.chess_piece.findPlaceCoordinates(placeId)
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

        self.assertEqual(self.chess_piece.id_gen(
            input_val[0], input_val[1]), expectedResult)

    def testMatrixSame(self):
        first_chessboard_matrix = [
            ["comp_rook1", "comp_horse1", "comp_bishop1", "comp_queen",
                "comp_king", "comp_bishop2", "comp_horse2", "comp_rook2"],
            ["comp_pawn1", "", "comp_pawn3", "comp_pawn4",
                "comp_pawn5", "comp_pawn6", "comp_pawn7", "comp_pawn8"],
            ["", "", "", "", "", "", "", ""],
            ["", "comp_pawn2", "", "", "", "", "", ""],
            ["", "", "", "", "", "", "", ""],
            ["player_horse1", "", "", "", "", "", "", ""],
            ["player_pawn1", "player_pawn2", "player_pawn3", "player_pawn4",
                "player_pawn5", "player_pawn6", "player_pawn7", "player_pawn8"],
            ["player_rook1", "", "player_bishop1", "player_queen",
                "player_king", "player_bishop2", "player_horse2", "player_rook2"]
        ]

        second_chessboard_matrix = [
            ["comp_rook1", "comp_horse1", "comp_bishop1", "comp_queen",
                "comp_king", "comp_bishop2", "comp_horse2", "comp_rook2"],
            ["comp_pawn1", "comp_pawn2", "comp_pawn3", "comp_pawn4",
                "comp_pawn5", "comp_pawn6", "comp_pawn7", "comp_pawn8"],
            ["", "", "", "", "", "", "", ""],
            ["", "", "", "", "", "", "", ""],
            ["", "", "", "", "", "", "", ""],
            ["player_horse1", "", "", "", "", "", "", ""],
            ["player_pawn1", "player_pawn2", "player_pawn3", "player_pawn4",
                "player_pawn5", "player_pawn6", "player_pawn7", "player_pawn8"],
            ["player_rook1", "", "player_bishop1", "player_queen",
                "player_king", "player_bishop2", "player_horse2", "player_rook2"]
        ]

        third_chessboard_matrix = [
            ["comp_rook1", "comp_horse1", "comp_bishop1", "comp_queen",
                "comp_king", "comp_bishop2", "comp_horse2", "comp_rook2"],
            ["comp_pawn1", "", "comp_pawn3", "comp_pawn4",
                "comp_pawn5", "comp_pawn6", "comp_pawn7", "comp_pawn8"],
            ["", "", "", "", "", "", "", ""],
            ["", "comp_pawn2", "", "", "", "", "", ""],
            ["", "", "", "", "", "", "", ""],
            ["player_horse1", "", "", "", "", "", "", ""],
            ["player_pawn1", "player_pawn2", "player_pawn3", "player_pawn4",
                "player_pawn5", "player_pawn6", "player_pawn7", "player_pawn8"],
            ["player_rook1", "", "player_bishop1", "player_queen",
                "player_king", "player_bishop2", "player_horse2", "player_rook2"]
        ]

        self.assertTrue(not (self.chess_piece.matrixSame(
            first_chessboard_matrix, second_chessboard_matrix)))
        self.assertTrue(self.chess_piece.matrixSame(
            first_chessboard_matrix, third_chessboard_matrix))

    def testFindDiffentPiece(self):
        first_chessboard_matrix = [
            ["comp_rook1", "comp_horse1", "comp_bishop1", "comp_queen",
                "comp_king", "comp_bishop2", "comp_horse2", "comp_rook2"],
            ["comp_pawn1", "", "comp_pawn3", "comp_pawn4",
                "comp_pawn5", "comp_pawn6", "comp_pawn7", "comp_pawn8"],
            ["", "", "", "", "", "", "", ""],
            ["", "comp_pawn2", "", "", "", "", "", ""],
            ["", "", "", "", "", "", "", ""],
            ["player_horse1", "", "", "", "", "", "", ""],
            ["player_pawn1", "player_pawn2", "player_pawn3", "player_pawn4",
                "player_pawn5", "player_pawn6", "player_pawn7", "player_pawn8"],
            ["player_rook1", "", "player_bishop1", "player_queen",
                "player_king", "player_bishop2", "player_horse2", "player_rook2"]
        ]

        second_chessboard_matrix = [
            ["comp_rook1", "comp_horse1", "comp_bishop1", "comp_queen",
                "comp_king", "comp_bishop2", "comp_horse2", "comp_rook2"],
            ["comp_pawn1", "comp_pawn2", "comp_pawn3", "comp_pawn4",
                "comp_pawn5", "comp_pawn6", "comp_pawn7", "comp_pawn8"],
            ["", "", "", "", "", "", "", ""],
            ["", "", "", "", "", "", "", ""],
            ["", "", "", "", "", "", "", ""],
            ["player_horse1", "", "", "", "", "", "", ""],
            ["player_pawn1", "player_pawn2", "player_pawn3", "player_pawn4",
                "player_pawn5", "player_pawn6", "player_pawn7", "player_pawn8"],
            ["player_rook1", "", "player_bishop1", "player_queen",
                "player_king", "player_bishop2", "player_horse2", "player_rook2"]
        ]

        expectedResult = "comp_pawn2"

        self.assertEqual(self.chess_piece.findDiffentPiece(
            second_chessboard_matrix, first_chessboard_matrix), expectedResult)

    def testFindMultipleDifferentPieces(self):
        first_chessboard_matrix = [
            ["comp_rook1", "comp_horse1", "", "comp_queen",
                "comp_king", "comp_bishop2", "", "comp_rook2"],
            ["comp_pawn1", "", "comp_pawn3", "comp_pawn4",
                "comp_pawn5", "comp_pawn6", "comp_pawn7", "comp_pawn8"],
            ["comp_bishop1", "", "", "", "", "", "", ""],
            ["", "comp_pawn2", "", "comp_horse2", "", "", "", ""],
            ["", "", "", "", "", "", "", ""],
            ["player_horse1", "", "", "", "", "", "", ""],
            ["player_pawn1", "player_pawn2", "player_pawn3", "player_pawn4",
                "player_pawn5", "player_pawn6", "player_pawn7", "player_pawn8"],
            ["player_rook1", "", "player_bishop1", "player_queen",
                "player_king", "player_bishop2", "player_horse2", "player_rook2"]
        ]

        second_chessboard_matrix = [
            ["comp_rook1", "comp_horse1", "comp_bishop1", "comp_queen",
                "comp_king", "comp_bishop2", "comp_horse2", "comp_rook2"],
            ["comp_pawn1", "comp_pawn2", "comp_pawn3", "comp_pawn4",
                "comp_pawn5", "comp_pawn6", "comp_pawn7", "comp_pawn8"],
            ["", "", "", "", "", "", "", ""],
            ["", "", "", "", "", "", "", ""],
            ["", "", "", "", "", "", "", ""],
            ["player_horse1", "", "", "", "", "", "", ""],
            ["player_pawn1", "player_pawn2", "player_pawn3", "player_pawn4",
                "player_pawn5", "player_pawn6", "player_pawn7", "player_pawn8"],
            ["player_rook1", "", "player_bishop1", "player_queen",
                "player_king", "player_bishop2", "player_horse2", "player_rook2"]
        ]

        expectedResult = ["comp_bishop1", "comp_horse2", "comp_pawn2"]
        differentPieces = self.chess_piece.shrinkContinuosArray(
            self.chess_piece.findMultipleDifferentPieces(
                second_chessboard_matrix, first_chessboard_matrix)
        )

        for i in range(len(differentPieces)):
            if differentPieces[i] != expectedResult[i]:
                self.assertEqual(differentPieces[i], expectedResult[i])

    def testFindBoardCoordinates(self):
        first_chessboard_matrix = [
            ["comp_rook1", "comp_horse1", "comp_bishop1", "comp_queen",
                "comp_king", "comp_bishop2", "comp_horse2", "comp_rook2"],
            ["comp_pawn1", "", "comp_pawn3", "comp_pawn4",
                "comp_pawn5", "comp_pawn6", "comp_pawn7", "comp_pawn8"],
            ["", "", "", "", "", "", "", ""],
            ["", "comp_pawn2", "", "", "", "", "", ""],
            ["", "", "", "", "", "", "", ""],
            ["", "", "", "", "", "", "", ""],
            ["player_pawn1", "player_pawn2", "player_pawn3", "player_pawn4",
                "player_pawn5", "player_pawn6", "player_pawn7", "player_pawn8"],
            ["player_rook1", "player_horse1", "player_bishop1", "player_queen",
                "player_king", "player_bishop2", "player_horse2", "player_rook2"]
        ]

        input2 = "comp_pawn2"
        expectedResult = [3, 1]

        self.assertTrue(self.chess_piece.findBoardCoordinates(
            first_chessboard_matrix, input2))

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
            ["comp_rook1", "comp_horse1", "comp_bishop1", "comp_queen",
                "comp_king", "comp_bishop2", "comp_horse2", "comp_rook2"],
            ["comp_pawn1", "", "comp_pawn3", "comp_pawn4",
                "comp_pawn5", "comp_pawn6", "comp_pawn7", "comp_pawn8"],
            ["", "", "", "", "", "", "", ""],
            ["", "comp_pawn2", "", "", "", "", "", ""],
            ["", "", "", "", "", "", "", ""],
            ["", "", "", "", "", "", "", ""],
            ["player_pawn1", "player_pawn2", "player_pawn3", "player_pawn4",
                "player_pawn5", "player_pawn6", "player_pawn7", "player_pawn8"],
            ["player_rook1", "player_horse1", "player_bishop1", "player_queen",
                "player_king", "player_bishop2", "player_horse2", "player_rook2"]
        ]

        matrixAfter = self.chess_piece.live_chessboard_matrix_gen(
            chess_place_ids, chess_piece_ids)

        for i in range(len(expectedResult)):
            for j in range(len(expectedResult[i])):
                self.assertEqual(matrixAfter[i][j], expectedResult[i][j])
