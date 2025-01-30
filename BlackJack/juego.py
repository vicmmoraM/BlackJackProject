from baraja import Baraja
from crupier import Crupier  

class Juego:

    def __init__(self):
        self.baraja = Baraja()  
        self.crupier = Crupier(self) 

    def repartir_carta(self):
        return self.baraja.repartir_carta()

    def iniciar_ronda(self, puntaje_jugador):
        self.crupier.jugar_turno(puntaje_jugador)
        return self.crupier.puntaje()


