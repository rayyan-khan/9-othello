import sys

# inputs from sys
startboard = sys.argv[1].lower() if len(sys.argv) > 1 else '.'*27 + 'ox......xo' + '.'*27
startTkn = sys.argv[2].lower() if len(sys.argv) > 2 else {0:'x', 1:'o'}[startboard.count('.')%2]

# global variables
NBRS_flips = {} # NBRS_flips = {index: {adjacent indexes}}
NBRS_moves = {} # NBRS_moves = {index: {adjacent indexes that moves can be made from}}
SUBSETS = [] # SUBSETS = [{nbr: [indexes in subset], nbr: [indexes in subset]}, {etc...}]
CNR_EDGES = {0: {1,2,3,4,5,6,7,8,16,24,32,40,48,56},
             7: {0,1,2,3,4,5,6,15,23,31,39,47,55,63},
             56: {0,8,16,24,32,40,48,57,58,59,60,61,62,63},
             63: {7,15,23,31,39,47,55,56,57,58,59,60,61,62}}
EDGE_CNR = {edgeInd: corner for corner in CNR_EDGES for edgeInd in CNR_EDGES[corner]}
CORNERS = {0, 7, 56, 63}
CX = {1: 0, 8: 0, 9: 0, 6: 7, 14: 7, 15: 7, 48: 56, 49: 56, 57: 56, 54: 63, 55: 63, 62: 63}
oppTkns = {'x':'o', 'o':'x'}
nextMovesChache = {}
makeFlipsCache = {}


# setting up NBRS
idxs = [i for i in range(0, len(startboard))]
for index in idxs: # make better later if time/energy/if its worth it
    if index % 8 == 0: # if its on left edge, don't include anything left
        NBRS_flips[index] = {index + 1,
                             index - 8, index + 8,
                             index - 7,
                             index + 9}\
            .intersection(idxs) # don't include indexes that don't exist
    elif index % 8 == 7: # if its on right edge, don't include anything right
        NBRS_flips[index] = {index - 1,
                             index - 8, index + 8,
                             index + 7,
                             index - 9} \
            .intersection(idxs)
    else:
        NBRS_flips[index] = {index - 1,index + 1,
                             index - 8, index + 8,
                             index - 7, index + 7,
                             index - 9, index + 9} \
            .intersection(idxs)

# setting up SUBSETS
for index in idxs: # want a dict for each index
    subDict = {nbr: [] for nbr in NBRS_flips[index]}
    for nbr in NBRS_flips[index]: # want a key for each neighbor
        # want the value to be a list of the other indexes in the same
        # row/column/diagonal, depending on the relationship between the
        # index and neighbor (which determines whether you're looking at
        # diagonals, columns, or rows)
        diff = index - nbr
        prev = nbr
        current = nbr + diff
        while -1 < current < 64 and current in NBRS_flips[prev]:
            if current != index:
                subDict[nbr].append(current)
            prev = current
            current = current + diff
        if len(subDict[nbr]) == 0:
            del subDict[nbr]
    SUBSETS.append(subDict)

# taking out neighbors that moves can't be made from
NBRS_moves = {index: {key for key in SUBSETS[index]} for index in NBRS_flips}
delInds = {key for key in NBRS_moves if len(NBRS_moves[key]) == 0}
for key in delInds:
    del NBRS_moves[key]


# helper methods
def printBoard(board):
    for i in range(0, 64, 8):
        print(' '.join(board[i:i+8]))


def printPossMoves(board, possMoves):
    # print board with asterisks in place of possible moves
    printBoard(''.join([ch if idx not in possMoves
                        else '*' for idx, ch in enumerate(board)]))


def checkBracketing(token, possInd, adjInd, board):
    # your token, possible placement index, adjacent index of opponent, current board
    # return index of bracketing token if there is one
    # also try to think of better ways to go about this? later

    subset = SUBSETS[adjInd][possInd]

    for index in subset:
        if board[index] == '.':
            # if you run into an empty space before bracketing token
            # then it doesn't work
            return -1
        elif board[index] == token:
            # if you find a bracketing token somewhere along the line
            # then it does form a bracket
            return index # return the ending index
    # if you get through the entire subset and don't find a bracketing token
    # then too bad
    return -1


