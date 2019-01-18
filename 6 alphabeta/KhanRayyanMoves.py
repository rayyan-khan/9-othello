import sys

# version 4 of this, took out all the print statements from possMoves2
# its so ugly though figure out how to fix it
# also comment/organize before it gets too confusing
# NBRS might be redundant now that there's SUBSETS but oh well think about that later


# variables
defaultBoard = '.'*27 + 'ox......xo' + '.'*27
NBRS = {} # NBRS = {index: {adjacent indexes that moves can be made from}}
SUBSETS = [] # SUBSETS = [{nbr: [indexes in subset], nbr: [indexes in subset]}, {etc...}]
startboard = defaultBoard
startTkns = ''

inpts = len(sys.argv) # make nicer later
if inpts == 3:
    if len(sys.argv[1]) == 64:
        startboard = sys.argv[1].lower()
        startTkns = sys.argv[2].lower()
    elif len(sys.argv[1]) == 1:
        startTkns = sys.argv[1]
        startboard = sys.argv[2].lower()
elif inpts == 2:
    if len(sys.argv[1]) == 64:
        startboard = sys.argv[1].lower()
    elif len(sys.argv[1]) == 1:
        startTkns = sys.argv[1].lower()


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



# helper methods

def printBoard(board):
    for i in range(0, 64, 8):
        print(' '.join(board[i:i+8]))


def printPossMoves(board, possMoves):
    printBoard(''.join([ch if idx not in possMoves
                        else '*' for idx, ch in enumerate(board)]))


def heylookcoolandflashylookhereherehere(x):
    # if you read this Dr. Gabor, just know that its existence was
    # a bit of a dare, and this has good reason to be here.
    # someone else chose the name of the method.
    # but also I'm taking it out next version.
    return x
heylookcoolandflashylookhereherehere(5)


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
            return True
    # if you get through the entire subset and don't find a bracketing token
    # then too bad
    return False



def nextMoves(board, tokens = ''):
    possMoves = set() # wow come up with a better name

    if tokens == '':
        token, oppToken = nextTokens(board)
    else:
        token, oppToken = tokens, getOppToken(tokens)


    for idx in NBRS:
        # lol don't check all this later

        if board[idx] == oppToken:
            for nbr in NBRS[idx]: # cringe
                if board[nbr] == '.':
                    if checkBracketing(token, nbr, idx, board):
                        possMoves.add(nbr)
    return len(possMoves), possMoves



# run
canMove, possMoves = nextMoves(startboard, startTkns)

if canMove:
    printPossMoves(startboard, possMoves)
    print('next moves:', possMoves)
else:
    print('No moves possible.')
