from random import shuffle


class Mazo:
    """
    Clase que representa una mazo de cartas y al cual puede tratarse
    parcialmente como una lista donde cada elemento es una carta. Es
    capaz de mezclar las cartas, repartirlas a otros mazos, incorporar
    más cartas a sí mismo o quitarlas.
    """

    def __init__(self, cartas: list):
        self.mazo = cartas.copy()

    def mezclar(self):
        """
        Mezcla las cartas del mazo.
        """
        shuffle(self.mazo)

    def introducir(self, cartas: list):
        """
        Integra más cartas, elementos de una lista 'cartas', al mazo.
        cartas: list
            Lista con las cartas a incorporar.
        """
        self.mazo.extend(cartas)

    def repartir(self, **kwargs):
        """
        Reparte 'n' cartas del tope del mazo a otro objeto Mazo
        'recipiente' o reparte cartas específicas 'cartas' de este
        mazo al otro.
        n: int
            Número de cartas a sacar del tope de este mazo para
            repartirlas. El tope del mazo se considera el inicio de su
            lista de cartas.
        cartas: Mazo
            Cartas a ser repartidas al mazo recipiente.
        recipiente: Mazo
            Mazo que recibe las cartas repartidas por este mazo.
        """
        repartidas = []

        # Se roban n cartas del tope del mazo
        if "n" in kwargs:
            [repartidas.append(self.mazo.pop(0)) for a in range(kwargs["n"])]

        # Se roban cartas específicas
        else:
            cartas = kwargs["cartas"].copiar()
            repartidas.extend(cartas)
            self.quitar(cartas)

        # Se añaden las cartas robadas al mazo recipiente
        kwargs["recipiente"].introducir(repartidas)

    def copiar(self):
        """
        Devuelve una copia de la lista de cartas del mazo.
        """
        return self.mazo.copy()

    def quitar(self, cartas: list):
        """
        Remueve ciertas cartas, elementos de la lista 'cartas', del
        mazo.
        cartas: list
            Lista cuyos elementos coinciden con los elementos de la
            lista de cartas del mazo.
        """
        [self.mazo.remove(i) for i in cartas]

    def __repr__(self):
        return str(self.mazo)

    def __str__(self):
        return str(self.mazo)

    def __len__(self):
        return len(self.mazo)

    def __iter__(self):
        for a in self.mazo:
            yield a

    def __getitem__(self, n: int):
        return self.mazo[n]
