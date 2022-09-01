# Algoritmo genetico para a soluçao N Rainhas

import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import random
import psutil
import time
import os

print('Valor Inicial de casos: ')
R = int(input())

#inicia a contagem do processamento atraves do pid do processo
exec = psutil.Process(os.getpid())

#gera possiveis soluçoes 
def Npop(PSolu,R): # -R é o tamanho da lista
    pop = []
    for z in range (PSolu):
        pop.append(random.sample(range(R), R))   
    return pop

# Gera Novos descendentes
def Gdescs(Ascendnts):
    Descednts = []
    for z in range(0,len(Ascendnts)-2,3):
        if muda():
            Descednts.extend(GeraDesc(Ascendnts[z:z+3]))
        else:    
            Descednts.extend(Ascendnts[z:z+3])
    return Descednts

#altera o gene ou item na lista
def GeraMut(Confirm):
    NovSoluc = Confirm[:]
    z,x=0,0
    while z==x:
        z = random.randint(0,len(Confirm)-1)
        x = random.randint(0,len(Confirm)-1)
    tp1 = NovSoluc[x]
    tp2 = NovSoluc[z]
    NovSoluc[z] = tp1
    NovSoluc[x] = tp2
    return NovSoluc 
   
#Seleciona os melhores individuos para nova geraçao
def NFit(Confirm):
    pont = (len(Confirm)-1)*len(Confirm)
    for z in range(0,len(Confirm)):
        for x in range(0,len(Confirm)):
            if z!=x:
                if z-Confirm[z] == x-Confirm[x] or z+Confirm[z] == x+Confirm[x]:
                    pont-=1       
    return pont/2            
  
# Cruzamento entre partes de individuos
def Cruza(Slc1,Slc2):
    n = int(len(Slc1)/2)
    NovSoluc1 = Slc1[:n] + Slc2[n:]
    NovSoluc2 = Slc1[n:] + Slc2[:n]
    return (NovSoluc1,NovSoluc2)

def muda():
    TxCruza = 2
    T = random.random()
    if TxCruza > T:
    	return T
    
#Gera novos descentes
def GeraDesc(Ascendnts): 
    descend = Ascendnts
    ftns = [NFit(each_sol) for each_sol in descend]
    descend.pop(ftns.index(min(ftns)))
    NovDescend = GeraMut(descend[random.randint(0, 1)])
    descend.append(NovDescend)
    return(descend) 

I = time.time()       # começo da contagem de tempo

PSolu = 45
Gera = 1000
Slcs = Npop(PSolu,R)
ftns = [NFit(item) for item in Slcs]
CritPara = False
PlotGrapic = []

x = 0
while x < Gera:
    for z in range(len(ftns)):
        if ftns[z] == R*(R-1)/2:
            print(Slcs[z])
            PlotGrapic = Slcs[0]
            CritPara = True
            break
        else:
            x+=1
        if CritPara:
            break

    Ngera = x    
    probability_matrix = [x/sum(ftns) for x in ftns]
    ns = np.random.choice([z for z in range(PSolu)],size = PSolu,p = probability_matrix)
    Ascendnts = [Slcs[z] for z in ns]
    Slcs = Ascendnts
    Slcs = Gdescs(Ascendnts)
    sol_fitness = [NFit(item) for item in Slcs]
    
F = time.time()    

M = (exec.memory_info()[0])/1000000 
print('tempo de execução:',(F - I),'ms \n')     
print('memoria:',M,'Mb \n')
print('Numero de gerações:',Ngera,'\n')