from modules.cartas import Mazo
import numpy as np

class Jugador:
    '''Clase que representa a un jugador. Tiene asociada el nombre del jugador,
    las cartas que el jugador posee, sus ejércitos y es capaz de realizar tiros de dados.
    La variable jugadores guarda a todos los jugadores creados'''

    jugadores=[]

    def __init__(self,nombre):
        self.nombre=nombre
        self.cartas=Mazo([])
        self.dado=0
        self.ejercitos=100
        self.territorios={}
        Jugador.jugadores.append(self)
    
    def robar(self,n:int,mazo,sumar=False):
        '''Función que toma un número n de cartas de un objeto Mazo y lo entrega al jugador.
        Si se configura sumar como True, la función añade las cartas robadas a la mano del
        jugador. De otra forma, el jugador toma una mano nueva'''

        if sumar:
            self.cartas.intr(mazo.repartir(n))
        else:
            self.cartas=mazo.repartir(n)
    
    def soltar(self,*args):
        '''Función que suelta cartas, eliminándolas de la mano del jugador. Las cartas se eligen
        poniendo sus nombres en el argumento como una lista'''

        self.cartas.quitar(args[0])
    
    def tirar(self):
        '''Función que genera un número entero entre 1 y 6 y lo asocia al valor dado del jugador.
        Devuleve el valor generado'''

        self.dado=np.int64(6*np.random.rand()+1)
        return self.dado
    
    def reclamar(self,n:int,*args):
        '''Función a la que se le entrega una lista de territorios y los añade al diccionario de territorios
        del jugador. Reclamar un territorio implica colocar n ejércitos en este, por lo que se reduce el número
        de ejércitos disponibles del jugador en n al reclamar. Si el jugador ya tiene uno de los territorios dados,
        añade n ejércitos más a este territorio'''

        for a in args[0]:
            if a in self.territorios.keys():
                self.territorios[a]+=n
            else:
                self.territorios[a]=n
            self.ejercitos-=n
    
    def __repr__(self):
        return self.nombre

    def __str__(self):
        return self.nombre