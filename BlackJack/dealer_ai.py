# 📌 Clase de IA del Dealer
from mazo import Mazo, Carta
from jugador import Jugador
import copy

class DealerAI:
    def __init__(self, mazo):
        self.mazo = mazo
        self.indice_carta = 0  # 📌 Mantiene el seguimiento de la carta a tomar en orden
    
    def minimax(self, dealer_mano, jugador_puntaje, profundidad, es_turno_dealer, mazo_simulado):
        dealer_puntaje = self.calcular_puntaje(dealer_mano)
        
        # 📌 Condiciones de fin del juego
        if dealer_puntaje > 21:
            return -1  # Dealer pierde automáticamente
        if dealer_puntaje >= 17:  # Dealer se planta a 17 o más
            if dealer_puntaje > jugador_puntaje or jugador_puntaje > 21:
                return 1  # Dealer gana
            elif dealer_puntaje == jugador_puntaje:
                return 0  # Empate
            else:
                return -1  # Dealer pierde
        
        if profundidad == 0:
            return dealer_puntaje / 21  # Evaluación heurística
        
        if es_turno_dealer:
            mejor_valor = -float('inf')
            for i in range(len(mazo_simulado.cartas)):
                nueva_mano = dealer_mano[:] + [mazo_simulado.cartas[i]]  # 📌 Asegurar que dealer_mano es una lista
                mazo_copia = copy.deepcopy(mazo_simulado)  # 📌 Clonar mazo para evitar alterar el original
                mazo_copia.cartas.pop(i)  # 📌 Simular que la carta ha sido tomada
                valor = self.minimax(nueva_mano, jugador_puntaje, profundidad - 1, False, mazo_copia)
                mejor_valor = max(mejor_valor, valor)
            return mejor_valor
        else:
            peor_valor = float('inf')
            for i in range(len(mazo_simulado.cartas)):
                nueva_mano = dealer_mano[:] + [mazo_simulado.cartas[i]]  # 📌 Asegurar que dealer_mano es una lista
                mazo_copia = copy.deepcopy(mazo_simulado)  # 📌 Clonar mazo para evitar alterar el original
                mazo_copia.cartas.pop(i)  # 📌 Simular que la carta ha sido tomada
                valor = self.minimax(nueva_mano, jugador_puntaje, profundidad - 1, True, mazo_copia)
                peor_valor = min(peor_valor, valor)
            return peor_valor
    
    def calcular_puntaje(self, mano):
        total = sum(carta.obtener_valor() for carta in mano)
        ases = sum(1 for carta in mano if carta.valor == 'A')
        while total > 21 and ases > 0:
            total -= 10  # Ajustar As de 11 a 1
            ases -= 1
        return total
    
    def decidir_accion(self, dealer_mano, jugador_puntaje):
        """Evalúa la mejor acción con Minimax."""
        mazo_simulado = copy.deepcopy(self.mazo)  # 📌 Clonar mazo para la simulación
        if not isinstance(dealer_mano, list):
            dealer_mano = []  # 📌 Asegurar que dealer_mano es una lista vacía si es un número
        if self.indice_carta < len(mazo_simulado.cartas):
            proxima_carta = mazo_simulado.cartas[self.indice_carta]
            tomar_carta_valor = self.minimax(dealer_mano + [proxima_carta], jugador_puntaje, 3, False, mazo_simulado)
        else:
            tomar_carta_valor = -float('inf')
        
        plantarse_valor = self.minimax(dealer_mano, jugador_puntaje, 3, False, mazo_simulado)
        
        if tomar_carta_valor > plantarse_valor:
            self.indice_carta += 1  # 📌 Avanza en el mazo solo si toma la carta
            return "tomar carta"
        else:
            return "plantarse"
