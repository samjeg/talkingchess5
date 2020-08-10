let ChessMechanics_ = null;
let robot = null;

$(document).ready(function() {
	let chess_piece_ids = [ 
		"comp_pawn1", "comp_pawn2", "comp_pawn3", "comp_pawn4", "comp_pawn5", "comp_pawn6", "comp_pawn7", "comp_pawn8", 
		"comp_rook1", "comp_horse1", "comp_bishop1", "comp_queen", "comp_king", "comp_bishop2", "comp_horse2", "comp_rook2",
		"player_pawn1", "player_pawn2", "player_pawn3", "player_pawn4", "player_pawn5", "player_pawn6", "player_pawn7", "player_pawn8",
		"player_rook1", "player_horse1", "player_bishop1", "player_queen", "player_king", "player_bishop2", "player_horse2", "player_rook2",
	];

	let matrix = [
		["comp_rook1", "comp_horse1", "comp_bishop1", "comp_queen", "comp_king", "comp_bishop2", "comp_horse2", "comp_rook2"],
		["comp_pawn1", "comp_pawn2", "comp_pawn3", "comp_pawn4", "comp_pawn5", "comp_pawn6", "comp_pawn7", "comp_pawn8" ],
		["", "", "", "", "", "", "", ""],
		["", "", "", "", "", "", "", ""],
		["", "", "", "", "", "", "", ""],
		["", "", "", "", "", "", "", ""],
		["player_pawn1", "player_pawn2", "player_pawn3", "player_pawn4", "player_pawn5", "player_pawn6", "player_pawn7", "player_pawn8" ],
		["player_rook1", "player_horse1", "player_bishop1", "player_queen", "player_king", "player_bishop2", "player_horse2", "player_rook2"]
	];

    ChessMechanics_ = new ChessMechanics();
	let chess_place_ids = ChessMechanics_.chessPiece.get_chess_place_ids(chess_piece_ids);
	ChessMechanics_.chessPiece.live_chessboard_matrix = ChessMechanics_.chessPiece.live_chessboard_matrix_gen(chess_place_ids, chess_piece_ids);
 
    current_matrix = []
	var state = document.getElementById("chess_state").getAttribute('value');

	if(state !== "") { 
		state = state.replace(/[\[\]']/g, '');

		state =  state.split(",");
		let current_matrix = [];

		let counter = 0;

		for(let i=0; i<8; i++) {
			let next = [];
			current_matrix[i] = next; 
			for(let j=0; j<8; j++) {
				state[counter] = state[counter].replace(/\s+/g, '');
				current_matrix[i][j] = state[counter];
				counter++;
			}
		}
	}

	function getLatestState() {	
		
		let temp_matrix = [
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

				temp_matrix[row_num][col_num] = chess_piece_ids[i];
				if(chess_piece_ids[i] === "player_pawn2") {
				    console.log("robot mvment getlateststate - row: "+row_num+" col: "+col_num);
				}
			}
		}
		
		return temp_matrix;
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
		let count = 0;
		new_matrix[0] = JSON.parse(window.localStorage.getItem("row0"));
        if(new_matrix[0] != null) {
	        if (new_matrix[0].length == 8) {
	        	count++;
	        }
	    }
		new_matrix[1] = JSON.parse(window.localStorage.getItem("row1"));
		if(new_matrix[1] != null) {
	        if (new_matrix[1].length == 8) {
	        	count++;
	        }
	    }
		new_matrix[2] = JSON.parse(window.localStorage.getItem("row2"));
		if(new_matrix[2] != null) {
	        if (new_matrix[2].length == 8) {
	        	count++;
	        }
	    }
		new_matrix[3] = JSON.parse(window.localStorage.getItem("row3"));
		if(new_matrix[3] != null) {
	        if (new_matrix[3].length == 8) {
	        	count++;
	        }
	    }
		new_matrix[4] = JSON.parse(window.localStorage.getItem("row4"));
		if(new_matrix[4] != null) {
	        if (new_matrix[4].length == 8) {
	        	count++;
	        }
	    }
		new_matrix[5] = JSON.parse(window.localStorage.getItem("row5"));
		if(new_matrix[5] != null) {
	        if (new_matrix[5].length == 8) {
	        	count++;
	        }
	    }
		new_matrix[6] = JSON.parse(window.localStorage.getItem("row6"));
		if(new_matrix[6] != null) {
	        if (new_matrix[6].length == 8) {
	        	count++;
	        }
	    }
		new_matrix[7] = JSON.parse(window.localStorage.getItem("row7"));
		if(new_matrix[7] != null) {
	        if (new_matrix[7].length == 8) {
	        	count++;
	        }
	    }
		return count;
	}

	function checkFullMatrix(new_matrix) {
		let count = 0;
		
		if(new_matrix != null) {
			if(new_matrix.length == 8) {
		        if(new_matrix[0] != null) {
			        if (new_matrix[0].length == 8) {
			        	count++;
			        }
			    }
				
				if(new_matrix[1] != null) {
			        if (new_matrix[1].length == 8) {
			        	count++;
			        }
			    }
				if(new_matrix[2] != null) {
			        if (new_matrix[2].length == 8) {
			        	count++;
			        }
			    }
				if(new_matrix[3] != null) {
			        if (new_matrix[3].length == 8) {
			        	count++;
			        }
			    }
				if(new_matrix[4] != null) {
			        if (new_matrix[4].length == 8) {
			        	count++;
			        }
			    }
				if(new_matrix[5] != null) {
			        if (new_matrix[5].length == 8) {
			        	count++;
			        }
			    }
				if(new_matrix[6] != null) {
			        if (new_matrix[6].length == 8) {
			        	count++;
			        }
			    }
				if(new_matrix[7] != null) {
			        if (new_matrix[7].length == 8) {
			        	count++;
			        }
			    }
			}
		}
		return count;
	}

	function removeState() {
		window.localStorage.removeItem("row0");
		window.localStorage.removeItem("row1");
		window.localStorage.removeItem("row2");
		window.localStorage.removeItem("row3");
		window.localStorage.removeItem("row4");
		window.localStorage.removeItem("row5");
		window.localStorage.removeItem("row6");
		window.localStorage.removeItem("row7");
	}

	function SetOnPlayerMove(type_of_player, new_matrix, old_matrix) {
        let original_positions = [];
        let new_positions = [];
        let counter = 0;
        let set = new Set();
        
        // get all the player pieces in original state
		for(let i=0; i<old_matrix.length; i++) {
			if(old_matrix[i] != null) {
				for(let j=0; j<old_matrix[i].length; j++) {
					if(ChessMechanics_.chessPiece.isType(old_matrix[i][j], type_of_player)) {
					    original_positions.push(ChessMechanics_.chessPiece.id_gen(i, j));
					}
				}
			}
		}
        
        // get all the player pieces in the new state
		for(let i=0; i<new_matrix.length; i++) {
			if(new_matrix[i] != null) {
				for(let j=0; j<new_matrix[i].length; j++) {
					if(ChessMechanics_.chessPiece.isType(new_matrix[i][j], type_of_player)) {
					    new_positions.push(ChessMechanics_.chessPiece.id_gen(i, j));
					}
				}
			}
		}
        
        // count the positions that are the same 
		for(let i=0; i<original_positions.length; i++) {
			for(let j=0; j<new_positions.length; j++) {
	            if(!set.has(j)) {
	            	if(original_positions[i] === new_positions[j]) {
	            		set.add(j);
	            		counter++;
	            	}
	            }
			}
		}

        console.log("robotmovement count: "+counter+" orig pos len: "+original_positions.length);
        // if the state hs changed from player movement stop player from moving
		if(counter == original_positions.length - 1 && type_of_player === "player") {
			ChessMechanics_.playerCanMove = false;
			ChessMechanics_.robotCanMove = true;
			$input_state = $("#input_state");
			$input_state.attr("value", new_matrix);
			chess_submit_btn = $('#chess_submit_btn');
			let state_sent = localStorage.getItem("state sent");
			if(state_sent === "n") {
				chess_submit_btn.click();
				localStorage.setItem("state sent", "y");
			}
			storeNewState(new_matrix);
			console.log("player state sent");
		} else if(counter == original_positions.length - 1 && type_of_player === "comp") {
			ChessMechanics_.robotCanMove = false;
			ChessMechanics_.playerCanMove = true;
			let state_sent = localStorage.getItem("state sent");
			if(state_sent === "y") {
				localStorage.setItem("state sent", "n");
			}
			storeNewState(new_matrix);
		}
	}

	function playerMove() {
		console.log("player can move: "+ChessMechanics_.playerCanMove+" robot can move: "+ChessMechanics_.robotCanMove);
		if(ChessMechanics_.playerCanMove == true) {
	        let initial_state = [
				["comp_rook1", "comp_horse1", "comp_bishop1", "comp_queen", "comp_king", "comp_bishop2", "comp_horse2", "comp_rook2"],
				["comp_pawn1", "comp_pawn2", "comp_pawn3", "comp_pawn4", "comp_pawn5", "comp_pawn6", "comp_pawn7", "comp_pawn8" ],
				["", "", "", "", "", "", "", ""],
				["", "", "", "", "", "", "", ""],
				["", "", "", "", "", "", "", ""],
				["", "", "", "", "", "", "", ""],
				["player_pawn1", "player_pawn2", "player_pawn3", "player_pawn4", "player_pawn5", "player_pawn6", "player_pawn7", "player_pawn8" ],
				["player_rook1", "player_horse1", "player_bishop1", "player_queen", "player_king", "player_bishop2", "player_horse2", "player_rook2"]
			];

		    let initial_state2 = [
				["comp_rook1", "comp_horse1", "comp_bishop1", "comp_queen", "comp_king", "comp_bishop2", "comp_horse2", "comp_rook2"],
				["comp_pawn1", "comp_pawn2", "comp_pawn3", "comp_pawn4", "comp_pawn5", "comp_pawn6", "comp_pawn7", "comp_pawn8" ],
				["", "", "", "", "", "", "", ""],
				["", "", "", "", "", "", "", ""],
				["", "", "", "", "", "", "", ""],
				["", "", "", "", "", "", "", ""],
				["player_pawn1", "player_pawn2", "player_pawn3", "player_pawn4", "player_pawn5", "player_pawn6", "player_pawn7", "player_pawn8" ],
				["player_rook1", "player_horse1", "player_bishop1", "player_queen", "player_king", "player_bishop2", "player_horse2", "player_rook2"]
			];
		
            let old_state = [];
			// get the old state if it exists   
	        let fullCount = unPackState(initial_state);
	        console.log("robotmovement plyer move full count: "+fullCount);
	        if(fullCount == 8) {
	        	old_state = initial_state;
	        } else {
	        	old_state = initial_state2;
	        }

	        // get the latest state possibly after a move 
	        let new_state = getLatestState();
	        let new_full_count = checkFullMatrix(new_state);
	        console.log("robotmovement player move new state count: "+new_full_count);
            // console.log("robotmovement playermove old state len: "+old_state.length+" new state len: "+new_state.length+" old state 0: "+old_state[0].length);
	        // change state current state after got latest move 
            if(new_state != null && old_state != null) {
		        if(new_state.length > 0 && old_state.length > 0) {
			        SetOnPlayerMove("player", new_state, old_state);	  
			    }
		    }
        }  
	}

	function robotMove() {
		if(ChessMechanics_.robotCanMove == true) {
			let initial_state = [
				["comp_rook1", "comp_horse1", "comp_bishop1", "comp_queen", "comp_king", "comp_bishop2", "comp_horse2", "comp_rook2"],
				["comp_pawn1", "comp_pawn2", "comp_pawn3", "comp_pawn4", "comp_pawn5", "comp_pawn6", "comp_pawn7", "comp_pawn8" ],
				["", "", "", "", "", "", "", ""],
				["", "", "", "", "", "", "", ""],
				["", "", "", "", "", "", "", ""],
				["", "", "", "", "", "", "", ""],
				["player_pawn1", "player_pawn2", "player_pawn3", "player_pawn4", "player_pawn5", "player_pawn6", "player_pawn7", "player_pawn8" ],
				["player_rook1", "player_horse1", "player_bishop1", "player_queen", "player_king", "player_bishop2", "player_horse2", "player_rook2"]
			];

		    let initial_state2 = [
				["comp_rook1", "comp_horse1", "comp_bishop1", "comp_queen", "comp_king", "comp_bishop2", "comp_horse2", "comp_rook2"],
				["comp_pawn1", "comp_pawn2", "comp_pawn3", "comp_pawn4", "comp_pawn5", "comp_pawn6", "comp_pawn7", "comp_pawn8" ],
				["", "", "", "", "", "", "", ""],
				["", "", "", "", "", "", "", ""],
				["", "", "", "", "", "", "", ""],
				["", "", "", "", "", "", "", ""],
				["player_pawn1", "player_pawn2", "player_pawn3", "player_pawn4", "player_pawn5", "player_pawn6", "player_pawn7", "player_pawn8" ],
				["player_rook1", "player_horse1", "player_bishop1", "player_queen", "player_king", "player_bishop2", "player_horse2", "player_rook2"]
			];

			let old_state = [];
			// get the old state if it exists   
	        let fullCount = unPackState(initial_state);
	        if(fullCount == 8) {
	        	old_state = initial_state;
	        } else {
	        	old_state = initial_state2;
	        }

	        // render the chessboard after robot move 
	    	changeMultiplePieceLocations(old_state, current_matrix);	

	        // get the latest state possibly robot after a move 
	        let new_state = getLatestState();
		    let new_full_count = checkFullMatrix(new_state);
		    console.log("robotmovement robotmove new state count: "+new_full_count);
	        // change state current state after got latest move 
	        if(new_state != null && old_state != null) {
		        if(full_count == 8 && new_full_count == 8) {
			        SetOnPlayerMove("robot", new_state, old_state);	  
			    }
		    }   
        }
	}

	setInterval(playerMove, 3000);
	setInterval(robotMove, 3000);


	function changeMultiplePieceLocations(live_matrix, new_chessboard_matrix){
		ChessMechanics_.playerCanMove = false;
		ChessMechanics_.robotCanMove = true;
		var diffPieces = ChessMechanics_.chessPiece.shrinkContinuosArray(
	 		ChessMechanics_.chessPiece.findMultipleDifferentPieces(live_matrix, new_chessboard_matrix));

		for(var i=0; i<diffPieces.length; i++){
	 		var diffPiece = diffPieces[i];
		 	if(diffPiece !== "") {	
		 		var diffPieceCoor = ChessMechanics_.chessPiece.findBoardCoordinates(new_chessboard_matrix, diffPiece);
				var diffPiecePlaceId = ChessMechanics_.chessPiece.id_gen(diffPieceCoor[0], diffPieceCoor[1]);
				var diffElement = document.getElementById(diffPiece);
				var diffPlaceElement = document.getElementById(diffPiecePlaceId).appendChild(diffElement);
			}
	 	}
	 	ChessMechanics_.playerCanMove = true;
		ChessMechanics_.robotCanMove = false;
	}

	robot = function robot(id) {}
});




	


