#Simulated Anneling

import pandas as pd
import matplotlib.pyplot as plt
#from pandas.plotting import register_matplotlib_converters
#register_matplotlib_converters()
from collections import Counter
import random
from random import choice
import psutil
import math
import time
import sys
import os

print('Valor Inicial de casos: ')
R = int(input())



def EstInit(R):
    global List_Glob
    Lst = list(random.randrange(R) for i in range(R))
    List_Glob = Lst
    return Lst
           
def h(state):
    ts1, ts2, ts3 = [Counter() for i in range(3)]
    for li, col in enumerate(state):
        ts3[li + col] += 1
        ts2[li - col] += 1
        ts1[col] += 1
        
    h = 0  
    for count in [ts1, ts2, ts3]:
        for key in count:
            h += count[key] * (count[key] - 1) / 2
    return -h

def goal_test(state):
    ts1, ts2, ts3 = (set() for i in range(3))
    for li, col in enumerate(state):
        if col in ts1 or li - col in ts2 or li + col in ts3:
            return False
        ts3.add(li + col)
        ts2.add(li - col)
        ts1.add(col)
    return True

def EstProx(std):
    estProx = []
    for linha in range(R):
        for coluna in range(R):
            if coluna != std[linha]:
                BestEst = list(std)
                BestEst[linha] = coluna  
                estProx.append(list(BestEst))  
    return estProx

def CriaEst(std):
    return choice(EstProx(std)) #escolha aleatoria

# Variação da temperatura
def MediaTemp(Temp=100, TxDec=0.010,iterac = 99999):
    return lambda temp: (Temp * math.exp(-TxDec * temp)if iterac>temp else 0)

#Tempera
def TempS(std,MediaTemp = MediaTemp()):
    att = std 
    ObjAtt = h(att) 
    for i in range(sys.maxsize): 
        Temp = MediaTemp(i)
        print(Temp)
        global Mtemp
        Mtemp.append(Temp)
        if Temp == 0 or goal_test(att):
            return att
        vizin = CriaEst(att)
        global Mvizin
        Mvizin.append(vizin)
        print(vizin)
        if not vizin:
            return att
        NewObj = h(vizin)
        media = NewObj - ObjAtt
        if media > 0 or math.exp(media / Temp) > random.uniform(0.0, 1.0):
            att = vizin
            ObjAtt = NewObj

###chamadas
Mtemp =[]
Mvizin = []
List_Glob = []
eixos = [i for i in range(R)]
Estd_I  = pd.DataFrame(index=(eixos),columns=(eixos))
Estd_F = pd.DataFrame(index=(eixos),columns=(eixos))
std = EstInit(R)     #Estado Inicial
for ts2 in range(len(List_Glob)):  #preenche tabuleiro
    Estd_I[ts2][List_Glob[ts2]] = 'rainha'
    
#executando algoritimo    
I = time.time()
exec = psutil.Process(os.getpid())
Tst = TempS(std)
M = (exec.memory_info()[0])/1000000 
F = time.time()
tempo_total = F-I 

for ts1 in range(len(Tst)):
    Estd_F[ts1][Tst[ts1]] = "rainha"
indices = [i for i in Mtemp]    
colunas = [j for j in range(len(Mtemp))]
Date = {'Heuristica': indices,
        'Iterações': colunas}
        
Plot = pd.DataFrame(Date,columns=['Heuristica','Iterações'])
Plot.plot(x='Iterações',y='Heuristica',kind='line')
plt.show()


print('Memoria :',M,'Mb \n')
print('Tempo:',(F-I) ,'seg \n')  