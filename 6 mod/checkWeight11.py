import sys
import time


# global variables
NBRS_flips = {}  # NBRS_flips = {index: {adjacent indexes}}
NBRS_moves = {}  # NBRS_moves = {index: {adjacent indexes that moves can be made from}}
SUBSETS = []  # SUBSETS = [{nbr: [indexes in subset], nbr: [indexes in subset]}, {etc...}]
def setBrdTkn(board, token):
    global startboard, startTkn, TKNSETS
    startboard, startTkns = board.lower(), token.lower()
    TKNSETS = {'o': {i for i in range(64) if startboard[i] == 'o'} - {0, 7, 56, 63},
                 'x': {i for i in range(64) if startboard[i] == 'x'} - {0, 7, 56, 63}}
    # set of indexes containing o and x

CNR_EDGES = {0: {1, 2, 3, 4, 5, 6, 7, 8, 16, 24, 32, 40, 48, 56}, 7: {0, 1, 2, 3, 4, 5, 6, 15, 23, 31, 39, 47, 55, 63},
             56: {0, 8, 16, 24, 32, 40, 48, 57, 58, 59, 60, 61, 62, 63},
             63: {7, 15, 23, 31, 39, 47, 55, 56, 57, 58, 59, 60, 61, 62}}
EDGE_CNR = {edgeInd: corner for corner in CNR_EDGES for edgeInd in CNR_EDGES[corner]}
CORNERS = {0, 7, 56, 63}
CX = {1: 0, 8: 0, 9: 0, 6: 7, 14: 7, 15: 7, 48: 56, 49: 56, 57: 56, 54: 63, 55: 63, 62: 63}
CX_a = {1, 8, 6, 15, 48, 57, 55, 62}
CX_d = {9, 14, 49, 54}
CNR_row = {0: {1: 0, 2: 1, 3: 2, 4: 3, 5: 4, 6: 5},
           7: {6: 0, 5: 1, 4: 2, 3: 3, 2: 4, 1: 5, 0: 6}}  # remember other two corners
CNR_col = {0: {8: 0, 16: 1, 24: 2, 32: 3, 40: 4, 48: 5, 56: 6},
           7: {15: 0, 23: 1, 31: 2, 39: 3, 47: 4, 55: 5, 63: 0}}  # remember other two
CNR_diag = {0: {1: {2, 9, 16}, 2: {3, 10, 17, 24}, 3: {4, 11, 18, 25, 32},
                4: {5, 12, 19, 26, 33, 40}, 5: {6, 13, 20, 27, 34, 41, 48},
                6: {7, 14, 21, 28, 35, 42, 49, 56}}}  # note: finish these later and try not to double count corners

# setting up NBRS -- part 1
idxs = [i for i in range(64)]
for index in idxs:  # make better later if time/energy/if its worth it
    if index % 8 == 0:  # if its on left edge, don't include anything left
        NBRS_flips[index] = {index + 1,
                             index - 8, index + 8,
                             index - 7,
                             index + 9} \
            .intersection(idxs)  # don't include indexes that don't exist
    elif index % 8 == 7:  # if its on right edge, don't include anything right
        NBRS_flips[index] = {index - 1,
                             index - 8, index + 8,
                             index + 7,
                             index - 9} \
            .intersection(idxs)
    else:
        NBRS_flips[index] = {index - 1, index + 1,
                             index - 8, index + 8,
                             index - 7, index + 7,
                             index - 9, index + 9} \
            .intersection(idxs)

# setting up SUBSETS
for index in idxs:  # want a dict for each index
    subDict = {nbr: [] for nbr in NBRS_flips[index]}
    for nbr in NBRS_flips[index]:  # want a key for each neighbor
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

# taking out NBRS that moves can't be made from
NBRS_moves = {index: {key for key in SUBSETS[index]} for index in NBRS_flips}
delInds = {key for key in NBRS_moves if len(NBRS_moves[key]) == 0}
for key in delInds:
    del NBRS_moves[key]


# helper methods
def getScore(board):
    return board.count('x'), board.count('o')


