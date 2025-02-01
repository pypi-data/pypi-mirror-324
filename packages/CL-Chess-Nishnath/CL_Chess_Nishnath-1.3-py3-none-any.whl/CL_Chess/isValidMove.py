from .moveDiagram import moveDiagram
from .stepsCountDiagram import stepsCountDiagram
from .gameEngine import gameEngine


def PKillMove(f,t,board):
    if(board[int(t[0])][int(t[1])]=="E"):
        return False
    for innerArr in moveDiagram["N"]:
        newF = str( int(f[0])+innerArr[0] ) + str( int(f[1])+innerArr[1] )
        if(newF==t ):
            return True
    return False
        


def isValidMove(f,t,board):
    if( board[int(f[0])][int(f[1])][1]!="Q" and  board[int(f[0])][int(f[1])][1]!="P" ):
        coin = board[int(f[0])][int(f[1])][1]
        return gameEngine( f, t, moveDiagram[coin] , stepsCountDiagram[coin] , board[int(f[0])][int(f[1])] , board )
    elif (board[int(f[0])][int(f[1])][1]=="Q"):
        return gameEngine( f, t, moveDiagram["E"] , stepsCountDiagram["E"], board[int(f[0])][int(f[1])] ,board)  or  gameEngine( f, t, moveDiagram["N"] , stepsCountDiagram["N"] ,  board[int(f[0])][int(f[1])],board )
    else:
        return gameEngine( f, t, moveDiagram["E"] , stepsCountDiagram["P"], board[int(f[0])][int(f[1])],board) or PKillMove(f,t,board)