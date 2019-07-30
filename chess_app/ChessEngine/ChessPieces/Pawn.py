from ChessPiece import ChessPiece
from chess_app.ChessEngine.Selecter import Select


class Pawn(ChessPiece):

    def __init__(self):
        super(Pawn, self).__init__()
        self.opponentPlaceIsSetEnPassant = False
        self.opponentPlaceEnPassant = None
        self.placeIsSetEnPassant = False
        self.placeEnPassant = None

    def movablePlaces(self, compPawnStartingPositions, currentEnPassantPlaceId, enPassantOpponentLeft, enPassantOpponentRight, isEnPassant, currentEnPassantOpponentPlaceId, x, y):

        newArray = self.enPassantMovement(
            compPawnStartingPositions,
            currentEnPassantPlaceId,
            enPassantOpponentRight,
            enPassantOpponentLeft,
            isEnPassant,
            currentEnPassantOpponentPlaceId,
            self.shrinkPawnArray(self.getPawnMovablePlaces(x, y), "playing"),
            x,
            y
        )

        return newArray

    # gets the postion of the pawns en passant position if it has been set
    def getEnPassantPlace(self):
        if self.placeIsSetEnPassant:
            self.placeIsSetEnPassant = True
            return self.placeEnPassant

        return None

    # get the position of the opponent enpassant is bieng performed on so opponent can be removed
    def getEnPassantOpponentPlace(self):
        if self.opponentPlaceIsSetEnPassant:
            self.opponentPlaceIsSetEnPassant = False
            return self.opponentPlaceEnPassant

        return None

    # gets all the places that a pawn can move
    def getPawnMovablePlaces(self, x, y):
        matrix = self.live_chessboard_matrix
        placeIds = ["" for a in range(4)]
        if x >= 0 and x <= 7 and y >= 0 and y <= 7:
            rightFwd1Select = Select()
            rightFwd1Element = rightFwd1Select.selectFromParentId(
                matrix, self.id_gen(y+1, x-1))
            leftFwd1Select = Select()
            leftFwd1Element = leftFwd1Select.selectFromParentId(
                matrix, self.id_gen(y+1, x+1))
            fwd1Select = Select()
            fwd1Element = fwd1Select.selectFromParentId(
                matrix, self.id_gen(y+1, x))
            fwd2Select = Select()
            # print("get pawn movable places %s"%self.id_gen(y+2, x))
            fwd2Element = fwd2Select.selectFromParentId(
                matrix, self.id_gen(y+2, x))
        
            if leftFwd1Element != None:
                if leftFwd1Element.piece_id != None and leftFwd1Element != "":
                    leftFwd1Id = leftFwd1Element.piece_id

                    if self.isType(leftFwd1Id, "player_"):
                        placeIds[0] = leftFwd1Element.parent_id

            if rightFwd1Element != None:
                if rightFwd1Element.piece_id != None and rightFwd1Element != "":
                    rightFwd1Id = rightFwd1Element.piece_id
                    if self.isType(rightFwd1Id, "player_"):
                        placeIds[1] = rightFwd1Element.parent_id

            if fwd1Element != None:
                if fwd1Element.piece_id != None and fwd1Element.piece_id == "":
                    placeIds[2] = fwd1Element.parent_id

            if fwd2Element != None:
                if fwd2Element.piece_id != None and fwd2Element.piece_id == "":
                    placeIds[3] = fwd2Element.parent_id
        # print("Pawn %s"%placeIds)
        return placeIds

    #checks if a piece is bieng attacked by the pawn
    def attackingPlaces(self, x, y):
        matrix = self.live_chessboard_matrix
        attackingPawnPlaces = self.shrinkPawnArray(
            self.getPawnMovablePlaces(x, y), "checking")
        new_array = []
        # print("Pawn %s"%attackingPawnPlaces)
        return attackingPawnPlaces

    # no gaps in array so can be used for selection
    def shrinkPawnArray(self, array, mechanic_needed):
        matrix = self.live_chessboard_matrix
        new_array = []

        if mechanic_needed == "playing":

            if array[0] != None:
                if array[0] != "":
                    new_array.append(array[0])

            if array[1] != None:
                if array[1] != "":
                    new_array.append(array[1])

            if array[2] != None:
                if array[2] != "":
                    new_array.append(array[2])

            if array[3] != None:
                if array[3] != "":
                    new_array.append(array[3])

        else:
            if array[0] != None:
                if array[0] != "":
                    new_array.append(array[0])

            if array[1] != None:
                if array[1] != "":
                    new_array.append(array[1])

        return new_array

    # adds the empassant postion if available to the pawns possible moves    
    def enPassantMovement(self, compPawnStartingPositions, currentEnPassantPlaceId, enPassantOpponentLeft, enPassantOpponentRight, isEnPassant, currentEnPassantOpponentPlaceId, pawnArray, x, y):
        matrix = self.live_chessboard_matrix
        newArray = []
        pawnHasLeft = False
        pawnHasRight = False
        leftOfPawn = self.id_gen(y, x-1)
        rightOfPawn = self.id_gen(y, x+1)
        leftOfPawnSelect = Select()
        leftOfPawnElement = leftOfPawnSelect.selectFromParentId(
            matrix, leftOfPawn)
        rightOfPawnSelect = Select()
        rightOfPawnElement = rightOfPawnSelect.selectFromParentId(
            matrix, rightOfPawn)

        if leftOfPawnElement != None:
            if leftOfPawnElement.piece_id != None and leftOfPawnElement.piece_id != "":
                enPassantSpace = self.pawnReadyEnPassant(
                    compPawnStartingPositions,
                    currentEnPassantPlaceId,
                    leftOfPawnElement.piece_id,
                    leftOfPawn
                )

                if enPassantSpace != "":
                    pawnArray.append(enPassantSpace)
                    enPassantOpponentLeft = leftOfPawnElement.piece_id
                    currentEnPassantOpponentPlaceId = leftOfPawn
                    isEnPassant = True
                    self.opponentPlaceIsSetEnPassant = True
                    self.opponentPlaceEnPassant = leftOfPawn

        if rightOfPawnElement != None:
            if rightOfPawnElement.piece_id != None and rightOfPawnElement.piece_id != "":
                enPassantSpace = self.pawnReadyEnPassant(
                    compPawnStartingPositions,
                    currentEnPassantPlaceId,
                    rightOfPawnElement.piece_id,
                    rightOfPawn
                )

                if enPassantSpace != "":
                    pawnArray.append(enPassantSpace)
                    enPassantOpponentRight = rightOfPawnElement.piece_id
                    currentEnPassantOpponentPlaceId = rightOfPawn
                    isEnPassant = True
                    self.opponentPlaceIsSetEnPassant = True
                    self.opponentPlaceEnPassant = rightOfPawn

            return pawnArray

    # checks if the pawn is ready for enpassant
    def pawnReadyEnPassant(self, compPawnStartingPositions, currentEnPassantPlaceId, pieceId, placeId):
        newPlaceId = ""

        if self.isType(pieceId, "player_pawn"):
            for i in range(len(compPawnStartingPositions)):
                if self.isType(pieceId, str(i+1)):
                    posBefore = self.findPlaceCoordinates(
                        compPawnStartingPositions[i])
                    y = posBefore[0] + 1
                    x = posBefore[1]
                    posNow = self.findPlaceCoordinates(placeId)
                    nY = posNow[0] - 1
                    nX = posNow[1]
                    placeIdWithPosBefore = self.id_gen(y, x)
                    placeIdWithPosNow = self.id_gen(nY, nX)

                    if placeIdWithPosBefore == placeIdWithPosNow:
                        newPlaceId = placeIdWithPosNow
                        currentEnPassantPlaceId = placeIdWithPosNow
                        self.placeIsSetEnPassant = True
                        self.placeEnPassant = placeIdWithPosNow

        return newPlaceId