def nextTokens(board):  # assuming no passes
    if board.count('.') % 2:  # do better later
        return 'o', 'x'  # next token, token after
    return 'x', 'o'


def getOppToken(token):
    if token == 'x':
        return 'o'
    return 'x'


def printBoard(board):
    for i in range(0, 64, 8):
        print(' '.join(board[i:i + 8]))


def printPossMoves(board, possMoves):
    printBoard(''.join([ch if idx not in possMoves
                        else '*' for idx, ch in enumerate(board)]))


def checkBracketing(token, possInd, adjInd, board):
    # your token, possible placement index, adjacent index of opponent, current board
    # return true or false depending on whether your token would
    # form a bracket with a matching token if placed next to index
    # also try to think of better ways to go about this

    subset = SUBSETS[adjInd][possInd]

    for index in subset:
        if board[index] == '.':
            # if you run into an empty space before bracketing token
            # then it doesn't work
            return -1
        elif board[index] == token:
            # if you find a bracketing token somewhere along the line
            # then it does form a bracket
            return index  # return the ending index
    # if you get through the entire subset and don't find a bracketing token
    # then too bad
    return -1


def nextMoves(board, tokens=''):
    possMoves = set()  # {indexes that given/default token may make a move at}

    if tokens == '':  # if token isn't given
        token, oppToken = nextTokens(board)  # assume no passes and find next token
    else:
        token, oppToken = tokens, getOppToken(tokens)

    for idx in TKNSETS[oppToken]:  # check opposing token indexes
        for nbr in NBRS_moves[idx]:  # check if there are spaces you can move into
            if board[nbr] == '.':
                if checkBracketing(token, nbr, idx, board) != -1:
                    # if placing here check whether there's another
                    # token down the line it would form a bracket with
                    possMoves.add(nbr)  # if so it's a possible move
    # if len(possMoves) == 0, then nextMoves[0] == False
    return len(possMoves), possMoves


def makeFlips(board, token, position):
    oppToken = getOppToken(token)

    adjOpps = {nbr for nbr in NBRS_flips[position]
               if board[nbr] == oppToken and position in SUBSETS[nbr]}

    TKNSETS_copy = TKNSETS.copy()

    allChanges = set()
    for opp in adjOpps:  # do better later
        idx = checkBracketing(token, position, opp, board)  # maybe pass in idx rather than re-finding
        if idx > -1:
            subset = SUBSETS[opp][position]
            changes = set(subset[:subset.index(idx) + 1] + [position, opp])
            allChanges = allChanges.union(changes)
            TKNSETS_copy[token] = TKNSETS_copy[token].union(changes) - {0, 7, 56, 63}
            TKNSETS_copy[oppToken] = TKNSETS_copy[oppToken] - changes
            board = ''.join([ch if ind not in changes else token for ind, ch in enumerate(board)])
    return board, allChanges, TKNSETS_copy


def CNR_CX(token, oppTkn, board, move):
    cnr_cx = 0
    if move in CORNERS:
        cnr_cx = 4
    elif move in EDGE_CNR:
        if board[EDGE_CNR[move]] == token:
            cnr_cx = 2
    if move in CX_a:
        if board[CX[move]] == '.':
            cnr_cx = -3
        elif board[CX[move]] == oppTkn:
            cnr_cx = -1
        else:
            cnr_cx = 4
    elif move in CX_d:
        if board[CX[move]] == '.':
            cnr_cx = -4
        elif board[CX[move]] == oppTkn:
            cnr_cx = -2
        else:
            cnr_cx = 3
    return cnr_cx / 4


def countDiag(board, token, cnr):
    furthestIndex = 0
    prev = 0
    stableTokens = 0
    for index in CNR_row[cnr]:
        if board[index] == token:
            stableTokens += 1
            prev = index
        else:
            furthestIndex = CNR_row[cnr][prev]
            break
    for index in CNR_col[cnr]:
        if board[index] == token:
            stableTokens += 1
            prev = index
        else:
            furthestIndex = CNR_col[cnr][prev]
    if furthestIndex:
        for diag in range(1, furthestIndex):
            currentDiag = CNR_diag[cnr][diag]
            if {board[ind] for ind in currentDiag} == {token}:
                stableTokens += len(currentDiag)
            else:
                break
    return stableTokens


