
def checkToBox(f):
    #checking entered value is number or not
    try:
        x = int(f[0])
        y = int(f[1])
        if(int(f)>77):
            return False
    except:
        return False
    #checking index entered is Greater then 7
    if( x>7 or y>7 ):
        return False
    return True

def gameEngine(f,t,movesArr,movesCount,coin,board):
    print(f,t,movesArr,movesCount,coin)
    # Base Condition
    if(f==t):
        return True
    # The present box should have my coin or an empty space
    if( board[int(f[0])][int(f[1])]!=coin and board[int(f[0])][int(f[1])]!="E" ):
        return False
    if(movesCount<1):
        return False
    # going to nextMove
    ans = False
    for innerArr in movesArr:
        newF = str( int(f[0])+innerArr[0] ) + str( int(f[1])+innerArr[1] )
        ans = ans or ( checkToBox(newF) and gameEngine(newF,t,movesArr,movesCount-1,coin,board) )
    return ans