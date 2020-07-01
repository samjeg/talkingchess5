let chess_place_ids = []
let chess_piece_ids = []

$(document).ready(function(){
	chess_piece_ids = [ 
		"comp_pawn1", "comp_pawn2", "comp_pawn3", "comp_pawn4", "comp_pawn5", "comp_pawn6", "comp_pawn7", "comp_pawn8", 
		"comp_rook1", "comp_horse1", "comp_bishop1", "comp_queen", "comp_king", "comp_bishop2", "comp_horse2", "comp_rook2",
		"player_pawn1", "player_pawn2", "player_pawn3", "player_pawn4", "player_pawn5", "player_pawn6", "player_pawn7", "player_pawn8",
		"player_rook1", "player_horse1", "player_bishop1", "player_queen", "player_king", "player_bishop2", "player_horse2", "player_rook2",
	];

	let new_chessboard_matrix = [
		["comp_rook1", "comp_horse1", "comp_bishop1", "comp_queen", "comp_king", "comp_bishop2", "comp_horse2", "comp_rook2"],
		[ "comp_pawn1", "", "comp_pawn3", "comp_pawn4", "comp_pawn5", "comp_pawn6", "comp_pawn7", "comp_pawn8" ],
		[ "", "", "", "", "", "", "", ""],
		[ "", "", "", "", "", "", "", ""],
		[ "", "comp_pawn2", "", "", "", "", "", ""],
		[ "", "", "", "", "", "", "", ""],
		[ "player_pawn1", "player_pawn2", "player_pawn3", "player_pawn4", "player_pawn5", "player_pawn6", "player_pawn7", "player_pawn8" ],
		["player_rook1", "player_horse1", "player_bishop1", "player_queen", "player_king", "player_bishop2", "player_horse2", "player_rook2"]
	];

	var state = document.getElementById("chess_state").getAttribute('value');
	// state = JSON.stringify(state);
	state = state.replace(/[\[\]']/g, '');
	// state = state + " Hello World";
	// let new_state = Array(8).fill(Array(8).fill(0));
	
	let i = 0;
    
	// state = JSON.stringify(state);
	state =  state.split(",");
	// console.log("state object name: "+state.constructor.name+" ---State---: "+state);
	let new_state = [];
	
    let counter = 0;

	for(let i=0; i<8; i++) {
		let next = [];
		new_state[i] = next; 
		for(let j=0; j<8; j++) {
			new_state[i][j] = state[counter];
			counter++;
		}
	}
	
	

	let chessMech = new ChessMechanics();	
	chess_place_ids = chessMech.chessPiece.get_chess_place_ids(chess_piece_ids);
	chessMech.chessPiece.live_chessboard_matrix = chessMech.chessPiece.live_chessboard_matrix_gen(chess_place_ids, chess_piece_ids);
	let matrixIsSame = chessMech.chessPiece.matrixSame(chessMech.chessPiece.live_chessboard_matrix, new_state);
    let matrix = chessMech.chessPiece.live_chessboard_matrix_gen(chess_place_ids, chess_piece_ids);
	let selectedPlace = null;
	let selectedPiece = null;
	let movedToPlace = null;
	let isSelected = null;
	let hasMoved = null;

	function getLatestState() {
	    chess_place_ids = chessMech.chessPiece.get_chess_place_ids(chess_piece_ids);
		chessMech.chessPiece.live_chessboard_matrix = chessMech.chessPiece.live_chessboard_matrix_gen(chess_place_ids, chess_piece_ids);
	}

	function changePieceLocation(live_matrix, new_chessboard_matrix){
		console.log("New State: "+live_matrix+" ---new_chessboard_matrix---: "+new_chessboard_matrix);
		var diffPiece = chessMech.chessPiece.findDiffentPiece(live_matrix, new_state);
		var diffPieceCoor = chessMech.chessPiece.findBoardCoordinates(new_state, diffPiece);
		var diffPiecePlaceId = chessMech.chessPiece.id_gen(diffPieceCoor[0], diffPieceCoor[1]);
		var diffElement = document.getElementById(diffPiece);
		console.log(diffPiecePlaceId);
		var diffPlaceElement = document.getElementById(diffPiecePlaceId).appendChild(diffElement);
	}

	// $.ajax({
	// 	url: '/chess_app/chessboard/1/',
	// 	method: 'GET', 
	// 	dataType: 'text',
	//     cache: false,
 //        success: function(item){
 //            if(item[0]){
 //                state = item[0];
 //                state2 = item[0].state
 //                state3 = item.state
 //                state4 = item.status_code

 //                console.log("robot movement state: "+state+" "+state2+" "+state3+" "+state4);
 //            }
	// 	},
	// 	error: function() {
	// 		console.log("unable to make get request");
	// 	}
	// });
	
	
	
    
    changePieceLocation(chessMech.chessPiece.live_chessboard_matrix, new_state);

	setInterval(getLatestState, 3000);	

	function robot(id){
		// console.log("robotmovement: "+id);
		console.log("Latest state: "+chess_place_ids);
		console.log("matrix: "+chessMech.chessPiece.live_chessboard_matrix);
		
		user_input_state = document.getElementById("input_state");
		user_input_state.setAttribute("value", chessMech.chessPiece.live_chessboard_matrix.stringify());
		chess_submit_btn = document.getElementById('chess_submit_btn');
		// chess_submit_btn.click();
	}
});




	


