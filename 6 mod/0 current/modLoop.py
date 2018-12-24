import time
import helper
import rand
import rand55
import chooseMove12
import chooseMove11

t = time.clock()

script1, script2 = chooseMove12, rand
print(script1, script2)
loops = 1

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
            chosenMove = script2.run(currentBoard, 'o')
            oppTkn = 'x'
        currentBoard = helper.makeFlips\
            (currentBoard, currentToken, chosenMove)[0]
        movesMade.append(chosenMove)
        checkPass = helper.nextMoves(currentBoard, oppTkn)[0]
        if checkPass: # checkPass == 0 if opponent has no moves
            currentToken = oppTkn
        else:
            checkPassAgain = helper.nextMoves(currentBoard, currentToken)[0]
            if not checkPassAgain: # neither player can move
                done = True

    xCount, oCount = helper.getScore(currentBoard)
    return xCount, oCount, movesMade


for k in range(loops):
    xCount, oCount, movesMade = playGame()

    tokenCounts[k%2] += xCount
    tokenCounts[(k+1)%2] += oCount

    if xCount > oCount:
        wins[k%2] += 1
    elif oCount > xCount:
        wins[(k+1)%2] += 1
    else:
        wins[2] += 1

    script1, script2 = script2, script1


def totalPercent():
    # token capture rates of each script
    tkr1 = round((tokenCounts[0]/(tokenCounts[0] + tokenCounts[1]))*100, 3)
    tkr2 = round(100 - tkr1, 3)

    # win and tie rates
    wr1 = round((wins[0]/loops)*100, 3)
    wr2 = round((wins[1]/loops)*100, 3)
    tr = round((wins[2]/loops)*100, 3)

    return tkr1, tkr2, wr1, wr2, tr


tkr1, tkr2, wr1, wr2, tr = totalPercent()
print('Total Games played: {}\nScript1 wins: {}, Script2 wins: {}, ties: {}'
      .format(loops, wins[0], wins[1], wins[2]))
print('Script1 Win Rate: {}% Script 2 Win Rate {}% Tie Rate: {}%'.format(wr1, wr2, tr))
print('Script1 TKR: {}%, Script2 TKR: {}%'.format(tkr1, tkr2))

# currently incorrectly determining the worst game of the better code
#print('Worst X game: {}/{} {}'.format(low1moves[0], low1moves[1], ' '.join([str(k) for k in low1moves[2]])))
#print('Worst O game: {}/{} {}'.format(low2moves[0], low2moves[1], ' '.join([str(k) for k in low2moves[2]])))

print('Time', round(time.clock()-t, 3))
