import time
import helper
import rand
import rand55
import chooseMove1
import chooseMove11
import chooseMove1101
<<<<<<< HEAD


xScript, oScript = chooseMove11, chooseMove1101
loops = 50
=======
import chooseMove1102
import chooseMove1103
import checkWeight11

t = time.clock()
>>>>>>> alternate

script1, script2 = rand55, rand
print(script1, script2)
loops = 100

tokenCounts = {0: 0, 1: 0} # first script counts, second counts
wins = {0:0, 1:0, 2: 0} # first script wins, second wins, ties
lowTkr = {0:1, 1:1} # low tkr 1, 2 (initally 1 because looking for lower)
lowMoves = {0:[], 1:[]}


def playGame():
    currentBoard = '.'*27 + 'ox......xo' + '.'*27
    currentToken = 'x'
    done = False
    movesMade = []

    while currentBoard.count('.') != 0 and not done:
        if currentToken == 'x':
            chosenMove = script1.run(currentBoard, 'x')
            oppTkn = 'o'
        else:
            try:
                chosenMove = script2.run(currentBoard, 'o')
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

    tokenCounts[k%2] += xCount
    tokenCounts[(k+1)%2] += oCount

    if xCount > oCount:
<<<<<<< HEAD
        xWins += 1
        #print('x win', xCount, oCount, ' '.join([str(k) for k in movesMade]))
=======
        wins[k%2] += 1
>>>>>>> alternate
    elif oCount > xCount:
        wins[(k+1)%2] += 1
    else:
        wins[2] += 1

    script1, script2 = script2, script1


def totalPercent():
    tkr1 = round((tokenCounts[0]/(tokenCounts[0] + tokenCounts[1]))*100, 3)
    tkr2 = round(100 - tkr1, 3)

    wr1 = round(wins[0]/(wins[0] + wins[1]), 3)
    wr2 = round(1-wr1, 3)

    return tkr1, tkr2, wr1, wr2

tkr1, tkr2, wr1, wr2 = totalPercent()
print('Total Games played: {}\nScript1 wins: {}, Script2 wins: {}, ties: {}'.format(loops, wins[0], wins[1], wins[2]))
print('Script1 Win Rate: {} Script 2 Win Rate {}'.format(wr1, wr2))
print('Script1 TKR: {}, Script2 TKR: {}'.format(tkr1, tkr2))

# currently incorrectly determining the worst game of the better code
#print('Worst X game: {}/{} {}'.format(low1moves[0], low1moves[1], ' '.join([str(k) for k in low1moves[2]])))
#print('Worst O game: {}/{} {}'.format(low2moves[0], low2moves[1], ' '.join([str(k) for k in low2moves[2]])))

print('Time', round(time.clock()-t, 3))