def stableTokens(board, token):
    stableTokens = 0
    openSpaces = board.count('.')
    if openSpaces > 52:
        return stableTokens
    else:
        if {board[0], board[1], board[8]} == {token}:
            # 0 corner
            stableTokens += 3
            if board[9] == token:
                stableTokens += 1
            stableTokens += countDiag(board, token, 0)

        if {board[6], board[7], board[15]} == {token}:
            # 7 corner
            stableTokens += 3
            if board[14] == token:
                stableTokens += 1
        if {board[48], board[56], board[57]} == {token}:
            # 56 corner
            stableTokens += 3
            if board[49] == token:
                stableTokens += 1
        if {board[55], board[62], board[63]} == {token}:
            # 63 corner
            stableTokens += 3
            if board[54] == token:
                stableTokens += 1

    return stableTokens


def stabletokens_est(token, oppTkn, oppPossMoves, flippedBoard, tknSet):
    currentTokens = len(tknSet[token])
    try:
        tknStable = stableTokens(flippedBoard, token)
        oppStable = stableTokens(flippedBoard, oppTkn)
    except:
        tknStable, oppStable = 0, 0
    if len(oppPossMoves) == 0:
        #print('Pass')
        return tknStable
    flippedTokens = 0
    for move in oppPossMoves:
        oppFlipped, oppChanges, newTknSet = makeFlips(flippedBoard, oppTkn, move)
        flippedTokens += len(tknSet[token].intersection(oppChanges))
    instability = flippedTokens / len(oppPossMoves) / currentTokens
    if tknStable + oppStable != 0 and tknStable - oppStable != 0:
        est = (tknStable - oppStable)/(tknStable + oppStable) - instability
        #print('Unstable: {} Player stability: {} Opponent Stability: {} Overall est: {}'
        #      .format(instability, tknStable, oppStable, est))
        return est
    else:
        return 0.5 - instability

def mobility(oppPossMoves, flippedBoard, token):
    oppMobl = len(oppPossMoves) * 4
    playerMobl = len(nextMoves(flippedBoard, token)[1])
    #print ("MOBILITY opp",oppMobl,"mine",playerMobl)
    if playerMobl + oppMobl != 0:
        return (playerMobl - oppMobl)/(playerMobl + oppMobl)
    else:
        return 0


def sortMoves(token, oppTkn, board, possMoves):
    # remember that the grader looks at the last int printed, so
    # print the best move last -- ascending order in this case
    sortedMoves = []

    boardProgress = board.count('.')/64
    cnrw = 3.7*boardProgress
    moblw = 1/(boardProgress*2.6)

    for move in possMoves:
        flippedBoard, changes, TKNSETS_new = makeFlips(board, token, move)
        oppCanMove, oppPossMoves = nextMoves(flippedBoard, oppTkn)

        cnr_cx = CNR_CX(token, oppTkn, board, move) * cnrw
        stbl = stabletokens_est(token, oppTkn, oppPossMoves, flippedBoard, TKNSETS_new) * 0
        if not oppCanMove:
            mobl = 0.14127*moblw
        else:
            mobl = mobility(oppPossMoves, flippedBoard, token) * moblw

        #print('Move: {} CNR: {} Skip: {} STBL: {}'.format(move, cnr_cx, skip, stbl))

        mytokens = flippedBoard.count(token)
        opptokens = flippedBoard.count(oppTkn)

        size = (opptokens-mytokens)/(mytokens+opptokens)

        print("mytokens",mytokens,"opptokens",opptokens)
        score = cnr_cx + mobl + size * boardProgress / 64
        print("move:",move,"cnr",cnr_cx,"stbl",stbl,"mobility",mobl,"size",size)
        sortedMoves.append((score, move))

    return sorted(sortedMoves)


# run
def run(board, token):
    setBrdTkn(board, token)
    oppTkn = getOppToken(token)
    canMove, possMoves = nextMoves(board, token)
    move = sortMoves(token, oppTkn, board, possMoves)[::-1][0][1]
    return move