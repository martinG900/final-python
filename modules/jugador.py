from modules.cartas import Mazo
import numpy as np


class Jugador:
    """Clase que representa a un jugador. Tiene asociada el nombre del jugador,
    las cartas que el jugador posee, sus ejércitos y es capaz de realizar tiros de dados.
    La variable jugadores guarda a todos los jugadores creados"""

    jugadores = []

    def __init__(self, nombre):
        self.nombre = nombre
        self.cartas = Mazo([])
        self.dado = 0
        self.ejercitos = 100
        self.territorios = {}
        Jugador.jugadores.append(self)

    def robar(self, n: int, mazo2):
        """Función que roba n cartas de un objeto Mazo y los añade a
        las cartas del jugador"""

        mazo2.repartir(n=n, mazo=self.cartas)

    def soltar(self, cartas: list, mazo):
        """Función que suelta cartas, eliminándolas de la mano del jugador. Las cartas se eligen
        poniendo sus nombres en el argumento como una lista. Las cartas
        se añaden al objeto Mazo entregado en el argumento"""

        self.cartas.repartir(nombres=cartas, mazo=mazo)

    def tirar(self):
        """Función que genera un número entero entre 1 y 6 y lo asocia al valor dado del jugador.
        Devuleve el valor generado"""

        self.dado = np.int64(6 * np.random.rand() + 1)
        return self.dado

    def reclamar(self, n: int, terrs: list):
        """Función a la que se le entrega una lista de territorios y los añade al diccionario de territorios
        del jugador. Reclamar un territorio implica colocar n ejércitos en este, por lo que se reduce el número
        de ejércitos disponibles del jugador en n al reclamar. Si el jugador ya tiene uno de los territorios dados,
        añade n ejércitos más a este territorio"""

        for a in terrs:
            if a in self.territorios.keys():
                self.territorios[a] += n
            else:
                self.territorios[a] = n
            self.ejercitos -= n

    def reclamos(self, m: int, terrs: list):
        """Función que realiza el método reclamar un número m veces,
        en cada iteración reclamando un territorio elegido eleatoriamente
        entre los territorios proveídos como una lista"""

        [
            self.reclamar(
                1,
                [terrs[int(np.random.rand() * len(terrs))]],
            )
            for a in range(m)
        ]

    def __repr__(self):
        return self.nombre

    def __str__(self):
        return self.nombre
