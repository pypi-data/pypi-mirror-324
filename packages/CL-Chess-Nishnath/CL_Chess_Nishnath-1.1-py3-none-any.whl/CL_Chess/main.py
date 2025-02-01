from .functions.printBoard import printBoard
from .functions.askUserToGiveInput import askUserToGiveInput
from .functions.makeCoinFtoT import makeCoinFtoT
from .functions.printGameOver import printGameOver
from .functions.printWinPlayer import printWin
from .functions.isValidMove import isValidMove

def main():
    # Initial board
    board = [
        ['WE', 'WN', 'WB', 'WQ', 'WK', 'WB', 'WN', 'WE'],  # White pieces
        ['WP', 'WP', 'WP', 'WP', 'WP', 'WP', 'WP', 'WP'],  # White Pawns
        ['E', 'E', 'E', 'E', 'E', 'E', 'E', 'E'],  # Empty row
        ['E', 'E', 'E', 'E', 'E', 'E', 'E', 'E'],  # Empty row
        ['E', 'E', 'E', 'E', 'E', 'E', 'E', 'E'],  # Empty row
        ['E', 'E', 'E', 'E', 'E', 'E', 'E', 'E'],  # Empty row
        ['BP', 'BP', 'BP', 'BP', 'BP', 'BP', 'BP', 'BP'],  # White Pawns
        ['BE', 'BN', 'BB', 'BQ', 'BK', 'BB', 'BN', 'BE']   # Black pieces
    ]

    # Turn and GameOver Flage
    turn = "White"
    gameOver = False

    # loop until the game is Over
    while not gameOver:
        #Convert the bord to symboles and print it
        printBoard(board)
        #takes user input and validate 
        f,t = askUserToGiveInput(turn,board)
        # checking the user move is valid or not
        if( isValidMove(f,t,board) ):
            #checks for game over condition
            if( len(board[int(t[0])][int(t[1])])==2  and board[int(t[0])][int(t[1])][1]=="K" ):
                break
            #makeing coin to move from f to t
            makeCoinFtoT(f,t,board)
            #togleing the turn between white and black
            turn = "Black" if turn=="White" else "White"

    # printing game Over
    printGameOver()

    #print win
    printWin(turn)

    #print "NISHNATH"
    print("Nishnath 🫶")
