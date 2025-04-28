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
        self.territorios = []
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
        país implica colocar n ejércitos en este, por lo que se reduce
        el número de ejércitos disponibles del jugador en n al reclamar.
        Si el jugador ya tiene uno de los países dados, añade n
        ejércitos más a este país"""

        for a in terrs:
            if a not in self.territorios:
                self.invadir(a)
            self.usar(n, a)

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

    def recuperar(self, n: int, pais):
        """Función que añade n ejércitos a la reserva del jugador,
        retirando ejércitos de un país entregado en el argumento"""

        self.ejercitos += n
        pais.retirar(n)

    def usar(self, n: int, pais):
        """Función que retira n ejércitos de la reserva del jugador y
        los coloca en un objeto Pais"""

        self.ejercitos -= n
        pais.reforzar(n)

    def conquistar(self):
        """Función que define el atributo de conquistador en True. Se
        usa para chequear el estado de la fase de Llamado"""

        self.conquistador = True

    def desconquistar(self):
        """Función que define el atributo de conquistador en False"""

        self.conquistador = False

    def invadir(self, pais):
        """Función a la que se le entrega un objeto Pais. El jugador lo
        reclama, añadiéndolo a su lista de territorios. También cambia
        el atributo jugador del país"""

        self.territorios.append(pais)
        self.conquistar()
        pais.conquistado(self)

    def perder(self, pais):
        """Función que elimina un país de los territorios del jugador"""

        self.territorios.remove(pais)

    def futuro(self, pais):
        """Función que define si un jugador puede recibir tropas extra
        si conquista un país en el siguiente turno. Coloca un objeto
        Pais al atributo por_conquistar"""

        self.por_conquistar = pais

    def canjear(self, descarte):
        """Función que hace que el jugador realice un canje. Sube el
        atributo de canje en uno. Se le entrega un objeto Mazo, es el
        mazo al cual envía las cartas que canjea"""

        propias = self.cartas.copiar()
        propiasSimbolos = [i.simbolo for i in propias]
        simbolosList = ["galeón", "cañón", "globo"]
        terrs = self.territorios
        canjeo = False

        for a in simbolosList:
            descartadas = [i for i in propias if i.simbolo == a]
            if propiasSimbolos.count(a) >= 3:
                descartadas[:3]
                canjeo = True
                break
            elif propiasSimbolos.count(a) + propiasSimbolos.count("comodín") >= 3:
                descartadas = descartadas + [
                    i for i in propias if i.simbolo == "comodín"
                ]
                canjeo = True
                break

        if canjeo:
            self.canje += 1
            self.soltar(Mazo(descartadas), descarte)
            if self.canje == 1:
                self.reclamos(4, terrs)
            elif self.canje == 2:
                self.reclamos(7, terrs)
            elif self.canje == 3:
                self.reclamos(10, terrs)
            else:
                self.reclamos(10 + 5 * (self.canje - 3), terrs)

    def atacar(self, pais1, pais2):
        """Función que hace que el jugador realice un ataque. Elige un
        objeto Pais propio y el objeto Pais al cual va a atacar. El
        ataque solo es posible si ambos países cumplen las condiciones
        determinadas por las reglas"""

        pais1.atacar(pais2)

    def __repr__(self):
        return self.nombre

    def __str__(self):
        return self.nombre

    def __eq__(self, jug):
        if isinstance(jug, Jugador):
            return self.nombre == jug.nombre
        return False
