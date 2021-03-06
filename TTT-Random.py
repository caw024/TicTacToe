#! /usr/bin/env python3

# Random move TicTacToe competitor
Usage = '''
TTT-Random.py board={9-char} result_prefix={prefix} result_file={filename}
       will write a move to filename (if result_file is provided)
       else print move
   or
TTT-Random.py id=1 result_prefix=(prefix) result_file={filename}
       will write AUTHOR and TITLE to filename (if result_file is provided)
       else print them
'''

AUTHOR = 'P. Brooks'
TITLE = 'Random Mover'

import random, sys


''' Layout positions:
0 1 2
3 4 5
6 7 8
'''
# layouts look like "_x_ox__o_"


Wins = [[0,1,2],[3,4,5],[6,7,8],[0,3,6],[1,4,7],[2,5,8],[0,4,8],[2,4,6]]

AllBoards = {} # this is a dictionary with key = a layout, and value = its corresponding BoardNode

class BoardNode:
    def __init__(self,layout):
        self.layout = layout
        self.endstate = None # if this is a terminal board, endState == 'x' or 'o' for wins, of 'd' for draw, else None
        self.children = [] # all layouts that can be reached with a single move

        #Implement these
        self.best_move = -1
        self.moves_to_end = 0
        self.final_state = "d"

    #get info from children to get your info
    #look at children, find min num of moves to end, such that final state is 'x' or 'o', else play 'd'. Choose subgroup of children who will win, then who will be fastest, then pick a random child. else, pick a random draw. if lose, find the child who will take the longest, then pick randomly
    def print_me(self):
        print ('layout:',self.layout, 'endState:',self.endstate)
        #print ('children:',self.children)
        print ('best move:', self.best_move)
        print ('moves to end:',self.moves_to_end)
        print ('final expected state:', self.final_state)
        
def nummovesleft(string):
    i = 0
    for k in string:
        if k == "_":
            i += 1
    return i
    
def winstate(string):
    #diagonals
    global Wins
    for k in Wins:
        if string[k[0]] == 'x' and 'x' == string[k[1]] and string[k[2]] == 'x':
            return 'x'
        if string[k[0]] == 'o' and 'o' == string[k[1]] and string[k[2]] == 'o':
            return 'o'
    for m in string:
        if m == "_":
            return None
    return "d"

def whosemove(string):
    num = 0
    for k in string:
        if k == "x":
            num += 1
        elif k == "o":
            num -= 1
    #it's o's turn
    if num == 1:
        return "o"
    return "x"

def emptycells(string):
    m = []
    i = 0
    while i < len(string):
        if string[i] == "_":
            m.append(i)
        i += 1
    return m
        
