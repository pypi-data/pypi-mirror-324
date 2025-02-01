mapOfSymbols = {
    "BE": '♖',  # White Rook
    "BN": '♘',  # White Knight
    "BB": '♗',  # White Bishop
    "BQ": '♕',  # White Queen
    "BK": '♔',  # White King
    "BP": '♙',  # White Pawn
    "WE": '♜',  # Black Rook
    "WN": '♞',  # Black Knight
    "WB": '♝',  # Black Bishop
    "WQ": '♛',  # Black Queen
    "WK": '♚',  # Black King
    "WP": '♟',  # Black Pawn
    "E": '.'    # Empty square (optional)
}


def generateBoard(board):
    generatedBoard = []
    for i in range(8):
        aRow = []
        for j in range(8):
            aRow.append( mapOfSymbols[ str(board[i][j]) ] )
        generatedBoard.append( aRow )
    return generatedBoard