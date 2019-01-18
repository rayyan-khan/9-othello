import sys

# inputs from sys
startboard = sys.argv[1].lower() if len(sys.argv) > 1 else '.'*27 + 'ox......xo' + '.'*27
startTkn = sys.argv[2].lower() if len(sys.argv) > 2 else {0:'x', 1:'o'}[startboard.count('.')%2]

# global variables
NBRS_flips = {} # NBRS_flips = {index: {adjacent indexes}}
NBRS_moves = {} # NBRS_moves = {index: {adjacent indexes that moves can be made from}}
NBRS_moves_r = {} # reverse for checking from space
SUBSETS = [] # SUBSETS = [{nbr: [indexes in subset], nbr: [indexes in subset]}, {etc...}]
CNR_EDGES = {0: {1,2,3,4,5,6,7,8,16,24,32,40,48,56},
             7: {0,1,2,3,4,5,6,15,23,31,39,47,55,63},
             56: {0,8,16,24,32,40,48,57,58,59,60,61,62,63},
             63: {7,15,23,31,39,47,55,56,57,58,59,60,61,62}}
EDGE_CNR = {edgeInd: corner for corner in CNR_EDGES for edgeInd in CNR_EDGES[corner]}
CORNERS = {0, 7, 56, 63}
CX = {1: 0, 8: 0, 9: 0, 6: 7, 14: 7, 15: 7, 48: 56, 49: 56, 57: 56, 54: 63, 55: 63, 62: 63}
oppTkns = {'x':'o', 'o':'x'}
nextMoveCache = {}
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
NBRS_moves_r = {index: {key for key in NBRS_moves if index in NBRS_moves[key]} for index in range(64)}


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


def nextMoves(board, token): # return moves to be flipped later
    global nextMoveCache
    if board + token in nextMoveCache:
        return nextMoveCache[board + token]

    possMoves = {} # {possible move indexes: indexes they flip}
    oppToken = oppTkns[token]
    tknSet = {idx for idx in range(64) if board[idx] == oppToken} - {0, 7, 56, 63}

    for idx in tknSet: # check opposing token indexes (maybe improve later)
        for nbr in NBRS_moves[idx]: # check if there are spaces you can move into
            if board[nbr] == '.':
                bracket = checkBracketing(token, nbr, idx, board)
                if bracket != -1:
                    # if placing here check whether there's another
                    # token down the line it would form a bracket with
                    subset = SUBSETS[idx][nbr]
                    changes = set(subset[:subset.index(bracket) + 1] + [nbr, idx])
                    if nbr in possMoves:
                        possMoves[nbr] = possMoves[nbr].union(changes)
                    else:
                        possMoves[nbr] = changes
    nextMoveCache[board + token] = possMoves
    return possMoves


def makeFlips(board, token, move, possMoves):
    global makeFlipsCache
    changes = possMoves[move]
    move = str(move)
    if board + token + move in makeFlipsCache:
        return makeFlipsCache[board + token + move]
    # replace all the indexes that should be flipped with your token
    flippedboard =  ''.join([ch if ind not in changes else token for ind, ch in enumerate(board)])
    makeFlipsCache[board + token + move] = flippedboard
    return flippedboard


def estimateMoves(board, token):
    # estimate best moves without using recursion
    # could be improved but satisfactory for grade
    # remember that the grader looks at the last int printed, so
    # print the best move last -- ascending order in this case
    oppTkn = oppTkns[token]
    possMoves = nextMoves(board, token)
    sortedMoves = []

    for move in possMoves:
        score = 0

        oppPossMoves = nextMoves(startboard, startTkn)
        if not oppPossMoves:
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


def alphabeta(board, token, lower, upper): # want to return: min guaranteed score, rev. sequence
    oppTkn = oppTkns[token]

    # possible token moves
    possMoves = nextMoves(board, token)

    if not possMoves:
        # possible enemy moves
        possOppMoves = nextMoves(board, oppTkn)

        if not possOppMoves: # if neither side can move, return final score
            score = [board.count(token) - board.count(oppTkn)]
            return score

        # otherwise, if you get skipped, just alphabeta from the opponent's side
        ab = alphabeta(board, oppTkn, -upper, -lower)
        return [-ab[0]] + ab[1:] + [-1]

    best = [lower - 1]
    for move in possMoves:
        ab = alphabeta(makeFlips(board, token, move, possMoves), oppTkn, -upper, -lower)
        score = -ab[0]
        if score > upper:
            return [score]
        if score < lower:
            continue
        best = [score] + ab[1:] + [move]
        lower = score + 1
    return best


def alphabetaTopLvl(board, token, lower, upper): # want to return: min guaranteed score, rev. sequence
    oppTkn = oppTkns[token]

    # possible token moves
    possMoves = nextMoves(board, token)

    if not possMoves:
        # possible enemy moves
        possOppMoves = nextMoves(board, oppTkn)

        if not possOppMoves: # if neither side can move, return final score
            score = [board.count(token) - board.count(oppTkn)]
            return score

        # otherwise, if you get skipped, just alphabeta from the opponent's side
        ab = alphabeta(board, oppTkn, -upper, -lower)
        return [-ab[0]] + ab[1:] + [-1]

    best = [lower - 1]
    for move in possMoves:
        ab = alphabeta(makeFlips(board, token, move, possMoves), oppTkn, -upper, -lower)
        score = -ab[0]
        if score > upper:
            return [score]
        if score < lower:
            continue
        best = [score] + ab[1:] + [move]
        lower = score + 1
        print(best)
    return best


# run
print(estimateMoves(startboard, startTkn))
ab = alphabetaTopLvl(startboard, startTkn, -65, 65)
print('Score: {} Sequence: {}'.format(ab[0], ab[1:]))

