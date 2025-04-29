import json
import random as rn
from pathlib import Path


class Pais:
    """
    Clase que representa a los países del juego. Contiene cuántos
    ejércitos lo conforman, a qué jugador pertenece y qué países son
    limíitrofes al mismo. Es capaz de realizar ataques y mover tropas.
    """

    with open(Path() / "data" / "limites.json", encoding="utf-8") as f:
        limites = json.load(f)

    with open(Path(".") / "data" / "cartas.json", "r", encoding="utf-8") as f:
        tarjetas = json.load(f)

    def __init__(self, nombre: str):

        self.nombre = nombre
        self.jugador = None
        self.ejercitos = 0
        self.dado = []
        self.limitrofes = [i for i in Pais.limites[self.nombre]]

        for simbolo in Pais.tarjetas.keys():
            if self.nombre in Pais.tarjetas[simbolo]:
                self.simbolo = simbolo

    def lanzar_dados(self, n: int):
        """
        Lanza 'n' dados y guarda todos los resultados en una lista.
        n: int
            Número de dados a ser lanzados.
        """

        self.dado = [rn.randint(1, 6) for i in range(n)]

        return self.dado

    def reforzar(self, n: int):
        """
        Añade 'n' ejércitos a las tropas en el país.
        n: int
            Número de tropas a añadir.
        """

        self.ejercitos += n

    def retirar(self, n: int):
        """
        Sustrae 'n' ejércitos de las tropas en el país.
        n: int
            Número de tropas a ser sustraídas.
        """

        self.ejercitos -= n

    def conquistado(self, conquistador):
        """
        Conquista el país, sacándolo de entre los territorios del previo
        dueño y añadiéndolo a la lista del nuevo jugador 'conquistador'.
        conquistador: Jugador
            Jugador que conquistó el país. Se adhiere al atributo
            'jugador' del país y lo añade a su lista de territorios.
        """

        if self.jugador != None:
            self.jugador.perder_pais(self)

        conquistador.conquistar()
        conquistador.invadir(self)
        self.jugador = conquistador

    def mover(self, n: int, pais_objetivo):
        """
        Refuerza el país 'pais_objetivo' entregándole 'n' tropas propias.
        n: int
            Número de tropas a mover.
        pais_objetivo: Pais
            País que recibe las tropas.
        """

        self.retirar(n)
        pais_objetivo.reforzar(n)

    def en_limite(self, pais):
        """
        Revisa si un 'pais' es limítrofe a este y devuelve un valor
        Booleano.
        pais: Pais
            País que puede o no ser limítrofe.
        """

        return pais in self.limitrofes

    def atacar(self, defensor):
        """
        Ataca al país 'defensor'.
        defensor: Pais
            País a ser atacado.
        """

        tropas_atacantes = self.ejercitos - 1
        tropas_defensoras = defensor.ejercitos
        jugador_atacante = self.jugador
        jugador_defensor = defensor.jugador

        if tropas_atacantes > 3:
            tropas_atacantes = 3
        if tropas_defensoras > 3:
            tropas_defensoras = 3

        dados_atacante = self.lanzar_dados(tropas_atacantes)
        dados_defensor = defensor.lanzar_dados(tropas_defensoras)

        dados_atacante.sort(reverse=True)
        dados_defensor.sort(reverse=True)

        for dado in range(min([len(dados_atacante), len(dados_defensor)])):
            if dados_defensor[dado] >= dados_atacante[dado]:
                jugador_atacante.retirar_ejercitos(1, self)
            else:
                jugador_defensor.retirar_ejercitos(1, defensor)
                if defensor.ejercitos == 0:
                    defensor.conquistado(jugador_atacante)
                    if (
                        jugador_atacante.por_conquistar != None
                        and jugador_atacante.por_conquistar == defensor
                    ):
                        jugador_atacante.usar_reservas(2, defensor)
                    if self.ejercitos > 2:
                        self.mover(rn.randint(1, 2), defensor)
                    else:
                        self.mover(1, defensor)

    def __repr__(self):
        return self.nombre

    def __str__(self):
        return self.nombre

    def __eq__(self, pais2):
        if isinstance(pais2, Pais):
            return self.nombre == pais2.nombre
        return False

    def __hash__(self):
        return hash(self.nombre)
