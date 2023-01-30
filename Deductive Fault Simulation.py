####################################################################################################################
#                               Vishakh V, M.Tech VLSI Design                                            #
####################################################################################################################
# Assignment No.1

# Deductive Fault Simulation

import re
import sys
import copy


#Extract netlist from file

with open('Netlist.txt', "r") as file:
    lines = file.readlines()
    
netl = []
k = 0

for x in range(0,len(lines)):
    netl.insert(k,lines[x].strip())
    k+=1
    
##print(netl)

#Removing Input node lines in file by copying to another variable netla

netla = copy.deepcopy(netl)

k = 0
length = len(netla)

while(k<length):
    if not (netla[k].find("inpt")>0 or netla[k].find("nand")>0 or netla[k].find("and")>0 or
            netla[k].find("or")>0 or netla[k].find("nor")>0 or netla[k].find("xor")>0 or
            netla[k].find("xnor")>0 or netla[k].find("buff")>0 or netla[k].find("not")>0 or
            netla[k].find("from")>0):
        netla.pop(netla.index(netla[k]))
        length = len(netla) 
    else:
        k+=1

##print(netla)

#Converting string to list from netlist
        
k = 0
a = []

for eachline in netla:
    temp = eachline.split()
    a.insert(k,temp)
    k+=1
    
##print(a) 


#Finding the Fanout Branches

l = 0
arr = []

for i in range(len(a)):
    curnode = a[i][1]
    repl = a[i][0]
    for j in range(len(a)):
        for k in range(len(a[j])):
            if (a[j][2] == 'from' and a[j][0] != repl and a[j][k] == curnode):
                arr.append([a[j][0],repl])
                break

##print(arr)

#Separate FROM and INPUT nodes

k = 0
length = len(netl)
frminp = []
l = 0

while(k<length):
    if (netl[k].find("from")>0 or netl[k].find("inpt")>0):
        frminp.insert(l,netl[k])
        l+=1
        netl.pop(netl.index(netl[k])) 
        length = len(netl) 
    else:
        k+=1
     
##print (netl)
##print (frminp)


#Extract all GATE node details from text
        
k = 0
extract1 = []

for eachline in netl:
    temp = eachline.split()
    extract1.insert(k,temp)
    k+=1

k = 0
extract2 = []

for eachline in frminp:
    temp = eachline.split()
    extract2.insert(k,temp)
    k+=1    
 
##print(extract1,'\n',extract2)

i = 0
ext1 = []
ext2 = []

for i in range(0,len(extract1),2):
    ext1.append([extract1[i][0],extract1[i][2],extract1[i][4],extract1[i+1]])

j = 0

for i in range(len(extract2)):
    if(extract2[i][2] == 'from'):
        ext2.append([extract2[i][0],'fanout',arr[j][1]])
        j+=1
    else:
        ext2.append([extract2[i][0],extract2[i][2],'--'])

    
#print('\next1\n\n',ext1,'\n\next2\n\n',ext2)


node = [chr(97+x) for x in range(len(a))]
state = ['x' for x in range(len(node))]

print ('Node\tName\tType\tFanin\tInputs\n')

for elt in range(len(ext2)):
    if(ext2[elt][1] == 'inpt'):
        print(int(ext2[elt][0]),'\t',node[int(ext2[elt][0])-1],'\t',ext2[elt][1],'\t\t',ext2[elt][2])
    else:
        print(int(ext2[elt][0]),'\t',node[int(ext2[elt][0])-1],'\t',ext2[elt][1],'\t',ext2[elt][2])
    
for elt in range(len(ext1)):
    print(int(ext1[elt][0]),'\t',node[int(ext1[elt][0])-1],'\t',ext1[elt][1],'\t',ext1[elt][2],'\t',list(map(int,ext1[elt][3])))

i = 0
ext3 = copy.deepcopy(ext1)

for item in arr:
    find = item[0]
    repl = item[1]
    for elt in extract1:
        for i in range(len(elt)):
            if elt[i] == find:
                elt[i] = repl

print ('\n\n')

for i in range(len(ext2)):
    if(ext2[i][1] == 'inpt'):
        state[i] = int(input('Enter input for node '+ext2[i][0]+' or '+node[int(ext2[i][0])-1]+': '))



def Evaluate_Gate(gate, fanin, inp1, inp2 = 'X', inp3 = 'X', inp4 = 'X'):

    out = 'X'
    if (gate == 'not'):
        out = not inp1
    elif (gate == 'buff'):
        out = inp1
        
    elif (gate == 'and' and fanin == 2):
        out = inp1 and inp2
    elif (gate == 'and' and fanin == 3):
        out = inp1 and inp2 and inp3
    elif (gate == 'and' and fanin == 4):
        out = inp1 and inp2 and inp3 and inp4
        
    elif (gate == 'or' and fanin == 2):
        out = inp1 or inp2
    elif (gate == 'or' and fanin == 3):
        out = inp1 or inp2 or inp3
    elif (gate == 'or' and fanin == 4):
        out = inp1 or inp2 or inp3 or inp4

    elif (gate == 'nand' and fanin == 2):
        out = not (inp1 and inp2)
    elif (gate == 'nand' and fanin == 3):
        out = not (inp1 and inp2 and inp3)
    elif (gate == 'nand' and fanin == 4):
        out = not (inp1 and inp2 and inp3 and inp4)

    elif (gate == 'nor' and fanin == 2):
        out = not (inp1 or inp2)
    elif (gate == 'nor' and fanin == 3):
        out = not (inp1 or inp2 or inp3)
    elif (gate == 'nor' and fanin == 4):
        out = not (inp1 or inp2 or inp3 or inp4)

    elif (gate == 'xor' and fanin == 2):
        out = (inp1 and (not inp2)) or (not (inp1) and inp2)
    
    elif (gate == 'xnor' and fanin == 2):
        out = (inp1 and inp2) or ((not inp1) and (not inp2))

    return out


                
