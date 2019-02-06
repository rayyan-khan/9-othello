# script to convert ai site transcript to a list of moves that can be read by lab 3

import sys, re

if len(sys.argv)<2:
    exit("Call with filename of othello.tjhsst.edu game transcript")

xscript = open(sys.argv[1], 'r').read()

brdaray = re.findall("[@o.]{64}", re.sub("$\\s+^\\d| ", "",
                                         xscript, flags=re.M))

mvray = [pos for odex, oth in enumerate(brdaray[1:]) for pos,tkn in
         enumerate(oth) if tkn != '.' and brdaray[odex][pos] == '.']

print("{}".format(mvray).replace(",","")[1:-1])
