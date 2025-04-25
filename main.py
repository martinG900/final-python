import json
from pathlib import Path
from random import shuffle
from modules.cartas import Mazo
from modules.jugador import Jugador

#Funciones

def tiros(m:int,*args):
    '''Función a la que se le pasa una lista de objetos Jugador. Hace que todos
    estos jugadores lancen los dados y compara sus resultados. Indica quienes
    son los m jugadores con los mayores resultados. La función tiene en cuenta los empates'''

    args=args[0]

    ganadores=[]

    while True:

        for a in args:
            a.tirar()

        jugs=list(args)
        
        jugs.sort(key=lambda x:x.dado,reverse=True)
        valores=[i.dado for i in jugs]

        for a in range(jugs[0].dado,0,-1):
            if valores.count(a)==m-len(ganadores):
                ganadores.extend(jugs[:valores.count(a)])
                return ganadores
            elif valores.count(a)>m-len(ganadores):
                args=jugs[:valores.count(a)].copy()
                break
            else:
                ganadores.extend(jugs[:valores.count(a)])
                jugs=jugs[valores.count(a):]

##INICIALIZACIÓN

# Abrir las cartas. Se considera al 0 de la lista como el tope del mazo

with open(Path('.')/'data'/'cartas.json','r',encoding='utf-8') as f:
    cartas=json.load(f)

mazo=Mazo(cartas)
mazo.mezclar()

#Crear jugadores. Los jugadores tienen sus propios dados

numJ=4

J=[Jugador(f'José {i+1}') for i in range(numJ)]

#Repartir paí­ses por jugador. Recordar que pueden sobrar dos cartas si jugadores=3,4,6

if numJ in [2,5]:
    mano=len(mazo)//numJ
    [i.robar(mano,mazo) for i in J]
else:
    mano=(len(mazo)-2)//numJ
    [i.robar(mano,mazo) for i in J]
    
    #Introducir el tiro de dados y las dos cartas extra

    [j.robar(1,mazo,True) for j in tiros(2,J)]

#Cada jugador añade 1 ejército a sus países

[j.reclamar(1,j.cartas.mazo) for j in J]

#Quitar las cartas de las manos de los jugadores y resetear el mazo de cartas

[j.soltar(j.territorios.keys()) for j in J]

mazo.juntar()

#Cada jugador añade 5 ejércitos repartidos entre sus paí­ses

for a in J:
    terrs=list(a.territorios.keys()).copy()
    shuffle(terrs)
    a.reclamar(1,terrs[0:5])

#Cada jugador añade 3 ejércitos repartidos entre sus paí­ses

for a in J:
    terrs=list(a.territorios.keys()).copy()
    shuffle(terrs)
    a.reclamar(1,terrs[0:3])


