import rand
import chooseMove1
import helper


xTokenCount, oTokenCount, xWins, oWins, ties = 0, 0, 0, 0, 0
lowXtkr, lowOtkr = 1, 1
lowXmoves, lowOmoves = (), ()
loops = 1000


def totalPercent():
    xPercent = round(xTokenCount/(xTokenCount + oTokenCount), 4)*100
    oPercent = 100 - xPercent
    return xPercent, oPercent

def playGame():
    currentBoard = '.'*27 + 'ox......xo' + '.'*27
    currentToken = 'x'
    xScript, oScript = rand, chooseMove1
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

    xTkr = round(xTokenCount/(xTokenCount + oTokenCount), 2)
    oTkr = 1 - xTkr

    if xTkr > oTkr:
        xWins += 1
    elif oTkr > xTkr:
        oWins += 1
    else:
        ties += 1

    if xTkr < lowXtkr:
        lowXtkr = xTkr
        lowXmoves = (xCount, oCount, movesMade)
    if oTkr < lowOtkr:
        lowOtkr = oTkr
        lowOmoves = (xCount, oCount, movesMade)


print('Total Games played: {}\nX wins: {} O wins: {}'.format(loops, xWins, oWins))
Xp, Op = totalPercent()
print('X%: {} O%: {}'.format(Xp, Op))
print('Worst X game: {}/{} {}'.format(lowXmoves[0], lowXmoves[1], ' '.join([str(k) for k in lowXmoves[2]])))
print('Worst O game: {}/{} {}'.format(lowOmoves[0], lowOmoves[1], ' '.join([str(k) for k in lowOmoves[2]])))
