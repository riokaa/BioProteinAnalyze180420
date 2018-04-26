from queue import Queue #头文件定义

# wrote by LJ

f=open('1.tab')
data1=f.readlines()
f.close()
length=len(data1)
z=[]
f=open('go-basic.obo')
data=f.readlines()
f.close()
q = Queue()
y=[]
d=[]
#getmid函数：将id：GO：blabla与下一个term之间的内容找出来
def getmid(a, b, c):
    n1 = a.index(b)
    n2 = a[(n1):len(a)].index(c)+n1
    return a[n1:n2]
# getmidope函数：将c列表中的GO们进行getmid操作
def getmidope(c):
    # 将c列表中的GO们进行getmid操作
    for i in range(0, len(c) ):
        go = c[i]
        i=i+1
        if 'id: ' + go + '\n' in data:
            g = getmid(data, 'id: ' + go + '\n', '[Term]\n')
            # 将每个注释中is_a,part_of提取出来，导入q队列
            for j in range(0, len(g)):
                if g[j][0] == ('r') and g[j][20] == ('f'):
                    t = g[j][22:32]
                    y.append(t)
                    q.put(t)
                    j=j+1
                elif g[j][0] == ('i') and g[j][1] == ('s') and g[j][3]==('a'):
                    t = g[j][6:16]
                    q.put(t)
                    y.append(t)
                    j=j+1
                else:
                    j=j+1
# 将每个GO的getmid中is_a,part_of提取出来，导入y列表
def extract(g):
    y = []
    for j in range(0, len(g)):
        if g[j][0] == ('i') and g[j][1] == ('s') and g[j][3]==('a'):
            t = g[j][6:16]
            y.append(t)
            j = j + 1
        elif g[j][0] == ('r') and g[j][20] == ('f'):
            t = g[j][22:32]
            y.append(t)
            j = j + 1
        else:
            j = j + 1
#将源文件分割成列表
for i in range(1,length):
    a=data1[i].split()
    i=i+1
    z.append(a)
#slice函数：看每个元素中的第一个数相等不，输出同一个proteinID的GOacc于新列表
def slice(z):
    c=[]
    idStore = 0
    for n in range(0,length):
        if z[n][0]==z[n+1][0]:
            c.append(z[n][1])
        else:
            idStore = z[n][0]
            c.append(z[n][1])
            #c.append(z[n][0])
            del z[:n+1]
            break
    # 将c列表中的GO们进行getmid操作
    #q = Queue()
    for i in range(0, len(c) ):
        go = c[i]
        i=i+1
        if 'id: ' + go + '\n' in data:
            g = getmid(data, 'id: ' + go + '\n', '[Term]\n')
            # 将每个注释中is_a,part_of提取出来，导入c列表
            for j in range(0, len(g)):
                if g[j][0] == ('r') and g[j][20] == ('f'):
                    t = g[j][22:32]
                    q.put(t)
                    y.append(t)
                    j=j+1
                elif g[j][0] == ('i') and g[j][1] == ('s') and g[j][3]==('a'):
                    t = g[j][6:16]
                    q.put(t)
                    y.append(t)
                    j=j+1
                else:
                    j=j+1
        #刚刚的操作中新建了一个队列q，之后进一个出一个流水作业，让所有爸爸都过一遍getmidope函数
        while(not q.empty()):
            d.append(q.get())
            getmidope(d)
            list.clear(d)
        for k in y:
            if k not in c:
                c.append(k)
    print(c)
    for i in range(0, len(c)):
        output.write(idStore + '\t' + c[i] + '\n')

    list.clear(c)

#写出所有的proteinid下的GO
output = open('result.tab','w')
while z is not []:
    slice(z)
output.close()


