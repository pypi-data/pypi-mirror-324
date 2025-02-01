def makeCoinFtoT(f,t,board):
    board[int(t[0])][int(t[1])] = board[int(f[0])][int(f[1])]
    board[int(f[0])][int(f[1])] = "E"
    print("\n\n\n\n")