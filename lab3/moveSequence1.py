import sys

# version to submit

# inputs from sys
startboard = '.'*27 + 'ox......xo' + '.'*27
startTkns = ''
movePos = ''

# assign those variables from sys input
# works regardless of order (not checked)
for k in range(1, len(sys.argv)):
    sys.argv[k] = sys.argv[k]
    if len(sys.argv[k]) == 64:
        startboard = sys.argv[k].lower()
    elif len(sys.argv[k]) in (1, 2):
        if sys.argv[k].lower() in 'xo':
            startTkns = sys.argv[k].lower()
        elif sys.argv[k][0].lower() in 'abcdefgh':
            movePos = (int(sys.argv[k][1])-1)*8 + \
                      'abcdefgh'.index(sys.argv[k][0].lower())
        else:
            movePos = int(sys.argv[k])
    else:
        print('Incorrect inputs at index {}:\nlength {}, {}'
              .format(k, len(sys.argv[k]), sys.argv[k]))

# global variables
NBRS_flips = {} # NBRS_flips = {index: {adjacent indexes}}
NBRS_moves = {} # NBRS_moves = {index: {adjacent indexes that moves can be made from}}
SUBSETS = [] # SUBSETS = [{nbr: [indexes in subset], nbr: [indexes in subset]}, {etc...}]
TKNSETS = {'o': {i for i in range(64) if startboard[i] == 'o'} - {0, 7, 56, 63},
             'x': {i for i in range(64) if startboard[i] == 'x'} - {0, 7, 56, 63}} # set of indexes containing o and x


# setting up NBRS -- part 1
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


# taking out NBRS that moves can't be made from
NBRS_moves = {index: {key for key in SUBSETS[index]} for index in NBRS_flips}
delInds = {key for key in NBRS_moves if len(NBRS_moves[key]) == 0}
for key in delInds:
    del NBRS_moves[key]

# helper methods

def getScore(board):
    return board.count('x'), board.count('o')


def nextTokens(board): # assuming no passes
    if board.count('.') % 2: # do better later
        return 'o', 'x' # next token, token after
    return 'x', 'o'


def getOppToken(token):
    if token == 'x':
        return 'o'
    return 'x'


def printBoard(board):
    for i in range(0, 64, 8):
        print(' '.join(board[i:i+8]))


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
            return False
        elif board[index] == token:
            # if you find a bracketing token somewhere along the line
            # then it does form a bracket
            return index # return the ending index
    # if you get through the entire subset and don't find a bracketing token
    # then too bad
    return False


def nextMoves(board, tokens = ''):
    possMoves = set() # {indexes that given/default token may make a move at}

    if tokens == '': # if token isn't given
        token, oppToken = nextTokens(board) # assume no passes and find next token
    else:
        token, oppToken = tokens, getOppToken(tokens)

    for idx in TKNSETS[oppToken]: # check opposing token indexes
        for nbr in NBRS_moves[idx]: # check if there are spaces you can move into
            if board[nbr] == '.':
                if checkBracketing(token, nbr, idx, board):
                    # if placing here check whether there's another
                    # token down the line it would form a bracket with
                    possMoves.add(nbr) # if so it's a possible move
    # if len(possMoves) == 0, then nextMoves[0] == False
    return len(possMoves), possMoves


def makeFlips(board, token, position):
    oppToken = getOppToken(token)
    adjOpps = {nbr for nbr in NBRS_flips[position]
               if board[nbr] == oppToken and position in SUBSETS[nbr]}

    for opp in adjOpps: # do better later
        idx = checkBracketing(token, position, opp, board) # maybe pass in idx rather than re-finding
        if idx:
            subset = SUBSETS[opp][position]
            changes = set(subset[:subset.index(idx) + 1] + [position, opp])
            TKNSETS[token] = TKNSETS[token].union(changes) - {0, 7, 56, 63}
            board = ''.join([ch if ind not in changes else token for ind, ch in enumerate(board)])
    return board


def play(startTkns, startboard, movePos):
    # takes in token, board, move position
    # outputs
    if startTkns == '':
        startTkns, oppTkn = nextTokens(startboard)
    else:
        oppTkn = getOppToken(startTkns)
    canMove, possMoves = nextMoves(startboard, startTkns)

    if canMove: # if you can make a move

        # if not a possible move, just print the first snapshot
        if movePos not in possMoves:
            printPossMoves(startboard, possMoves)
            xCount, oCount = getScore(startboard)
            print('Score: {}/{}'.format(xCount, oCount))
            print('Possible moves for {} : {}'.format(startTkns, possMoves))
            print(startboard + '\n')

        # if a possible move, print the first and second snapshots
        # + possible moves for next opponent
        elif movePos != '':
            # first print board rep of possMoves, then score,
            # then possMoves listed, then string rep of board
            printPossMoves(startboard, possMoves)
            xCount, oCount = getScore(startboard)
            print('Score: {}/{}'.format(xCount, oCount))
            print('Possible moves for {} : {}'.format(startTkns, possMoves))
            print(startboard + '\n')

            # print move made, then board resulting from the move
            # and new score followed by string rep of new board
            print('Player {} moves to {}:'.format(startTkns, movePos))
            flippedBoard = makeFlips(startboard, startTkns, movePos)
            printBoard(flippedBoard)
            xCount, oCount = getScore(flippedBoard)
            print('Score: {}/{}'.format(xCount, oCount))
            print(flippedBoard)

            # check if the opposing token can make moves on flipped board
            canMove, possMoves = nextMoves(flippedBoard, oppTkn)
            oppPass = False
            if canMove: # if it can, print its possible moves
                print('Possible moves for {}: {}'.format(oppTkn, possMoves))
            else: # otherwise, pass and check if your token
                # can make a move on the board
                canMove, possMoves = nextMoves(flippedBoard, startTkns)
                if canMove:
                    print('Possible moves for {}: {}'.format(startTkns, possMoves))

    else: # if no moves possible, say so
        printBoard(startboard)
        xCount, oCount = getScore(startboard)
        print('Score: {}/{}'.format(xCount, oCount))
        print(startboard)
        print('No possible moves.')

print('hi')