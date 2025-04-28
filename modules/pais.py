import json
import numpy as np
from pathlib import Path


class Pais:
    """Clase que representa los países del juego. Tiene asociadas su
    nombre, el número de ejércitos en él, los objetos Pais limítrofes
    y el objeto Jugador que posee este país. El país también es capaz
    de lanzar dados, algo útil durante la fase de ataque de un jugador"""

    # Añadí un objeto Pais porque es más útil que los combates sean
    # Pais contra Pais, y que estos objetos referencien cuántos
    # ejército tienen y a qué jugador pertenencen, en lugar de que los
    # combates sean jugador contra jugador

    # El conteo de tarjetas se usa para añadir el símbolo que
    # corresponde a cada país

    with open(Path() / "data" / "limites.json", encoding="utf-8") as f:
        limites = json.load(f)

    with open(Path(".") / "data" / "cartas.json", "r", encoding="utf-8") as f:
        tarjetas = json.load(f)

    paises = []

    def __init__(self, nombre: str):

        # PREGUNTAR CÓMO HACER QUE SI PAIS YA EXISTE, QUE AL CREARLO
        # SIMPLEMENTE SE REFIERA AL QUE YA EXISTE

        self.nombre = nombre
        self.jugador = None
        self.ejercitos = 0
        self.dado = []

        # PREGUNTAR POR RECURRENCIA Y COMO AÑADIR LIMÍTROFES SIN ELLA
        Pais.paises.append(self)

        # Hice que los limítrofes ya no sean objetos Pais. Solo
        # strings

        self.limitrofes = [i for i in Pais.limites[self.nombre]]

        for a in Pais.tarjetas.keys():
            if self.nombre in Pais.tarjetas[a]:
                self.simbolo = a

    def lanzar(self, n: int):
        """Función que lanza n dados de seis caras y los asocia al valor
        de dado del país"""

        self.dado = [np.int64(6 * np.random.rand() + 1) for i in range(n)]

        return self.dado

    def reforzar(self, n: int):
        """Función que añade n ejércitos al objeto Pais y los retira
        de la reserva del jugador asociado a este país"""

        self.ejercitos += n

    def retirar(self, n: int):
        """Función que retira n ejércitos del objeto Pais y los devuelve
        a la reserva del jugador que posee este país"""

        self.ejercitos -= n

    def conquistado(self, jugador):
        """Función a la que se le entrega un objeto Jugador y hace que
        el país pertenezca a dicho jugador cambiando el valor jugador
        del país"""

        if self.jugador != None:
            self.jugador.perder(self)

        self.jugador = jugador

    def mover(self, n: int, pais2):
        """Función que mueve n ejércitos de este país a un objeto Pais
        entregado en el argumento"""

        # En esta función no se añade un chequeo de si pais2 es limítrofe
        # porque se supone que solo se usa la función en países adecuados

        self.retirar(n)
        pais2.reforzar(n)

    def en_limite(self, pais):
        """Función que revisa si un objeto Pais es limítrofe a este
        país y devuelve un valor Booleano"""

        return pais in self.limites

    def atacar(self, pais2):
        """Función en la que el país elige otro objeto Pais y lo ataca.
        Las reglas del juego definen que pasa en caso de victorias,
        derrotas o empates"""

        # Va a haber que añadir sistemas que revisen que el ataque sea
        # válido

        na = self.ejercitos - 1
        nd = pais2.ejercitos
        ja = self.jugador
        jd = pais2.jugador

        if na > 3:
            na = 3
        if nd > 3:
            nd = 3

        da = self.lanzar(na)
        dd = pais2.lanzar(nd)

        da.sort(reverse=True)
        dd.sort(reverse=True)

        for m in range(min([len(da), len(dd)])):
            if dd[m] >= da[m]:
                ja.recuperar(1, self)
            else:
                jd.recuperar(1, pais2)
                if pais2.ejercitos == 0:
                    ja.invadir(pais2)
                    if self.ejercitos > 2:
                        self.mover(int(2 * np.random.rand() + 1), pais2)
                    else:
                        self.mover(1, pais2)

    def __repr__(self):
        return self.nombre

    def __str__(self):
        return self.nombre

    # Añadí eq para que dos objetos Pais sean iguales si tienen el
    # mismo nombre
    # Añadí hash para poder comparar sets de países

    def __eq__(self, pais2):
        if isinstance(pais2, Pais):
            return self.nombre == pais2.nombre
        return False

    def __hash__(self):
        return hash(self.nombre)
