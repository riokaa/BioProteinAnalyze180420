from queue import Queue #头文件定义

# -------------------- by:rayiooo --------------------
# Wrote by LJ's bf rayiooo, use tree and Breadth First Search to handle the problem.
# Only run less than 2 minutes.
# 要求：取出1.tab中的编号和GO，根据go-basic.obo中的is_a关系和part_of关系找到每个编号所有GO及GO的父、爷……GO。
# --------------------class define--------------------
# tree nodes
class Node(object):
    def __init__(self, value):
        self.value = value      # node value
        self.childList = []     # children
        self.color = 'white'    # color for bfs or dfs, white / gray / black

    def addChild(self, node):
        self.childList.append(node)

    def getValue(self):
        return self.value


# tree
class Tree(object):
    def __init__(self):
        self.headers = []
        self.gos = []

    def BFS(self, headerNode):  # breadth first search from headerName, return its all children
        self.setAllGoWhite()
        headerNode.color = 'red'
        res = []

        q = Queue()
        q.put(headerNode)
        while(not q.empty()):
            node = q.get()
            if(node.color == 'white'):
                res.append(node.getValue())
                for i in range(0, len(node.childList)):
                    q.put(node.childList[i])
                node.color = 'black'
            elif(node.color == 'red'):      # if is header
                for i in range(0, len(node.childList)):
                    q.put(node.childList[i])
                node.color = 'black'
        self.setAllGoWhite()
        print('res of '+headerNode.getValue()+' printing')
        return res


    def addHeader(self, node):
        self.headers.append(node)   # such as 1673 or 1697 etc.

    def addGo(self, node):
        self.gos.append(node)       # such as GO:0008150 or GO:0010467 etc.
        if(len(node.childList)==0):
            # if(node.getValue() == 'GO:0005099'):
            #     print('Oh shit!')
            text = getmid(goBasic, 'id: '+node.getValue()+'\n', '[Term]\n')
            if(text == ''):
                text = getmid(goBasic, 'alt_id: '+node.getValue()+'\n', '[Term]\n')
            addFatherGo(node.getValue(), text)

    def getHeaderOrCreate(self, headerName):    # return the header node named headerName, if not have then create
        for i in range(0, len(self.headers)):
            if(self.headers[i].getValue() == headerName):
                return self.headers[i]
        node = Node(headerName)
        self.addHeader(node)
        return node

    def getGoOrCreate(self, goName):    # return the GO node named nodeName, if not have then create
        for i in range(0, len(self.gos)):
            if(self.gos[i].getValue() == goName):
                return self.gos[i]
        node = Node(goName)
        self.addGo(node)
        return node

    def setAllGoWhite(self):
        # for i in range(0, len(self.headers)):
        #     self.headers[i].color = 'white'
        for i in range(0, len(self.gos)):
            self.gos[i].color = 'white'

# ---------------------fang fa define-------------------
# getmid函数：将id：GO：.......与下一个term之间的内容找出来
def getmid(a, b, c):    # get text from a between b and c
    if b in a and c in a:
        n1 = a.index(b)
        n2 = a[(n1):len(a)].index(c)+n1
        return a[n1:n2]
    return ''

# add relationship on tree
def addFatherGo(termGoName, text):
    currentTerm = tree.getGoOrCreate(termGoName)
    altIdBrothers = []
    for i in range(0, len(text)):
            if(text[i][:9] == 'is_a: GO:'):
                fatherGO = tree.getGoOrCreate(text[i][6:16])     # in tree, we call it childGo.
                currentTerm.addChild(fatherGO)
                # print(goBasic[i][6:16])
            elif(text[i][:25] == 'relationship: part_of GO:'):
                fatherGO = tree.getGoOrCreate(text[i][22:32])
                currentTerm.addChild(fatherGO)
                # print(goBasic[i][22:32])
            elif(text[i][:11] == 'alt_id: GO:'):
                # if(text[i][8:18] == 'GO:0005099'):
                #     print('Oh Shit!')
                altIdBrothers.append(tree.getGoOrCreate(text[i][8:18]))
    for i in range(0, len(altIdBrothers)):  # alt_id set the same childList to id
        altIdBrothers[i].childList = currentTerm.childList

# ************************* Main ************************
# read files
f = open('1.tab')
goList = f.readlines()
f.close()
f = open('go-basic.obo')
goBasic = f.readlines()
f.close()

# basic variable
tree = Tree()

# read 1.tab, store goList to the tree
temp = Node('0')    # store current header
for i in range(1,len(goList)):
# for i in range(1,505):    # debug line
    a = goList[i].split()
    if(temp.getValue() != a[0]):  # a new header
                                                # temp = Node(a[0])
                                                # tree.addHeader(temp)
        temp = tree.getHeaderOrCreate(a[0])
        print(a[0])
                                                # tempGo = Node(a[1])   # very wrong writing! must check whether the node exist.
                                                # tree.addGo(tempGo)    # very wrong writing! must check whether the node exist.
    tempGo = tree.getGoOrCreate(a[1])
    temp.addChild(tempGo)

# read go-basic.obo, store goBasic's father-child relationship to tree
# --Why I delete this part?
# --Because read all Terms waste a lot time. So we read Terms which and when we use it only.
# currentTerm = Node('0')
# for i in range(0, len(goBasic)):
#     if(goBasic[i][:6] == '[Term]'):
#         i += 1          # i = i + 1
#         currentTermName = goBasic[i][4:-1]
#         currentTerm = tree.getGoOrCreate(currentTermName)
#         # print(goBasic[i][4:-1])
#     elif(goBasic[i][:9] == 'is_a: GO:'):
#         fatherGO = tree.getGoOrCreate(goBasic[i][6:16])     # in tree, we call it childGo.
#         currentTerm.addChild(fatherGO)
#         # print(goBasic[i][6:16])
#     elif(goBasic[i][:25] == 'relationship: part_of GO:'):
#         fatherGO = tree.getGoOrCreate(goBasic[i][22:32])
#         currentTerm.addChild(fatherGO)
#         # print(goBasic[i][22:32])

# cal result and output
output = open('resultPlus.tab','w')
for i in range(0, len(tree.headers)):
    currentHeader = tree.headers[i]
    currentGoOfHeader = tree.BFS(currentHeader)
    for j in range(0, len(currentGoOfHeader)):
        output.write(currentHeader.getValue() + '\t' + currentGoOfHeader[j] + '\n')
output.close()
