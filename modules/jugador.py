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
        self.dado = []
        self.ejercitos = 100
        self.conquistador = False
        # Conquistador revisa si se conquistó un país durante la fase
        # de ataque. Sirve para luego pasar a la fase de llamado
        self.por_conquistar = None
        # por_conquistar revisa si hay un país que el jugador debe
        # conquistar en el siguiente turno para recibir dos ejércitos
        # extra
        self.canje = 0
        # canje revisa el número de canjes realizado por el jugador
        Jugador.jugadores.append(self)

    def robar(self, n: int, mazo2):
        """Función que roba n cartas de un objeto Mazo y los añade a
        las cartas del jugador"""

        mazo2.repartir(n=n, mazo=self.cartas)

    def soltar(self, mazo1, mazo2):
        """Función que suelta las cartas de un objeto Mazo, mazo1,
        eliminándolas de la mano del jugador. Las cartas se eligen
        poniendo sus nombres en el argumento como una lista. Las cartas
        se añaden al objeto Mazo entregado en el argumento"""

        self.cartas.repartir(nombres=mazo1, mazo=mazo2)

    def lanzar(self, n: int):
        """Función que hace que el jugador lance n dados de seis caras,
        asociando los valores obtenidos al valor dado del objeto
        Jugador"""

        self.dado = [np.int64(6 * np.random.rand() + 1) for i in range(n)]

    def reclamar(self, terrs: list, n: int):
        """Función a la que se le entrega una lista de objetos Pais y
        los añade a la lista de territorios del jugador. Reclamar un
        pais implica colocar n ejércitos en este, por lo que se reduce
        el número de ejércitos disponibles del jugador en n al reclamar.
        Si el jugador ya tiene uno de los paises dados, añade n
        ejércitos más a este país"""

        for a in terrs:
            if a.jugador == self:
                a.reforzar(n)
            else:
                a.conquistar(self)
                a.reforzar(n)
            self.ejercitos -= n

    def reclamos(self, m: int, terrs: list):
        """Función que realiza el método reclamar un número m veces,
        en cada iteración reclamando un territorio elegido eleatoriamente
        entre los territorios proveídos como una lista de objetos Pais"""

        # Hay que revisar que solo se reclaman países sin ejércitos
        # enemigos en él

        [
            self.reclamar([terrs[int(np.random.rand() * len(terrs))]], 1)
            for a in range(m)
        ]

    def quitar(self, pais, n: int):
        """Funcion que quita n ejércitos de un objeto País del jugador.
        Además si el país se queda sin ejércitos, el jugador pierde
        dicho país"""

        # Hay que revisar que se quite el número adecuado de ejércitos
        # del país para evitar que haya un número negativo de ejércitos

        pais.retirar(n)

        self.ejercitos += n

    def recuperar(self, n: int):
        """Función que añade n ejércitos a los ejércitos del jugador"""

        self.ejercitos += n

    def usar(self, n: int):
        """Función que retira n ejércitos de los ejércitos del jugador"""

        self.ejercitos -= n

    def conquistar(self):
        """Función que define el atributo de conquistador en True. Se
        usa para chequear el estado de la fase de Llamado"""

        self.conquistador = True

    def futuro(self, pais):
        """Función que define si un jugador puede recibir tropas extra
        si conquista un país en el siguiente turno. Coloca un objeto
        Pais al atributo por_conquistar"""

        self.por_conquistar = pais

    def __repr__(self):
        return self.nombre

    def __str__(self):
        return self.nombre

    def __eq__(self, jug):
        if isinstance(jug, Jugador):
            return self.nombre == jug.nombre
        return False
