from carta import Carta
import random as rd
import copy

class Baraja:

    def __init__(self):
        self.baraja = self.generar_baraja()
        rd.shuffle(self.baraja)

    def generar_baraja(self):
        valores = list(Carta.cartas.keys())
        simbolos = Carta.simbolos
        baraja = []
        for simbolo in simbolos:
            for valor in valores:
                baraja.append(Carta(simbolo,valor))
        return baraja

    def repartir_carta(self):
        if not self.baraja:  
            self.baraja = self.generar_baraja()
            rd.shuffle(self.baraja)
        return self.baraja.pop()
    
    def clonar_baraja(self):
        return copy.deepcopy(self.baraja)