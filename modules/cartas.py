from random import shuffle


class Mazo:
    """Clase que representa el mazo de cartas del juego. Tiene asociada cada
    carta del mazo y es capaz de mezclarlas y cortarlas en mazos más pequeños.
    Se inicializa entregándole una lista o diccionario"""

    def __init__(self, cartas: list):

        self.mazo = cartas.copy()
        self.original = self.mazo.copy()

    def mezclar(self):
        """Función que mezcla el mazo de cartas"""

        shuffle(self.mazo)

    def introducir(self, cartas: list):
        """Función a la que se le entrega una lista de nombres de cartas
        y los introduce al mazo"""

        self.mazo.extend(cartas)

    def repartir(self, **kwargs):
        """Función que puede tomar un número de cartas del tope de este
        mazo entregándole el número n de cartas a tomar o puede tomar
        cartas espefícicas del mazo entregándole una lista con los
        nombres de las cartas. Además, se le entrega un objeto Mazo
        para añadir las cartas tomadas de este mazo al otro"""

        # Usar kwargs como {'n':int,'nombres'=obejeto Mazo,
        # 'mazo'=objeto Mazo}

        repartidas = []

        if "n" in kwargs:
            [repartidas.append(self.mazo.pop(0)) for a in range(kwargs["n"])]
        else:
            cartas = kwargs["nombres"].copiar()
            repartidas.extend(cartas)
            self.quitar(cartas)

        kwargs["mazo"].introducir(repartidas)

    def copiar(self):
        """Función que devuelve una copia de la lista de cartas del mazo.
        Sirve para evitar problemas al modificar listas"""

        return self.mazo.copy()

    def quitar(self, nombres):
        """Función que quita cartas del mazo entregando una lista con los nombres de las cartas"""

        [self.mazo.remove(i) for i in nombres]

        self.original = self.mazo.copy()

    def juntar(self):
        # VOY A ELIMINAR ESTA FUNCIÓN
        """Función que devuelve el mazo a su cantidad original, con las cartas sin mezclar"""

        self.mazo = self.original

    def __repr__(self):
        return str(self.mazo)

    def __str__(self):
        return str(self.mazo)

    def __len__(self):
        return len(self.mazo)

    def __iter__(self):
        for a in self.mazo:
            yield a
