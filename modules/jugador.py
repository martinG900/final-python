from modules.cartas import Mazo
import random as rn


class Jugador:
    """
    Clase que representa a un jugador. Tiene asociados su nombre,
    su color, una mano de cartas, un dado, los ejércitos en su reserva
    y valores asociados a cada fase del juego
    """

    def __init__(self, nombre: str = "José", color: str = "orange"):
        self.nombre = nombre
        self.cartas = Mazo([])
        self.color = color
        self.dado = []
        self.territorios = []
        self.reserva = 100
        self.conquistador = False
        self.por_conquistar = None
        self.canje = 0

    def robar(self, n: int, baraja):
        """
        Roba 'n' cartas de un mazo 'baraja', añadiéndolas a la mano
        del jugador.
        n: int
            Número de cartas a robar.
        baraja: Mazo
            Mazo del cual se roban las cartas.
        """
        baraja.repartir(n=n, mazo=self.cartas)

    def devolver(self, cartas_propias, baraja):
        """
        Elige cartas específicas 'cartas_propias' de la mano y las
        entrega al mazo 'baraja'.
        cartas_propias: Mazo
            Cartas a ser devueltas.
        baraja: Mazo
            Mazo al que se le devuelven las cartas.
        """
        self.cartas.repartir(nombres=cartas_propias, mazo=baraja)

    def lanzar_dados(self, n: int):
        """
        Lanza 'n' dados y guarda los valores en el atributo 'dado'.
        n: int
            Número de dados a lanzar.
        """
        self.dado = [rn.randint(1, 6) for i in range(n)]

    def desplegar(self, n: int, paises_objetivo: list):
        """
        Entrega 'n' ejércitos de la reserva a los países en la lista
        'paises_objetivo'. Si un país de la lista no forma parte de los
        territorios del jugador, lo añade.
        n: int
            Número de ejércitos a colocar en cada país.
        paises_objetivo: list
            Lista de objetos Pais en los que se despliegan los ejércitos.
        """
        for pais in paises_objetivo:
            if pais not in self.territorios:
                pais.conquistado(self)
            self.usar_reservas(n, pais)

    def despliegues(self, m: int, paises_objetivo: list):
        """
        Despliega un ejército a un país elegido aleatoriamente de una
        lista de países 'paises_objetivo'. Repite este proceso 'm'
        veces.
        m: int
            Número de veces a repetir el despliege.
        paises_objetivo: list
            Lista de objetos Pais, posibles receptores de los ejércitos
            a desplegar.
        """
        [self.desplegar(1, [rn.choice(paises_objetivo)]) for i in range(m)]

    def retirar_ejercitos(self, n: int, pais):
        """
        Retira 'n' ejércitos del país 'pais' y los devuelve a la
        reserva.
        n: int
            Número de ejércitos a retirar.
        pais: Pais
            País del cual retirar los ejércitos.
        """
        pais.retirar(n)
        self.reserva += n

    def usar_reservas(self, n: int, pais):
        """
        Saca 'n' ejércitos de la reserva y los añade a las tropas en el
        país 'pais'.
        n: int
            Número de ejércitos a añadir al país.
        pais: Pais
            País al cual añadir los ejércitos.
        """

        if self.reserva - n < 0:
            pais.reforzar(self.reserva)
            self.reserva = 0
        else:
            pais.reforzar(n)
            self.reserva -= n

    def conquistar(self):
        """
        Define como 'True' el atributo 'conquistador' del jugador.
        """

        self.conquistador = True

    def sin_conquistas(self):
        """
        Define como 'False' el el atributo 'conquistador' del jugador.
        """

        self.conquistador = False

    def invadir(self, pais):
        """
        Añade un país 'pais' a los territorios del jugador y
        cambia el atributo 'jugador' de dicho país para reflejar esto.
        pais: Pais
            País a ser añadido.
        """

        self.territorios.append(pais)
        # self.conquistar()
        # pais.conquistado(self)

    def perder_pais(self, pais):
        """
        Elimina el país 'pais' de los territorios del jugador.
        pais: Pais
            País a ser removido.
        """

        self.territorios.remove(pais)

    def pais_objetivo(self, pais):
        """
        Define un país 'pais' a ser conquistado el siguiente turno par
        obtener refuerzos extra.
        pais: Pais
            País a ser conquistado.
        """

        self.por_conquistar = pais

    def canjear(self, descarte):
        """
        Canjea cartas de la mano para usar ejércitos de la reserva y
        desplegarlos en países propios. Tira dichas cartas al mazo
        'descarte'.
        descarte: mazo
            Mazo que recibe las cartas descartadas por el jugador.
        """

        mis_cartas = self.cartas.copiar()
        mis_simbolos = [i.simbolo for i in mis_cartas]
        simbolos = ["galeón", "cañón", "globo"]
        ocurre_canjeo = False

        for simbolo in simbolos:
            cartas_canjeo = [i for i in mis_cartas if i.simbolo == simbolo]
            if mis_simbolos.count(simbolo) >= 3:
                cartas_canjeo[:3]
                ocurre_canjeo = True
                break
            elif mis_simbolos.count(simbolo) + mis_simbolos.count("comodín") >= 3:
                cartas_canjeo = cartas_canjeo + [
                    i for i in mis_cartas if i.simbolo == "comodín"
                ]
                ocurre_canjeo = True
                break

        if ocurre_canjeo:
            self.canje += 1
            self.devolver(Mazo(cartas_canjeo), descarte)
            if self.canje == 1:
                self.despliegues(4, self.territorios)
            elif self.canje == 2:
                self.despliegues(7, self.territorios)
            elif self.canje == 3:
                self.despliegues(10, self.territorios)
            else:
                self.despliegues(10 + 5 * (self.canje - 3), self.territorios)

    def atacar(self, atacante, defensor):
        """
        Realiza un ataque entre el país atacante 'atacante' y el
        defensor 'defensor'.
        atacante: Pais
            País atacante.
        defensor: Pais
            País defensor.
        """

        atacante.atacar(defensor)

    def mis_paises(self):
        """
        Entrega una copia de la lista de países conquistados por el
        jugador.
        """

        return self.territorios.copy()

    def __repr__(self):
        return self.nombre

    def __str__(self):
        return self.nombre

    def __eq__(self, jug):
        if isinstance(jug, Jugador):
            return self.nombre == jug.nombre
        return False

    @classmethod
    def tiros(cls, numero_ganadores: int, participantes: list):
        """
        Hace que los jugadores 'participantes' lancen los dados y los
        compara. Repite el proceso hasta que haya exactamente
        'numero_ganadores' ganadores.
        numero_ganadores: int
            Número de ganadores requerido para terminar la sesión de
            tiros.
        participantes: list
            Lista de objetos Jugador que participarán de la competencia.
        """

        ganadores = []
        jugadores = participantes.copy()

        # Repetir los tiros hasta tener suficientes ganadores
        while True:

            # Jugadores tiran dados

            [i.lanzar_dados(1) for i in jugadores]

            # Los jugadores se ordenan según sus dados en orden descendente

            jugadores.sort(key=lambda x: x.dado[0], reverse=True)
            dados = [i.dado[0] for i in jugadores]

            # Se hace una lista con los números obtenidos entre todos
            # los tiros

            resultados = list({6, 5, 4, 3, 2, 1} & set(dados))
            resultados.sort(reverse=True)

            # Se chequean quienes califican para ganar y se repiten los tiros para
            # los que empataron

            # Se revisan todos los nuúmeros sacados en los tiros y se
            # cuentan cuántos ganaron en orden descendente
            for numero in resultados:
                if dados.count(numero) == numero_ganadores - len(ganadores):
                    # Se obtuvo el número justo de ganadores. Se termina
                    # la función
                    ganadores.extend(jugadores[: dados.count(numero)])
                    return ganadores
                elif dados.count(numero) > numero_ganadores - len(ganadores):
                    # Hay muchos ganadores. Estos vuelven a hacer los
                    # tiros
                    jugadores = jugadores[: dados.count(numero)].copy()
                    break
                else:
                    # Ganan algunos. Los demás vuelven a tirar
                    ganadores.extend(jugadores[: dados.count(numero)])
                    jugadores = jugadores[dados.count(numero) :]
