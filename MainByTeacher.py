def obtain_gene(lst):
    # obtain full information on the first gene from a gene+GO list, input the gene+GO list, output the list for the first gene
    a=0
    while lst[a].split()[0]==lst[a+1].split()[0]:
        a+=1
    output_list=lst[:a+1]
    return output_list
def make_new_list(lst):
    # remove the first gene and make a new list from a gene+GO list
    a = 0
    while lst[a].split()[0] == lst[a + 1].split()[0]:
        a += 1
    output_list = lst[a+1:]
    return output_list
def obtain_go_list(lst):
    #obtain GO list from a gene+GO list
    list2=[]
    for line in lst:
        list3=line.split()
        list2.append(list3[1])
    return list2
def find_father(str):
    #find all the father terms for a specific GO
    f=open('go-basic.obo')
    ont=f.readlines()
    f.close()
    a=0
    while ont[a]!='id: '+str+'\n' and ont[a]!='alt_id: '+str+'\n':
        a+=1
    b=0
    while ont[a+b]!='[Term]\n':
        b+=1
    str_term=ont[a:a+b]
    output=[]
    for line in str_term:
        if line[:4]=='is_a':
            output.append(line[6:16])
        elif line[:21]=='relationship: part_of':
            output.append(line[22:32])
        else:
            continue
    return output
def expand_go(list):
    #find the parent terms for all the GO's in a GO list
    list2=list
    for line in list:
        list2=list2+find_father(line)
    return list2
def shrink_list(list):
    # remove repeting GO terms from a GO list
    output=[]
    for line in list:
        while not(line in output):
            output.append(line)
    return output
def gene_name(list):
    # obtain the gene name of the first gene from a gene+GO list
    stri=list[0].split()[0]
    return stri
def find_all_go(lst):
    #find all the GO terms related to a specific gene, input the gene+GO list, output the full gene+GO list
    go_list=obtain_go_list(lst)
    gene=gene_name(lst)
    a=len(go_list)
    b=0
    print(go_list)
    while a!=b:
        a=len(go_list)
        go_list=expand_go(go_list)
        go_list=shrink_list(go_list)
        b=len(go_list)
    output=[]
    for line in go_list:
        output.append(gene+'\t'+line+'\n')
    return(output)
def find_end(list):
    #determine if the gene+GO list has reached the end of the file.
    a=1
    if list[0].split()[0]=='124286':
        a=0
    return a

f=open('1.tab')
g=open('result.txt','w')
full_list=f.readlines()
f.close()
while find_end(full_list):
    gene_list = obtain_gene(full_list)
    print(gene_list)
    final_list=find_all_go(gene_list)
    full_list=make_new_list(full_list)
    g.writelines(final_list)
final_list=find_all_go(full_list)
g.writelines(final_list)
g.close()
