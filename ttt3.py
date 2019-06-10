#!usr/bin/python3

import sys
import random

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
        return "move number " + movenum(layout) + "\nbest move for " + currentmove + " is " + str(K.best_move) + ", " + directions(K.best_move) + "\n" + K.final_state + " is the expected final state in " +  str(K.moves_to_end) + " moves"

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
    return "located at" + dirarray[num]
    

def main():
    k = len(sys.argv)
    print(k)
    finals = ""
    i = 1

    f = 0
    order = []
    
    while i < k:
        print(sys.argv[i])
        if sys.argv[i][0:2] == "id":
            
        elif sys.argv[i][0:5] == "board":
            pass
        elif sys.argv[i][0:11] == "cutoff_time":
            pass
        elif sys.argv[i][0:11] == "result_file":
            f = open(sys.argv[i][12:],'w')
        elif sys.argv[i][0:13] == "result_prefix":
            finals += sys.argv[i][14:] + "\n"
        else:
            print("unidentified argument " + sys.argv[k])
        i += 1

    print( CreateAllBoards(sys.argv[1]) )
    if f == 0:
        print(finals)
    else:
        f.close()
    
main()

