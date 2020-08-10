from .Selecter import Select 
from .ChessPieces.ChessPiece import ChessPiece
from .ChessPieces.Horse import Horse
from .ChessPieces.Rook import Rook
from .ChessPieces.Bishop import Bishop
from .ChessPieces.Queen import Queen
from .ChessPieces.Pawn import Pawn
from .ChessPieces.King import King
from .Selecter import Select
from .CheckerGetter import CheckerGetter
from .ChessMechanics import ChessMechanics
import random

class RobotMovement(object):

    def __init__(self):
        self.chess_mech = ChessMechanics()
        self.chess_piece = ChessPiece()
        self.current_chess_piece_ids = []
        self.pawn = Pawn()
        self.movable_places = []
        self.comp_pieces = []
        self.next_piece = ""

 

    # Returns the ids of the chess pieces currently on the board
    def getChessPieces(self, matrix):
        array = []

        for i in range(8):
            for j in range(8):
                if self.chess_piece.isType(matrix[i][j], "comp_") or self.chess_piece.isType(matrix[i][j], "player_"):
                    array.append(matrix[i][j])

        return array

    # Updates current_chess_piece_ids being tracked by this robot object
    def updateChessPieces(self, matrix):
        for i in range(8):
            for j in range(8):
                if self.chess_piece.isType(matrix[i][j], "comp_") or self.chess_piece.isType(matrix[i][j], "player_"):
                    self.current_chess_piece_ids.append(matrix[i][j])   


    # Returns true if it can't find a piece from the old chessboard state in the new chessboard
    def pieceIsMissing(self, new_matrix):
        
        old_chess_pieces = self.current_chess_piece_ids
        new_chess_pieces = self.getChessPieces(new_matrix)
        old_chess_pieces_length = len(old_chess_pieces)
        new_chess_pieces_length = len(new_chess_pieces)
        diff = old_chess_pieces_length - new_chess_pieces_length


        if diff == 1:
            return True

        if diff > 1:
            print("Looks like more than a single piece was found, this is most likely an Error")
            return False
        
        return False    


    # Returns the missing piece that was gone from the old chessboard state so can assign points for capturing  
    def getMissingPiece(self, new_matrix):
        
        old_chess_pieces = self.current_chess_piece_ids
        new_chess_pieces = self.getChessPieces(new_matrix)
        missing_piece = ""
        pos = 0

        for i in range(len(old_chess_pieces)):
            current_piece_found = True 
            j = 0 
            
            for j in range(len(new_chess_pieces)):
                if old_chess_pieces[i] == new_chess_pieces[j]:
                    break

            if len(new_chess_pieces) == (j + 1):
                missing_piece = old_chess_pieces[i]
                break

            
        return missing_piece

    # Collects the points of the from taking the missing piece
    def getPoints(self, piece):
        points = 0

        if self.chess_piece.isType(piece, "pawn"):
            points = 10

        elif self.chess_piece.isType(piece, "bishop"):
            points = 30

        elif self.chess_piece.isType(piece, "horse"):
            points = 30

        elif self.chess_piece.isType(piece, "rook"):
            points = 50

        elif self.chess_piece.isType(piece, "queen"):
            points = 90


        if self.chess_piece.isType(piece, "comp"):
            points = - points

        return points


    
    def playRandomMove(self, matrix):
        self.comp_pieces =  [ 
          "comp_rook1", "comp_horse1", "comp_bishop1", "comp_queen", "comp_king", "comp_bishop2", "comp_horse2", "comp_rook2",
          "comp_pawn1", "comp_pawn2", "comp_pawn3", "comp_pawn4", "comp_pawn5", "comp_pawn6", "comp_pawn7", "comp_pawn8", 
        ]
        selected_pieces = []
        movablePlaces = []
        # print("robot movement play random 1")
        self.chess_mech.chessPiece.live_chessboard_matrix = matrix
        # print("robot movement play random 2")
        print("robot move playrand before %s %s"%(matrix, selected_pieces))
        self.next_piece = self.getMovablePiece(matrix, selected_pieces)  
        # print("robot movement play random 3")
        
        place = random.choice(self.movable_places)
        # print("robot movement play random 4")
        self.chess_mech.moveTo(place)
        # print("robot move playrand move to %s"%self.chess_mech.chessPiece.live_chessboard_matrix)
        # print("robot movement play random 5")
        new_coordinates = []

        new_matrix = self.chess_mech.chessPiece.live_chessboard_matrix
        # print("robot movement play random 6")
        # print("robot move playrand after %s"%self.chess_mech.chessPiece.live_chessboard_matrix)
        
        for k in range(8):
            # print("robot movement play random 7")
            for l in range(8):
                # print("robot movement play random 8")
                if new_matrix[k][l] == self.next_piece:
                    # print("robot movement play random 9")
                    new_matrix[k][l] = ''


        # print("robot movement play random 10")
        for n in range(8):
            # print("robot movement play random 11")
            for m in range(8):
                # print("robot movement play random 12")
                next_val = new_matrix[n][m]
                # print("robot movement play random 13")
                if isinstance(next_val, Select):
                    # print("robot movement play random 14")
                    new_place = self.chess_piece.id_gen(n, m)
                    new_matrix[n][m] = self.next_piece
       
        return new_matrix



    def pickUnSelected(self, selected_pieces, piece):
        length = len(selected_pieces)
        i = 0
        # print("robot movement pick unselected 1")

        for i in range(len(selected_pieces)):
            # print("robot movement pick unselected 2")
            if selected_pieces[i] == piece:
                # print("robot movement pick unselected 3")
                self.comp_pieces.remove(piece)
                # print("robot movement pick unselected 4")
                piece = random.choice(self.comp_pieces)
                # print("robot movement pick unselected 5")
                break;
        # print("robot movement pick unselected 6")
        selected_pieces.append(piece)
        # print("robot movement pick unselected 7")
        return piece
                    
        
    def getMovablePiece(self, matrix, selected_pieces):
        # print("robot movement movable piece 1")
        piece = ""
        while len(self.movable_places) == 0:
            # print("robot movement movable piece 2")
            piece = random.choice(self.comp_pieces)
            # print("robot movement movable piece 3")
            piece = self.pickUnSelected(selected_pieces, piece)
    
            firstCoor = 0
            secCoor = 0   
            # print("robot movement movable piece 4")         
            for i in range(len(matrix)):
                # print("robot movement movable piece 5")
                for j in range(len(matrix[i])):
                    # print("robot movement movable piece 6")
                    if matrix[i][j] == piece:
                        # print("robot movement movable piece 7")
                        firstCoor = i
                        secCoor = j
                        coordinates = [i, j]
            
            # print("robot movement movable piece 8")
            self.chess_mech.select(piece)   
            # print("robot movement movable piece 9")    
            self.movable_places = self.chess_mech.getMovable(piece, secCoor, firstCoor)
            # print("robot movement movable piece 10")

            if len(self.comp_pieces) == 0:
                # print("robot movement movable piece 11")
                break

            # print("robot movement movable piece 12")
        
        return piece
        



