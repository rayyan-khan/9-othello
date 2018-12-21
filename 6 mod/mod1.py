import rand
import chooseMove1
import helper

def run():
    currentBoard = '.'*27 + 'ox......xo' + '.'*27
    currentToken = 'x'
    xScript, oScript = rand, chooseMove1
    done = False
    movesMade = []

    while currentBoard.count('.') != 0 and not done:
        #xCount, oCount = helper.getScore(currentBoard)
        #print('Player: {} Score: {}x/{}o Board: {}'
        #      .format(currentToken, xCount, oCount, currentBoard))
        if currentToken == 'x':
            chosenMove = xScript.run(currentBoard, 'x')
            oppTkn = 'o'
        else:
            chosenMove = oScript.run(currentBoard, 'o')
            oppTkn = 'x'
        currentBoard = helper.makeFlips\
            (currentBoard, currentToken, chosenMove)[0]
        movesMade.append((currentToken, chosenMove, currentBoard))
        checkPass = helper.nextMoves(currentBoard, oppTkn)[0]
        if checkPass:
            currentToken = oppTkn
        else:
            checkPassAgain = helper.nextMoves(currentBoard, currentToken)
            if not checkPassAgain:
                done = True

    xCount, oCount = helper.getScore(currentBoard)
    print('Score: {}x/{}o'.format(xCount, oCount))
    print('Moves made: {}'.format([' '.join(str(tpl[1]) for tpl in movesMade)]))