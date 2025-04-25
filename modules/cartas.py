from random import shuffle

class Mazo:
    '''Clase que representa el mazo de cartas del juego. Tiene asociada cada
    carta del mazo y es capaz de mezclarlas y cortarlas en mazos más pequeños.
    Se inicializa entregándole una lista o diccionario'''

    def __init__(self,cartas):

        if isinstance(cartas,dict):
            self.cartas=cartas
            self.mazo=[]
            for a in self.cartas.values():
                self.mazo.extend(a)
        else:
            self.mazo=cartas
        
        self.original=self.mazo.copy()
    
    def mezclar(self):
        '''Función que mezcla el mazo de cartas'''

        shuffle(self.mazo)
    
    def repartir(self,n):
        '''Función que quita una cantidad n de cartas del tope del mazo y entrega esas cartas como
        otro objeto Mazo'''

        repartidas=[]

        for a in range(n):
            repartidas.append(self.mazo[0])
            self.mazo.pop(0)
        
        return Mazo(repartidas)
    
    def quitar(self,*args):
        '''Función que quita cartas del mazo entregando una lista con los nombres de las cartas'''

        [self.mazo.remove(i) for i in args[0]]

        self.original=self.mazo.copy()
    
    def juntar(self):
        '''Función que devuelve el mazo a su cantidad original, con las cartas sin mezclar'''

        self.mazo=self.original
    
    def intr(self,mazo2):
        #¡PROBABLEMENTE ELIMINE ESTE METODO!
        '''Función que toma un objeto Mazo y añade sus cartas a este objeto Mazo'''

        self.mazo.extend(mazo2.mazo)
    
    def __repr__(self):
        return str(self.mazo)
    
    def __str__(self):
        return str(self.mazo)
    
    def __len__(self):
        return len(self.mazo)