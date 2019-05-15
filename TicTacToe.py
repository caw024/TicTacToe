#input: string

numofgames = 0
numXwin= 0
numOwin = 0
numdraw = 0
states = set()

def checkctr(char):
    if char == "X":
        global numXwin
        numXwin += 1
    elif char == "O":
        global numOwin
        numOwin += 1
    else:
        global numdraw
        numdraw += 1

def winstate(string):
    #diagonals
    ctr = string[4]
    if ctr != "_" and string[0] == ctr and ctr == string[8]:
        checkctr(ctr)
        return True
    if ctr != "_" and string[2] == ctr and ctr == string[6]:
        checkctr(ctr)
        return True
    #row and column
    for k in range(0,3):
        m = 3*k
        if string[k] != "_" and string[k] == string[k+3] and string[k] == string[k+6]:
            checkctr(string[k])
            return True
        elif string[m] != "_" and string[m] == string[m+1] and string[m] == string[m+2]:
            checkctr(string[m])
            return True
    filled = 0
    for k in string:
        if k == "_":
            filled = 1
    if filled == 0:
        checkctr(0)
        return True
    return False

def emptycells(string):
    m = []
    i = 0
    while i < len(string):
        if string[i] == "_":
            m.append(i)
        i += 1
    return m

def allrotations(string):
    rot = set()
    order = [string[k] for k in range(0,9)]
    inverse = [string[2-i+3*k] for k in range(0,3) for i in range(0,3)]
    i = 0
    while i < 4:
        myorder = []
        for k in range(0,3):
            myorder.extend([order[k+6],order[k+3],order[k]])
        myorder = "".join(myorder)
        #print(myorder)
        rot.add(myorder)
        order = myorder[:]
        i += 1
    i = 0
    while i < 4:
        myorder = []
        for k in range(0,3):
            myorder.extend([inverse[k+6],inverse[k+3],inverse[k]])
        myorder = "".join(myorder)
        #print(myorder)
        rot.add(myorder)
        inverse = myorder[:]
        i += 1
    return rot



def TicTacToe1(string,currentmove):
    m = ''
    goodcells = emptycells(string)
    for k in goodcells:
        m = string[:k] + currentmove + string[k+1:]
        global states
        states.add(m)

        if winstate(m) == True:
            global numofgames
            numofgames += 1
            #print(numofgames)
            #print(m)
        else:
            if currentmove == "X":
                TicTacToe1(m,"O")
            else:
                TicTacToe1(m,"X")

def TicTacToe(string,startmove):
   TicTacToe1(string,startmove)
   global numofgames, numXwin, numOwin,numdraw,states
   print(numofgames,numXwin,numOwin,numdraw,len(states)+1 )

   i = 0
   specialstates = set()
   mycopy = states.copy()
   for k in states:
       specialset = allrotations(k)
       ele = specialset.pop()
       specialset.add(ele)
       if ele in mycopy:
           specialstates.add(ele)
           for a in specialset:
               mycopy.remove(a)
               #print(len(mycopy))
       #print(len(specialstates))
        
   print(len(specialstates)+1)
      
    
TicTacToe("_________","X")
#print( allrotations('012345678') )