while (state.count('x')>0):
    
    for item in arr:
        state[int(item[0])-1] = state[int(item[1])-1]

    for item in ext1:
        if (int(item[2]) == 1):
            state[int(item[0])-1] = int(Evaluate_Gate (item[1],int(item[2]),state[int(item[3][0])-1]))
        elif (int(item[2]) == 2 and state[int(item[3][0])-1] != 'x' and state[int(item[3][1])-1] != 'x'):
            state[int(item[0])-1] = int(Evaluate_Gate (item[1],int(item[2]),state[int(item[3][0])-1],state[int(item[3][1])-1]))
        elif (int(item[2]) == 3 and state[int(item[3][0])-1] != 'x' and state[int(item[3][1])-1] != 'x' and state[int(item[3][2])-1] != 'x'):
            state[int(item[0])-1] = int(Evaluate_Gate (item[1],int(item[2]),state[int(item[3][0])-1],state[int(item[3][1])-1],state[int(item[3][2])-1]))
        elif (int(item[2]) == 4 and state[int(item[3][0])-1] != 'x' and state[int(item[3][1])-1] != 'x' and state[int(item[3][2])-1] != 'x' and state[int(item[3][3])-1] != 'x'):
            state[int(item[0])-1] = int(Evaluate_Gate (item[1],int(item[2]),state[int(item[3][0])-1],state[int(item[3][1])-1],state[int(item[3][2])-1],state[int(item[3][3])-1]))

##print('\n\nNode number\tNode\tTrue Value\n')
##for i in range(len(node)):
##    print(i+1,'\t\t',node[i],'\t',state[i])
    

    
print('\n\nDeductive Fault Simulation\n')

faultlist = []
old = []

for i in range(len(node)):
    faultlist.insert(i,[node[i]+str(int(not(state[i])))])

#For Fanout Branches
    
for item in arr:
    
    set1 = set(faultlist[int(item[0])-1])
    set2 = set(faultlist[int(item[1])-1])
    old = faultlist[int(item[0])-1]
    faultlist[int(item[0])-1] = list(set1.union(set2))
    if (old != faultlist[int(item[0])-1]):
        for item in ext3:
            if (item[1] == 'not'):
                set1 = set(faultlist[int(item[3][0])-1])
                setop = set(faultlist[int(item[0])-1])
                faultlist[int(item[0])-1] = list(set1.union(setop))
                
            elif (item[1] == 'buff'):
                set1 = set(faultlist[int(item[3][0])-1])
                setop = set(faultlist[int(item[0])-1])
                faultlist[int(item[0])-1] = list(set1.union(setop))
                
            elif (item[1] == 'and' or item[1] == 'nand'):
                set1 = set(faultlist[int(item[3][0])-1])
                set2 = set(faultlist[int(item[3][1])-1])
                setop = set(faultlist[int(item[0])-1])
                ip1 = state[int(item[3][0])-1]
                ip2 = state[int(item[3][1])-1]

                if (ip1 == 0 and ip2 == 0):
                    faultlist[int(item[0])-1] = list((set1.intersection(set2)).union(setop))
                elif (ip1 == 0 and ip2 == 1):
                    faultlist[int(item[0])-1] = list((set1.difference(set2)).union(setop))
                elif (ip1 == 1 and ip2 == 0):
                    faultlist[int(item[0])-1] = list((set2.difference(set1)).union(setop))
                elif (ip1 == 1 and ip2 == 1):
                    faultlist[int(item[0])-1] = list((set1.union(set2)).union(setop))
                    
            elif (item[1] == 'or' or item[1] == 'nor'):
                set1 = set(faultlist[int(item[3][0])-1])
                set2 = set(faultlist[int(item[3][1])-1])
                setop = set(faultlist[int(item[0])-1])
                ip1 = state[int(item[3][0])-1]
                ip2 = state[int(item[3][1])-1]

                if (ip1 == 0 and ip2 == 0):
                    faultlist[int(item[0])-1] = list((set1.union(set2)).union(setop))
                elif (ip1 == 0 and ip2 == 1):
                    faultlist[int(item[0])-1] = list((set2.difference(set1)).union(setop))
                elif (ip1 == 1 and ip2 == 0):
                    faultlist[int(item[0])-1] = list((set1.difference(set2)).union(setop))
                elif (ip1 == 1 and ip2 == 1):
                    faultlist[int(item[0])-1] = list((set1.intersection(set2)).union(setop))

            elif (item[1] == 'xor' or item[1] == 'xnor'):
                set1 = set(faultlist[int(item[3][0])-1])
                set2 = set(faultlist[int(item[3][1])-1])
                setop = set(faultlist[int(item[0])-1])
                faultlist[int(item[0])-1] = list((set1.union(set2)).union(setop))
                
print('\nTest vector : ')
for i in range(len(ext2)):
    if(ext2[i][1] == 'inpt'):
        print('\t',node[int(ext2[i][0])-1],'=',state[int(ext2[i][0])-1])

        
print('\n\nNode number\tNode\tTrue value\tFaults detectable\n')
for i in range(len(faultlist)):
     print(i+1,'\t\t',node[i],'\t',state[i],'\t\t',faultlist[i])
     
sys.exit(0);