def nextMoves(board, token, tknSets): # return moves to be flipped later
    global nextMovesChache
    if board + token in nextMovesChache:
        return nextMovesChache[board + token]

    possMoves = {} # {possible move indexes: indexes they flip}
    oppToken = oppTkns[token]

    for idx in tknSets[oppToken]: # check opposing token indexes (maybe improve later)
        for nbr in NBRS_moves[idx]: # check if there are spaces you can move into
            if board[nbr] == '.':
                bracket = checkBracketing(token, nbr, idx, board)
                if bracket != -1:
                    # if placing here check whether there's another
                    # token down the line it would form a bracket with
                    subset = SUBSETS[idx][nbr]
                    changes = set(subset[:subset.index(bracket) + 1] + [nbr, idx])
                    if nbr in possMoves:
                        possMoves[nbr].union(changes)
                    else:
                        possMoves[nbr] = changes
    # if len(possMoves) == 0, then nextMoves[0] == False
    nextMovesChache[board + token] = (len(possMoves), possMoves)
    return len(possMoves), possMoves


def makeFlips(board, token, changes):
    global makeFlipsCache
    if board + token in makeFlipsCache:
        return makeFlipsCache[board + token]
    # replace all the indexes that should be flipped with your token
    flippedboard =  ''.join([ch if ind not in changes else token for ind, ch in enumerate(board)])
    #print('BOARD: {} FLIPPED BOARD: {}'.format(board, flippedboard))
    makeFlipsCache[board + token] = flippedboard
    return flippedboard


def estimateMoves(board, token):
    # estimate best moves without using recursion
    # could be improved but satisfactory for grade
    # remember that the grader looks at the last int printed, so
    # print the best move last -- ascending order in this case
    oppTkn = oppTkns[token]
    tknSets = {'o': {i for i in range(64) if startboard[i] == 'o'} - {0, 7, 56, 63},
               'x': {i for i in range(64) if startboard[i] == 'x'} - {0, 7, 56, 63}}
    canMove, possMoves = nextMoves(board, token, tknSets)
    sortedMoves = []

    for move in possMoves:
        score = 0

        oppCanMove, oppPossMoves = nextMoves(startboard, startTkn, tknSets)
        if not oppCanMove:
            score += 2

        # just checking for corners and edges and stuff like that
        if move in CORNERS:
            score += 3
        elif move in EDGE_CNR:
            if board[EDGE_CNR[move]] == token:
                score += 1
        if move in CX:
            if board[CX[move]] == '.':
                score = -100
            elif board[CX[move]] == oppTkn:
                score = -99

        sortedMoves.append((score, move))

    return [move for score, move in sorted(sortedMoves)]


def negamax(board, token): # want to return: min guaranteed score, rev. sequence
    oppTkn = oppTkns[token]
    tknSets = {'o': {i for i in range(64) if startboard[i] == 'o'} - {0, 7, 56, 63},
               'x': {i for i in range(64) if startboard[i] == 'x'} - {0, 7, 56, 63}}

    # number of possible moves, set of possible moves
    canMove, possMoves = nextMoves(board, token, tknSets)

    if not canMove:
        # number of enemy possible moves, set of those moves
        canOppMove, possOppMoves = nextMoves(board, oppTkn, tknSets)

        if not canOppMove: # if neither side can move, return final score
            score = [board.count(token) - board.count(oppTkn)]
            #print('POSS SCORE', score)
            return score

        # otherwise, if you get skipped, just negamax from the opponent's side
        nm = negamax(board, oppTkn)
        return [-nm[0]] + nm[1:] + [-1]

    # of the possible scores you might get, find the smallest
    best = min(negamax(makeFlips(board, token, possMoves[move]), oppTkn)
               + [move] for move in possMoves)
    return [-best[0]] + best[1:]


def printSorted(board, token):
    #print('Board: {}'.format(board))
    movesLeft = board.count('.')
    #print('Moves left: {}'.format(movesLeft))
    if movesLeft <= 3:
        nm = negamax(board, token)
        print('Score: {} Sequence: {}'.format(nm[0], nm[1:]))
    else:
        print('est')
        print(estimateMoves(board, token))


# run
print(estimateMoves(startboard, startTkn))
printSorted(startboard, startTkn)


