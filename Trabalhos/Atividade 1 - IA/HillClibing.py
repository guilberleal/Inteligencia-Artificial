#HillClimbing  

import matplotlib.pyplot as plt
import pandas as pd
import psutil
import random
import time
import os

print('Valor Inicial de casos: ')
R = int(input())


Verificar = [] 

def print_board(state_board): 
    for z in range(len(state_board)):
        for x in range(len(state_board)):
            if state_board[x] == z:
                Estd_F[z][x] = 'rainha'

#verifica se a conflito                 
def conflicted(state, li, coln):
    return any(Conft(li, coln, state[c], c)for c in range(coln))
    
def Conft(li1, coln1, li2, coln2):
    return ( (li1 == li2 or  # linha
              coln1 == coln2 or  #  coluna
              li1 - coln1 == li2 - coln2 or  #  \ diagonal
              li1 + coln1 == li2 + coln2 ))  #  / diagonal

def goal_test(state):
    if state[-1] == -1:
        return False
    return not any(conflicted(state, state[coln], coln)
                  for coln in range(len(state)))

def EstProx(R,std):
    EstdProx = []
    for li in range(R):    
        for coln in range(R):
            if coln != std[li]:
                aux = list(std)
                aux[li] = coln  
                EstdProx.append(list(aux))  
    return EstdProx

#verifica os estados
def h(std):
    NConflitos = 0
    for (l1, c1) in enumerate(std):
        for (l2, c2) in enumerate(std):
            if (l1, c1) != (l2, c2):
                NConflitos += Conft(l1, c1, l2, c2)
              
    return -NConflitos/2

def FindVizn(V, std):
    melhorVz = []  #lista de vizinhos
    Vz = max(V, key=lambda std: h(std))
    melhorVz.append(Vz)
    for n in V:
    	if(h(Vz) == h(n)):
    		melhorVz.append(n)
    global Verificar
    Verificar.append(h(Vz))           
    pos = random.randint(0,len(melhorVz)-1)
    #print('Saida : ',Vz)
    return melhorVz[pos]

#Funçao HillClimbig
def HillC(R,stdIni):
	act = stdIni
	Cont = 0
	while True:
		V = EstProx(R, act)
		if not V:
		    break	
		Vz = FindVizn(V, stdIni)
		if h(Vz) < h(act):
		  break
		Cont += 1 
		act = Vz
	print("Valores de mudança : ",Cont)
	return act

eixos = [z for z in range(R)]
Estd_I  = pd.DataFrame(index=(eixos),columns=(eixos))
Estd_F = pd.DataFrame(index=(eixos),columns=(eixos))

#gerando estado aleatório
stdIni = list(random.randrange(R) for z in range(R))
for z in range(len(stdIni)):
    Estd_I[eixos[z]][stdIni[z]] = 'Rainha'   
    
#inicia hill climb    
I = time.time()
exec = psutil.Process(os.getpid())
resultado = HillC(R, stdIni)  
M = (exec.memory_info()[0])/1000000 
F = time.time()

#Povoando dataframe com resultado
print_board(resultado)

result = goal_test(resultado) #testa resultado

# Grafico 
indices = [z for z in Verificar]    
colunas = [x for x in range(len(Verificar))]
 
Date = {'Heuristica': indices,
        'Iterações': colunas}

Plot = pd.DataFrame(Date,columns=['Heuristica','Iterações'])
Plot.plot(x='Iterações',y='Heuristica',kind='line')
plt.show()


print('tempo de execução:',(F - I),'seg \n')     
print('memoria:',M,'Mb \n')