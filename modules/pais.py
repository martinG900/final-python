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
        limitrofes = json.load(f)

    with open(Path(".") / "data" / "cartas.json", "r", encoding="utf-8") as f:
        tarjetas = json.load(f)

    paises = []

    def __init__(self, nombre: str):
        self.nombre = nombre
        self.jugador = None
        self.ejercitos = 0
        self.dado = []
        if self not in Pais.paises:
            Pais.paises.append(self)
            self.limitrofes = [Pais(i) for i in Pais.limitrofes[self.nombre]]

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

    '''def conquistar(self, jugador):
        """Función a la que se le entrega un objeto Jugador y hace que
        el país pertenezca a dicho jugador cambiando el valor jugador
        del país"""

        self.jugador = jugador
        self.jugador.conquistar()'''

    def mover(self, pais2, n: int):
        """Función que mueve n ejércitos de este país a un objeto Pais
        entregado en el argumento"""

        # En esta función no se añade un chequeo de si pais2 es limítrofe
        # porque se supone que solo se usa la función en países adecuados

        self.retirar(n)
        pais2.reforzar(n)

    def atacar(self, pais2):
        """Función en la que el país elige otro objeto Pais y lo ataca.
        Las reglas del juego definen que pasa en caso de victorias,
        derrotas o empates"""

        # Va a haber que añadir sistemas que revisen que el ataque sea
        # válido

        na = self.ejercitos - 1
        nd = pais2.ejercitos
        ja=self.jugador
        jd=pais2.jugador

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
                self.retirar(1)
            else:
                pais2.retirar(1)
                if pais2.ejercitos == 0:
                    pais2.conquistar(self.jugador)
                    if self.ejercitos == 1:
                        self.mover(pais2, 1)
                    else:
                        self.mover(pais2, int(2 * np.random.rand() + 1))

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
