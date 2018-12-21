
import helper
import rand
import rand55
import chooseMove1
import chooseMove11
import chooseMove1101

xScript, oScript = chooseMove11, chooseMove1101
loops = 50


xTokenCount, oTokenCount, xWins, oWins, ties = 0, 0, 0, 0, 0
lowXtkr, lowOtkr = 1, 1
lowXmoves, lowOmoves = (), ()


def playGame():
    currentBoard = '.'*27 + 'ox......xo' + '.'*27
    currentToken = 'x'
    done = False
    movesMade = []

    while currentBoard.count('.') != 0 and not done:
        if currentToken == 'x':
            chosenMove = xScript.run(currentBoard, 'x')
            oppTkn = 'o'
        else:
            try:
                chosenMove = oScript.run(currentBoard, 'o')
                oppTkn = 'x'
            except:
                exit('Error: ' + currentBoard)
        currentBoard = helper.makeFlips\
            (currentBoard, currentToken, chosenMove)[0]
        movesMade.append(chosenMove)
        checkPass = helper.nextMoves(currentBoard, oppTkn)[0]
        if checkPass:
            currentToken = oppTkn
        else:
            checkPassAgain = helper.nextMoves(currentBoard, currentToken)[0]
            if not checkPassAgain:
                done = True
    xCount, oCount = helper.getScore(currentBoard)
    return xCount, oCount, movesMade


for k in range(loops):
    xCount, oCount, movesMade = playGame()
    xTokenCount += xCount
    oTokenCount += oCount

    if xCount > oCount:
        xWins += 1
        #print('x win', xCount, oCount, ' '.join([str(k) for k in movesMade]))
    elif oCount > xCount:
        oWins += 1
    else:
        ties += 1

    xTkr = xTokenCount/(xTokenCount + oTokenCount)
    oTkr = oTokenCount/(oTokenCount + xTokenCount)

    if xTkr <= lowXtkr:
        lowXtkr = xTkr
        lowXmoves = (xCount, oCount, movesMade)
    if oTkr <= lowOtkr:
        lowOtkr = oTkr
        lowOmoves = (xCount, oCount, movesMade)


def totalPercent():
    xPercent = round((xTokenCount/(xTokenCount + oTokenCount))*100, 3)
    oPercent = 100 - xPercent
    return xPercent, oPercent

Xp, Op = totalPercent()
print('Total Games played: {}\nX wins: {} O wins: {} ties: {}'.format(loops, xWins, oWins, ties))
print('X%: {} O%: {}'.format(Xp, Op))

# currently incorrectly determining the worst game of the better code
#print('Worst X game: {}/{} {}'.format(lowXmoves[0], lowXmoves[1], ' '.join([str(k) for k in lowXmoves[2]])))
#print('Worst O game: {}/{} {}'.format(lowOmoves[0], lowOmoves[1], ' '.join([str(k) for k in lowOmoves[2]])))
