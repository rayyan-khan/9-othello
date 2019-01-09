import time
import helper
import rand
import chooseMove1
import chooseMove2
import chooseMove3
import chooseMove4

t = time.clock()
results = open('results.txt', 'a')
script1, script2 = rand, chooseMove3
loops = 1000

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

    xTkr = xCount/(xCount + oCount)
    oTkr = oCount/(xCount + oCount)

    if xTkr < lowTkr[k%2]:
        lowTkr[k%2] = xTkr
        lowMoves[k%2] = [xCount, oCount, movesMade]
    if oTkr < lowTkr[(k+1)%2]:
        lowTkr[(k+1)%2] = oTkr
        lowMoves[(k+1)%2] = [oCount, xCount, movesMade]

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


# printing methods
def output(s):
    global results
    print(s)
    results.write('\n' + s)


def scriptName(script):
    s = str(script)
    return s[s.rfind('\\') + 1: s.find('.') + 3]


# printing
tkr1, tkr2, wr1, wr2, tr = totalPercent()
script1, script2 = scriptName(script1), scriptName(script2)
output('\nNEW GAME: {} vs. {}'.format(scriptName(script1), scriptName(script2)))

output('Total Games played: {}\n{} wins: {}, {} wins: {}, ties: {}'
      .format(loops, script1, wins[0], script2, wins[1], wins[2]))

output('{} Win Rate: {}%, {} Win Rate {}% Tie Rate: {}%'.format(script1, wr1, script2, wr2, tr))

output('{} TKR: {}%, {} TKR: {}%'.format(script1, tkr1, script2, tkr2))

output('Worst {} game: {}/{} {}'
       .format(script1, lowMoves[0][0], lowMoves[0][1], ' '.join([str(k) for k in lowMoves[0][2]])))
output('Worst {} game: {}/{} {}'
       .format(script2, lowMoves[1][0], lowMoves[1][1], ' '.join([str(k) for k in lowMoves[1][2]])))

output('Time: {} seconds'.format(round(time.clock() - t, 3)))
