class NodoDecision:
    def __init__(self, condicion, si, no):
        """
        Nodo de decisión del árbol.

        :param condicion: Función que evalúa si tomar el camino 'si' o 'no'.
        :param si: Rama del árbol si la condición es verdadera.
        :param no: Rama del árbol si la condición es falsa.
        """
        self.condicion = condicion
        self.si = si
        self.no = no

    def evaluar(self, puntaje_dealer, puntaje_jugador):
        """Evalúa el árbol de decisión y retorna 'tomar carta' o 'plantarse'."""
        if self.condicion(puntaje_dealer, puntaje_jugador):
            if isinstance(self.si, NodoDecision):
                return self.si.evaluar(puntaje_dealer, puntaje_jugador)
            return self.si  # Retorna la acción final
        else:
            if isinstance(self.no, NodoDecision):
                return self.no.evaluar(puntaje_dealer, puntaje_jugador)
            return self.no  # Retorna la acción final

# 📌 Acciones finales
nodo_plantarse = "plantarse"
nodo_tomar_carta = "tomar carta"

# 📍 Si el dealer tiene 17 o más, se planta
nodo_dealer_17 = NodoDecision(
    condicion=lambda dealer, jugador: dealer >= 17,
    si=nodo_plantarse,
    no=None  # Se llenará con la siguiente decisión
)

# 📍 Si el jugador ya se pasó de 21, el dealer se planta automáticamente
nodo_jugador_se_paso = NodoDecision(
    condicion=lambda dealer, jugador: jugador > 21,
    si=nodo_plantarse,
    no=nodo_dealer_17  # Si el jugador no se pasó, seguimos evaluando
)

# 📍 Si el dealer tiene menos puntos que el jugador, debe tomar carta
nodo_comparar_puntajes = NodoDecision(
    condicion=lambda dealer, jugador: dealer < jugador,
    si=nodo_tomar_carta,
    no=nodo_plantarse
)

# 📍 Conectar la estructura del árbol
nodo_dealer_17.no = nodo_comparar_puntajes 

# 📌 Clase de IA del Dealer
class DealerAI:
    def __init__(self):
        self.arbol_decision = nodo_jugador_se_paso

    def decidir_accion(self, puntaje_dealer, puntaje_jugador):
        """Usa el árbol de decisión para determinar si el dealer debe tomar carta o plantarse."""
        return self.arbol_decision.evaluar(puntaje_dealer, puntaje_jugador)
