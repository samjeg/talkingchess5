let robot = null;
let stateHasChanged = false;
let robotHasMoved = false;
let playerHasMoved = true;
let ChessMechanics_ = null;
let playerMovable = null;

$(document).ready(function() {
	let chess_piece_ids = [ 
		"comp_pawn1", "comp_pawn2", "comp_pawn3", "comp_pawn4", "comp_pawn5", "comp_pawn6", "comp_pawn7", "comp_pawn8", 
		"comp_rook1", "comp_horse1", "comp_bishop1", "comp_queen", "comp_king", "comp_bishop2", "comp_horse2", "comp_rook2",
		"player_pawn1", "player_pawn2", "player_pawn3", "player_pawn4", "player_pawn5", "player_pawn6", "player_pawn7", "player_pawn8",
		"player_rook1", "player_horse1", "player_bishop1", "player_queen", "player_king", "player_bishop2", "player_horse2", "player_rook2",
	];

	let new_chessboard_matrix = [
		["comp_rook1", "comp_horse1", "comp_bishop1", "comp_queen", "comp_king", "comp_bishop2", "comp_horse2", "comp_rook2"],
		["comp_pawn1", "comp_pawn2", "comp_pawn3", "comp_pawn4", "comp_pawn5", "comp_pawn6", "comp_pawn7", "comp_pawn8" ],
		["", "", "", "", "", "", "", ""],
		["", "", "", "", "", "", "", ""],
		["", "", "", "", "", "", "", ""],
		["", "", "", "", "", "", "", ""],
		["player_pawn1", "player_pawn2", "player_pawn3", "player_pawn4", "player_pawn5", "player_pawn6", "player_pawn7", "player_pawn8" ],
		["player_rook1", "player_horse1", "player_bishop1", "player_queen", "player_king", "player_bishop2", "player_horse2", "player_rook2"]
	];
	
	let mat = [];
	console.log(window.localStorage.length == 0);
	
	let original_state = new_chessboard_matrix;
	var state = document.getElementById("chess_state").getAttribute('value');
	state = state.replace(/[\[\]']/g, '');

	state =  state.split(",");
	let new_state = [];

	let counter = 0;

	for(let i=0; i<8; i++) {
		let next = [];
		new_state[i] = next; 
		for(let j=0; j<8; j++) {
			state[counter] = state[counter].replace(/\s+/g, '');
			new_state[i][j] = state[counter];
			counter++;
		}
	}

    ChessMechanics_ = new ChessMechanics();
	let chess_place_ids = ChessMechanics_.chessPiece.get_chess_place_ids(chess_piece_ids);
	ChessMechanics_.chessPiece.live_chessboard_matrix = ChessMechanics_.chessPiece.live_chessboard_matrix_gen(chess_place_ids, chess_piece_ids);
	let matrixIsSame = ChessMechanics_.chessPiece.matrixSame(ChessMechanics_.chessPiece.live_chessboard_matrix, new_state);
	let matrix = ChessMechanics_.chessPiece.live_chessboard_matrix_gen(chess_place_ids, chess_piece_ids);
	let selectedPlace = null;
	let selectedPiece = null;
	let movedToPlace = null;
	let isSelected = null;
	let hasMoved = null;

	function getLatestState() {	
		let live_matrix = [
			["", "", "", "", "", "", "", ""],
			["", "", "", "", "", "", "", ""],
			["", "", "", "", "", "", "", ""],
			["", "", "", "", "", "", "", ""],
			["", "", "", "", "", "", "", ""],
			["", "", "", "", "", "", "", ""],
			["", "", "", "", "", "", "", ""],
			["", "", "", "", "", "", "", ""]
		];
		
		for(var i=0; i<chess_piece_ids.length; i++){
			if(document.getElementById(chess_piece_ids[i])!=null){
				let place_id = document.getElementById(chess_piece_ids[i]).parentElement.id;
				let firstAttr = place_id[0];
				let secAttr = place_id[1];
				let row_num = ChessMechanics_.chessPiece.first_coordinate_gen(firstAttr);
				let col_num = ChessMechanics_.chessPiece.second_coordinate_gen(secAttr);

				live_matrix[row_num][col_num] = chess_piece_ids[i];
				ChessMechanics_.chessPiece.live_chessboard_matrix = live_matrix;
			}
		}

		if(i == chess_piece_ids.length) {
			console.log("all pieces completed");
		} else {
			console.log("pieces not completed");
		}   
	}

	function storeNewState(matrix) {
		window.localStorage.setItem("row0", JSON.stringify(matrix[0]));
		window.localStorage.setItem("row1", JSON.stringify(matrix[1]));
		window.localStorage.setItem("row2", JSON.stringify(matrix[2]));
		window.localStorage.setItem("row3", JSON.stringify(matrix[3]));
		window.localStorage.setItem("row4", JSON.stringify(matrix[4]));
		window.localStorage.setItem("row5", JSON.stringify(matrix[5]));
		window.localStorage.setItem("row6", JSON.stringify(matrix[6]));
		window.localStorage.setItem("row7", JSON.stringify(matrix[7]));
	}

	function unPackState(new_matrix) {
		new_matrix[0] = JSON.parse(window.localStorage.getItem("row0"));
		new_matrix[1] = JSON.parse(window.localStorage.getItem("row1"));
		new_matrix[2] = JSON.parse(window.localStorage.getItem("row2"));
		new_matrix[3] = JSON.parse(window.localStorage.getItem("row3"));
		new_matrix[4] = JSON.parse(window.localStorage.getItem("row4"));
		new_matrix[5] = JSON.parse(window.localStorage.getItem("row5"));
		new_matrix[6] = JSON.parse(window.localStorage.getItem("row6"));
		new_matrix[7] = JSON.parse(window.localStorage.getItem("row7"));
	}

    // toggle player can move
	playerMovable = function playerMovable() {
	    if(ChessMechanics_.playerCanMove == false) {
	    	ChessMechanics_.playerCanMove = true;
	    } else {
	    	ChessMechanics_.playerCanMove = false;
	    }
	}

	// changes the chessboard with the different piece from the state 
	// function changePieceLocation(live_matrix, new_chess_matrix) {
	// 	var diffPiece = ChessMechanics_.chessPiece.findDiffentPiece(live_matrix, new_chess_matrix);
	// 	var diffPieceCoor = ChessMechanics_.chessPiece.findBoardCoordinates(new_chess_matrix, diffPiece);
	// 	var diffPiecePlaceId = ChessMechanics_.chessPiece.id_gen(diffPieceCoor[0], diffPieceCoor[1]);
	// 	var diffElement = document.getElementById(diffPiece);
	// 	var diffPlaceElement = document.getElementById(diffPiecePlaceId).appendChild(diffElement);
	// 	ChessMechanics_.chessPiece.live_chessboard_matrix = new_chess_matrix;
	// 	console.log("robot movement change piece location: "+ChessMechanics_.chesssPie.live_chessboard_matrix);
	// }

	// updates the front end with the changed state for all the pieces on the chessboard
	function changeMultiplePieceLocations(live_matrix, new_chessboard_matrix){
		var diffPieces = ChessMechanics_.chessPiece.shrinkContinuosArray(
	 		ChessMechanics_.chessPiece.findMultipleDifferentPieces(live_matrix, new_chessboard_matrix));

		for(var i=0; i<diffPieces.length; i++){
	 		var diffPiece = diffPieces[i];
		 	if(diffPiece === "") {	
		 		var diffPieceCoor = ChessMechanics_.chessPiece.findBoardCoordinates(new_chessboard_matrix, diffPiece);
				var diffPiecePlaceId = ChessMechanics_.chessPiece.id_gen(diffPieceCoor[0], diffPieceCoor[1]);
				var diffElement = document.getElementById(diffPiece);
				var diffPlaceElement = document.getElementById(diffPiecePlaceId).appendChild(diffElement);
			}
	 	}
	}

	changeMultiplePieceLocations(ChessMechanics_.chessPiece.live_chessboard_matrix, new_state);	

	robot = function robot(id){
		// ChessMechanics_.robotCanMove = true;
		current_player_type = $("#current_player_type");
		current_player_type.attr("value", "robot");
		console.log("current player type: "+current_player_type.val());
		// user_input_state = $("#input_state");
		// getLatestState();
		// user_input_state.attr("value", JSON.stringify(ChessMechanics_.chessPiece.live_chessboard_matrix));
		// chess_submit_btn = $('#chess_submit_btn');
		// ChessMechanics_.robotCanMove = false;
	}	
});




	