def CreateAllBoards(layout):
    # recursive function to manufacture all BoardNode nodes and place them into the AllBoards dictionary
    global AllBoards
    if layout not in AllBoards:
        K = BoardNode(layout)
        #endstate
        K.endstate = winstate(layout)

        goodcells = emptycells(layout)
        currentmove = whosemove(layout)

        
        #print("win state with layout:",winstate(layout))
        if K.endstate == None:
            for k in goodcells:
                m = layout[:k] + currentmove + layout[k+1:]
                #children
                K.children.append(m)
            
        AllBoards[layout] = K
        #print("going")
        if K.endstate != None:
            #print('+')
            K.moves_to_end = 0
            K.best_move = -1
            K.final_state = K.endstate
        else:
            #print('-')
            statexlist, stateolist, statedlist = [],[],[]
            if currentmove == "x":
                statex = 100
                stateo = 0
            else:
                statex = 0
                stateo = 100
            stated = nummovesleft(layout)
            #print(statex,stateo,stated)
            #print("current move",currentmove)
            #print("original layout",layout)
            for k in goodcells:
                m = layout[:k] + currentmove + layout[k+1:]
                #can cause printing other stuff to happen
                CreateAllBoards(m)
                BigBad = AllBoards[m].final_state
                numofmovestoend = AllBoards[m].moves_to_end + 1
                if BigBad == 'x':
                    if currentmove == 'x':
                        if numofmovestoend == statex:
                            statexlist.append(k)
                        elif numofmovestoend < statex:
                            statexlist = []
                            statexlist.append(k)
                            statex = numofmovestoend
                    else:
                        if numofmovestoend == statex:
                            statexlist.append(k)
                        elif numofmovestoend > statex:
                            statexlist = []
                            statexlist.append(k)
                            statex = numofmovestoend
                elif BigBad == 'o':
                    if currentmove == 'o':
                        if numofmovestoend == stateo:
                            stateolist.append(k)
                        elif numofmovestoend < stateo:
                            stateolist = []
                            stateolist.append(k)
                            stateo = numofmovestoend
                    else:
                        if numofmovestoend == stateo:
                            stateolist.append(k)
                        elif numofmovestoend > stateo:
                            stateolist = []
                            stateolist.append(k)
                            stateo = numofmovestoend
                else:
                    statedlist.append(k)
                #print(m,statexlist,stateolist,statedlist)
            #print("to evaluate",statexlist,stateolist,statedlist)
            if 'x' == currentmove:
                if len(statexlist) >= 1:
                    K.best_move = random.choice(statexlist)
                    K.moves_to_end = statex
                    K.final_state = 'x'
                else:
                    if len(statedlist) >= 1:
                        K.best_move = random.choice(statedlist)
                        K.moves_to_end = stated
                        K.final_state = 'd'
                    else:
                        #print(len(stateolist))
                        K.best_move = random.choice(stateolist)
                        K.moves_to_end = stateo
                        K.final_state = 'o'
                        
            elif 'o' == currentmove:
                if len(stateolist) >= 1:
                    K.best_move = random.choice(stateolist)
                    K.moves_to_end = stateo
                    K.final_state = 'o'
                else:
                    if len(statedlist) >= 1:
                        K.best_move = random.choice(statedlist)
                        K.moves_to_end = stated
                        K.final_state = 'd'
                    else:
                        #print(len(statexlist))
                        K.best_move = random.choice(statexlist)
                        K.moves_to_end = statex
                        K.final_state = 'x'
        #K.print_me()
        '''"move number " + movenum(layout) +'''
        '''str(K.best_move) + ", "'''
        return "\nbest move for " + currentmove + " is " + directions(K.best_move) + "\n" + K.final_state + " is the expected final state in " +  str(K.moves_to_end) + " moves"

def movenum(layout):
    i = 0
    for k in layout:
        if k != "_":
            i += 1
    return str(i+1)
    
def directions(num):
    if num == -1:
        return 'game has ended'
    dirarray = ['top left', 'top mid', 'top right', 'middle left', 'center', 'middle right', 'bottom left', 'bottom middle', 'bottom right']
    return dirarray[num]


def main():
    if len(sys.argv) < 2:
        print (Usage)
        return
    dct = getargs()
    result = ''
    if 'id' in dct:
        result='author=%s\ntitle=%s\n' % (AUTHOR,TITLE)
    elif 'board' in dct:
        board=dct['board']
        if len(board) != 9:
            result='Error: board must be 9 characters'
        else:
            poss=[i for i in range(9) if board[i]=='_']
            if len(poss) > 0:
                i = random.choice(poss)
                #result = 
                result='move=%d\n' % i + CreateAllBoards(board) + '\n'
            else:
                result='move=-1\n(Come on, the game is done!)\n'
    if 'result_prefix' in dct:
        result = dct['result_prefix']+'\n'+result
    if 'result_file' in dct:
        try:
            f=open(dct['result_file'],'w')
            f.write(result)
            f.close()
        except:
            print ('Cannot open: %s\n%s\n' % (dct['result_file'],result))
    else:
        print (result)

def getargs():
    dct = {}
    for i in range(1,len(sys.argv)):
        sides = sys.argv[i].split('=')
        if len(sides) == 2:
            dct[sides[0]] = sides[1]
    return dct

main()



