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
    
        self.next_piece = self.getMovablePiece(matrix, selected_pieces)  
        print("RobotMovement playRandomMove getMovablePiece piece %s %s"%(self.next_piece, self.getMovablePiece(matrix, selected_pieces)))
        place = random.choice(self.movable_places)
        self.chess_mech.moveTo(place)

        new_coordinates = []

        new_matrix = self.chess_mech.chessPiece.live_chessboard_matrix
        
        for k in range(8):
            for l in range(8):
                if new_matrix[k][l] == self.next_piece:
                    new_matrix[k][l] = ''


           
        for n in range(8):
            for m in range(8):
                next_val = new_matrix[n][m]
                if isinstance(next_val, Select):
                    new_place = self.chess_piece.id_gen(n, m)
                    new_matrix[n][m] = self.next_piece
        print("RobotMovement playRandomMove last piece %s"%self.next_piece)
        # print("piece: %s place: %s confirm place: %s matrix: %s"%(piece, place, new_place, new_matrix))

        return new_matrix



    def pickUnSelected(self, selected_pieces, piece):
        length = len(selected_pieces)
        i = 0
        while length != 0 and i < length:
            for i in range(len(selected_pieces)):
                if selected_pieces[i] == piece:
                    self.comp_pieces.remove(piece) # Remove pieces from the comp_pieces array
                    piece = random.choice(self.comp_pieces)
                    break;

        selected_pieces.append(piece)
        return piece
                    
        
    def getMovablePiece(self, matrix, selected_pieces):
        self.chess_mech.chessPiece.live_chessboard_matrix = matrix
        piece = ""
        while len(self.movable_places) == 0:
            piece = random.choice(self.comp_pieces)
            piece = self.pickUnSelected(selected_pieces, piece)
    
            firstCoor = 0
            secCoor = 0            
            for i in range(len(matrix)):
                for j in range(len(matrix[i])):
                    if matrix[i][j] == piece:
                        firstCoor = i
                        secCoor = j
                        coordinates = [i, j]
            
            
            self.chess_mech.select(piece)       
            self.movable_places = self.chess_mech.getMovable(piece, secCoor, firstCoor)

            if len(self.comp_pieces) == 0:
                break
        
        return piece
        
        




