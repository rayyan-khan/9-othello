defaultBoard = '.'*27 + 'ox......xo' + '.'*27
rows = []
nbrIndexes = {}
idxs = [i for i in range(0, len(defaultBoard))]
for index in idxs: # make better later if time/energy
    if index % 8 == 0: # if its on left edge, don't include anything left
        nbrIndexes[index] = {index + 1,
                             index - 8, index + 8,
                             index - 7,
                             index + 9}\
            .intersection(idxs) # don't include indexes that don't exist
    elif index % 8 == 7: # if its on right edge, don't include anything right
        nbrIndexes[index] = {index - 1,
                             index - 8, index + 8,
                             index + 7,
                             index - 9} \
            .intersection(idxs)
    else:
        nbrIndexes[index] = {index - 1,index + 1,
                             index - 8, index + 8,
                             index - 7, index + 7,
                             index - 9, index + 9} \
            .intersection(idxs)


def printBoard(board):
    for i in range(0, 64, 8):
        print(' '.join(board[i:i+8]))


def printPossMoves(board, possMoves):
    dispOps = ''.join([ch if idx not in possMoves else '*' for idx, ch in enumerate(board)])
    printBoard(dispOps)


def nextTokens(board): # assuming no passes
    if board.count('.') % 2: # do better later
        return 'o', 'x' # next token, token after
    return 'x', 'o'


def checkBracketing(token, possInd, adjInd, board):
    # your token, possible index, adjacent index, direction relative to
    # the adjacent opposing token, current board
    # return true or false depending on whether your token would
    # form a bracket with a matching token if placed next to index
    # also fix this later its lazy and kinda dumb

    diff = adjInd - possInd
    # what you have to do to get from possInd to adjInd

    checkInd = adjInd
    while 0 < checkInd < 64:
        newInd = checkInd + diff
        if newInd not in nbrIndexes[checkInd]:
            return False
        elif board[newInd] == '.':
            return False
        elif board[newInd] == token:
            return True
        checkInd = newInd


def nextMoves(board):
    possMoves = set() # wow come up with a better name
    token, oppToken = nextTokens(board)

    for idx in range(64):
        # lol don't check all this fr

        if board[idx] == oppToken:
            for nbr in nbrIndexes[idx]: # cringey
                if board[nbr] == '.':
                    if checkBracketing(token, nbr, idx, board):
                        possMoves.add(nbr)
    return possMoves


printBoard(defaultBoard)
possMoves = nextMoves(defaultBoard)
print('next moves:', possMoves)
printPossMoves(defaultBoard, possMoves)
