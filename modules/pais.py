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

    with open(Path() / "data" / "limites.json", encoding="utf-8") as f:
        limitrofes = json.load(f)

    paises = []

    def __init__(self, nombre: str):
        self.nombre = nombre
        self.ejercitos = 0
        self.jugador = None
        self.dado = []
        if self not in Pais.paises:
            Pais.paises.append(self)
            self.limitrofes = [Pais(i) for i in Pais.limitrofes[self.nombre]]

    def lanzar(self, n: int):
        """Función que lanza n dados de seis caras y los asocia al valor
        de dado del país"""

        self.dado = [np.int64(6 * np.random.rand() + 1) for i in range(n)]

        return self.dado

    def reforzar(self, n: int):
        """Función que añade n ejércitos al objeto Pais y los retira
        de la reserva del jugador asociado a este país"""

        self.ejercitos += n
        self.jugador.usar(n)

    def retirar(self, n: int):
        """Función que retira n ejércitos del objeto Pais y los devuelve
        a la reserva del jugador que posee este país"""

        self.ejercitos -= n
        self.jugador.recuperar(n)

    def conquistar(self, jugador):
        """Función a la que se le entrega un objeto Jugador y hace que
        el país pertenezca a dicho jugador cambiando el valor jugador
        del país"""

        self.jugador = jugador

    def mover(self, pais2, n: int):
        """Función que mueve n ejércitos de este país a un objeto Pais
        entregado en el argumento"""

        self.ejercitos -= n
        pais2.ejercitos += n

    def atacar(self, pais2):
        """Función en la que el país elige otro objeto Pais y lo ataca"""

        # Va a haber que añadir sistemas que revisen que el ataque sea
        # válido

        na = self.ejercitos - 1
        nd = pais2.ejercitos

        if na > 3:
            na = 3
        if nd > 3:
            nd = 3
        
        da=self.lanzar(na)
        dd=pais2.lanzar(nd)

        da.sort(reverse=True)
        dd.sort(reverse=True)

        for m in range(min([len(da),len(dd)])):
            if dd[m] >= da[m]:
                self.retirar(1)
            else:
                pais2.retirar(1)
                if pais2.ejercitos == 0:
                    pais2.conquistar(self.jugador)
                    self.mover(pais2, int(2 * np.random.rand() + 1))

    def __repr__(self):
        return self.nombre

    def __str__(self):
        return self.nombre

    # Añadí eq para que dos objetos Pais sean iguales si tienen el
    # mismo nombre

    def __eq__(self, pais2):
        return self.nombre == pais2.nombre
