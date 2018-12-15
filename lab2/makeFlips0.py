import sys
import time
# first go at lab 2, broken


# variables
defaultBoard = '.'*27 + 'ox......xo' + '.'*27
NBRS = {} # NBRS = {index: {adjacent indexes that moves can be made from}}
SUBSETS = [] # SUBSETS = [{nbr: [indexes in subset], nbr: [indexes in subset]}, {etc...}]
startboard = defaultBoard
startTkns = ''
movePos = ''

'''
inpts = len(sys.argv) # make nicer later
if len(sys.argv[1]) == 64:
    startboard = sys.argv[1].lower()
    if sys.argv[2] in 'xo':
        startTkns = sys.argv[2].lower()
        movePos = int(sys.argv[3])
elif len(sys.argv[1]) == 1:
    if sys.argv[1] in 'xo':
        startTkns = sys.argv[1].lower()
    else:
        movePos = int(sys.argv[1])
    if len(sys.argv[2]) == 1:
        startTkns = sys.argv[2]
        startboard = sys.argv[3]
    else:
        startTkns = sys.argv[3]
        startboard = sys.argv[2]
'''

t = time.clock()

# setting up NBRS -- part 1
idxs = [i for i in range(0, len(defaultBoard))]
for index in idxs: # make better later if time/energy/if its worth it
    if index % 8 == 0: # if its on left edge, don't include anything left
        NBRS[index] = {index + 1,
                             index - 8, index + 8,
                             index - 7,
                             index + 9}\
            .intersection(idxs) # don't include indexes that don't exist
    elif index % 8 == 7: # if its on right edge, don't include anything right
        NBRS[index] = {index - 1,
                             index - 8, index + 8,
                             index + 7,
                             index - 9} \
            .intersection(idxs)
    else:
        NBRS[index] = {index - 1,index + 1,
                             index - 8, index + 8,
                             index - 7, index + 7,
                             index - 9, index + 9} \
            .intersection(idxs)

# setting up SUBSETS
for index in idxs: # want a dict for each index
    subDict = {nbr: [] for nbr in NBRS[index]}
    for nbr in NBRS[index]: # want a key for each neighbor
        # want the value to be a list of the other indexes in the same
        # row/column/diagonal, depending on the relationship between the
        # index and neighbor (which determines whether you're looking at
        # diagonals, columns, or rows)
        diff = index - nbr
        prev = nbr
        current = nbr + diff
        while -1 < current < 64 and current in NBRS[prev]:
            if current != index:
                subDict[nbr].append(current)
            prev = current
            current = current + diff
        if len(subDict[nbr]) == 0:
            del subDict[nbr]
    SUBSETS.append(subDict)

# taking out NBRS that moves can't be made from
NBRS = {index: {key for key in SUBSETS[index]} for index in NBRS}
delInds = {key for key in NBRS if len(NBRS[key]) == 0}
for key in delInds:
    del NBRS[key]

print('TIME:', time.clock()-t)

# helper methods

def printBoard(board):
    for i in range(0, 64, 8):
        print(' '.join(board[i:i+8]))


def printPossMoves(board, possMoves):
    printBoard(''.join([ch if idx not in possMoves
                        else '*' for idx, ch in enumerate(board)]))


def nextTokens(board): # assuming no passes
    if board.count('.') % 2: # do better later
        return 'o', 'x' # next token, token after
    return 'x', 'o'


def getOppToken(token):
    if token == 'x':
        return 'o'
    return 'x'


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
    possMoves = set() # wow come up with a better name

    if tokens == '':
        token, oppToken = nextTokens(board)
    else:
        token, oppToken = tokens, getOppToken(tokens)


    for idx in range(64):
        # lol don't check all this later

        if board[idx] == oppToken:
            for nbr in NBRS[idx]: # cringe
                if board[nbr] == '.':
                    if checkBracketing(token, nbr, idx, board):
                        possMoves.add(nbr)
    return len(possMoves), possMoves


def makeFlips(board, token, position):
    oppToken = getOppToken(token)
    adjOpps = {nbr for nbr in NBRS[position] if board[nbr] == oppToken}

    for opp in adjOpps: # do better later
        idx = checkBracketing(token, position, opp, board)
        if idx:
            subset = SUBSETS[opp][position]
            print('subset {} position {} opp {} idx {}'.format(subset, position, opp, idx))
            numFlips = len(subset[subset.index(idx):subset.index(opp)]) - 1
            flips = token * (numFlips + 1)
            firstPos = position if position < idx else idx
            secondPos = position if firstPos != position else idx
            #print('FirstPos {} SecondPos {} flips: {}'.format(firstPos, secondPos, flips))
            board = board[:firstPos] + flips + board[secondPos:]
            #print('BOARD:')
            #printBoard(board)
            #print('\n')

    return board

def getScore(board):
    return board.count('x'), board.count('o')


# testing
test1 = (defaultBoard, 'x', 26)
test2 = ('..........................xxx......xo...........................', 'o', 18)

startboard, startTkns, movePos = test2

'''
# run
canMove, possMoves = nextMoves(startboard, startTkns)
if canMove:
    if movePos != '':
        flippedBoard = makeFlips(startboard, startTkns, movePos)
        printPossMoves(startboard, possMoves)
        xCount, oCount = getScore(startboard)
        print('Score: {}/{}'.format(xCount, oCount))
        print('Possible moves for {} : {} \n'.format(startTkns, possMoves))
        print('Player {} moves to {}:'.format(startTkns.upper(), movePos))
        printBoard(flippedBoard)
        xCount, oCount = getScore(flippedBoard)
        print('Score: {}/{}'.format(xCount, oCount))
        print(flippedBoard)
        canMove, possMoves = nextMoves(flippedBoard, getOppToken(startTkns))
        oppPass = False
        if canMove:
            print('Possible moves for {}: {}'.format(getOppToken(startTkns), possMoves))
        else:
            oppPass = True
        canMove, possMoves = nextMoves(flippedBoard, startTkns)
        if canMove and oppPass:
            print('Possible moves for {}: {}'.format(startTkns, possMoves))
else:
    print('No possible moves.')
'''
