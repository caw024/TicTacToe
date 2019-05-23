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
        self.parents = [] # all layouts that can lead to this one, by one move
        self.children = [] # all layouts that can be reached with a single move

        #Implement these
        self.bestmove = -1
        self.moves_to_end = 0
        self.finalstate = "d"

    #get info from children to get your info
    #look at children, find min num of moves to end, such that final state is 'x' or 'o', else play 'd'. Choose subgroup of children who will win, then who will be fastest, then pick a random child. else, pick a random draw. if lose, find the child who will take the longest, then pick randomly
    def print_me(self):
        print ('layout:',self.layout, 'endState:',self.endstate)
        print ('parents:',self.parents)
        print ('children:',self.children)
        print ('best move:', self.bestmove)
        print ('moves to end:',self.move_to_end)
        print ('final expected state:', self.finalstate)

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
        
def CreateAllBoards(layout,parent):
    # recursive function to manufacture all BoardNode nodes and place them into the AllBoards dictionary
    global AllBoards
    if layout in AllBoards:
        temp = AllBoards[layout]
        temp.parents.append(parent)
        AllBoards[layout] = temp
    else:
        K = BoardNode(layout)
        #endstate
        K.endstate = winstate(layout)
        K.parents.append(layout)

        goodcells = emptycells(layout)
        currentmove = whosemove(layout)
        #print("win state with layout:",winstate(layout))
        if K.endstate == None:
            for k in goodcells:
                m = layout[:k] + currentmove + layout[k+1:]
                #children
                K.children.append(m)
        K.print_me()

        AllBoards[layout] = K

        if K.endstate == None:
            for k in goodcells:
                m = layout[:k] + currentmove + layout[k+1:]
                CreateAllBoards(m,layout)
    
CreateAllBoards("_________",[])
print("length of board",len(AllBoards))
mynum, myx, myo, myd, myNone = 0,0,0,0,0
for k in AllBoards:
    mynum += len(AllBoards[k].children)
    Lmao = AllBoards[k].endstate
    if Lmao == "x":
        myx += 1
    elif Lmao == "o":
        myo += 1
    elif Lmao == "d":
        myd += 1
    else:
        myNone += 1
print("mynum:",mynum)
print("myx:",myx)
print("myo:",myo)
print("myd:",myd)
print("myNone:",myNone)
