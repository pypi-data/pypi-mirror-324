

def checkToBox(f,board,turn):
    #checking entered value is number or not
    try:
        x = int(f[0])
        y = int(f[1])
        if(int(f)>77):
            print("\t\t\t\t ⚠️ Enter a valid number")
            return False
    except:
        print("\t\t\t\t ⚠️ Enter a valid number")
        return False
    #checking index entered is Greater then 7
    if( x>7 or y>7 ):
        print("\t\t\t\t ⚠️ Above 7 is Not Possible")
        return False
    #a user can kill him self
    if( (board[x][y][0]=="W" and turn=="White") or (board[x][y][0]=="B" and turn=="Black") ):
        print("\t\t\t\t ⚠️ Please Pic the right Coin (You cannot Kill You)")
        return False
    
    #If all above cases are passed then we did it
    return True

def checkFromBox(f,board,turn):
    #checking entered value is number or not
    try:
        x = int(f[0])
        y = int(f[1])
        if(int(f)>77):
            print("\t\t\t\t ⚠️ Enter a valid number")
            return False
    except:
        print("\t\t\t\t ⚠️ Enter a valid number")
        return False
    #checking index entered is Greater then 7
    if( x>7 or y>7 ):
        print("\t\t\t\t ⚠️ Above 7 is Not Possible")
        return False
    # checking from box should have a Coin
    if(board[x][y]=="E"):
        print("\t\t\t\t ⚠️ From Box Should Have A Coin")
        return False
    # picking the right coin test
    if( (board[x][y][0]=="W" and turn=="Black") or (board[x][y][0]=="B" and turn=="White") ):
        print("\t\t\t\t ⚠️ Please Pic the right Coin")
        return False
    
    #If all above cases are passed then we did it
    return True
    


def askUserToGiveInput(turn,board):
    print(f"\t\t\t\t Its {turn} 's { "♚" if turn=="White" else  "♔" }  turn")
    print("\t\t\t\t Enter row and colloum num without space ","eg:'57' 5 th Row and 7 th Colloum",sep="\n\t\t\t\t ",end="\n\n")
    fromIsPossible = False
    while not fromIsPossible:
        f = input("\t\t\t\t From -->  ")
        fromIsPossible = checkFromBox(f,board,turn)
    toIsPossible = False
    while not toIsPossible:
        t = input("\t\t\t\t To  --->  ")
        toIsPossible = checkToBox(t,board,turn)
    return [f, t]