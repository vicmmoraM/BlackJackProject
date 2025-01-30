from carta import Carta

class Nodo:

    def __init__(self,simbolo,carta):
        self.carta = Carta(simbolo,carta)
        self.children = []
    
    def agregar(self, nodo):
        self.children.append(nodo)


