from arbol import Arbol
from carta import Carta
import copy  # Importamos copy para clonar estructuras

class Crupier:
    
    def __init__(self, juego):
        self.juego = juego  
        carta_inicial = self.juego.repartir_carta()
        self.arbol = Arbol(carta_inicial) 


    def pedir_carta(self):
        carta = self.juego.repartir_carta()
        if carta:
            nuevo_nodo = Nodo(carta)
            self.arbol.agregar_hijo(self.arbol.raiz, nuevo_nodo)

    def puntaje(self):
        return self.arbol.puntaje_total(self.arbol.raiz)

    def minimax(self, nodo, profundidad, es_max, puntaje_jugador, baraja_simulada):
        """Algoritmo Minimax para decidir si el Crupier debe pedir carta o quedarse."""
        puntaje_actual = self.arbol.puntaje_total(nodo)  # Calculamos desde la raíz usando Arbol

        # Condiciones base
        if puntaje_actual > 21:
            return -100  # Peor caso, se pasa y pierde
        if puntaje_actual == 21:
            return 100  # Mejor caso, Blackjack
        if profundidad == 0:
            return puntaje_actual  # Evalúa el estado actual

        if es_max:  # Turno del Crupier
            max_eval = -float('inf')
            for _ in range(5):  # Prueba hasta 5 cartas aleatorias
                if not baraja_simulada:  # Si no quedan cartas simuladas, termina la simulación
                    break
                carta = baraja_simulada.pop()  # Tomamos una carta de la copia de la baraja
                nuevo_nodo = Nodo(carta)  # Crea un nodo hijo con la nueva carta
                self.arbol.agregar_hijo(nodo, nuevo_nodo)  # Se agrega como hijo en el árbol
                eval_nodo = self.minimax(nuevo_nodo, profundidad - 1, False, puntaje_jugador, baraja_simulada[:])  # Clonamos la baraja simulada en cada iteración
                max_eval = max(max_eval, eval_nodo)
            return max_eval
        else:  # Evaluación del jugador
            if puntaje_actual >= puntaje_jugador:
                return puntaje_actual  # Se queda si ya gana
            else:
                min_eval = float('inf')
                for _ in range(5):
                    if not baraja_simulada:
                        break
                    carta = baraja_simulada.pop()
                    nuevo_nodo = Nodo(carta)
                    self.arbol.agregar_hijo(nodo, nuevo_nodo)
                    eval_nodo = self.minimax(nuevo_nodo, profundidad - 1, True, puntaje_jugador, baraja_simulada[:])
                    min_eval = min(min_eval, eval_nodo)
                return min_eval

    def jugar_turno(self, puntaje_jugador):
        while self.puntaje() < 18:  
            self.pedir_carta()

        if self.puntaje() >= 21:
            return self.puntaje()
        
        # Clonamos la baraja antes de hacer el análisis con Minimax
        baraja_clonada = self.juego.baraja.clonar_baraja()

        decision = self.minimax(self.arbol.raiz, profundidad=3, es_max=True, puntaje_jugador=puntaje_jugador, baraja_simulada=baraja_clonada)

        if decision > self.puntaje():
            self.pedir_carta()

        return self.puntaje()


