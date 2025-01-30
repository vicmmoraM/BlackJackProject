class Jugador:
    def __init__(self, nombre):
        self.nombre = nombre
        self.mano = []

    def tomar_carta(self, mazo):
        carta = mazo.repartir_carta()
        if carta:
            self.mano.append(carta)
    
    def calcular_puntaje(self):
        total = sum(carta.obtener_valor() for carta in self.mano)
        ases = sum(1 for carta in self.mano if carta.valor == 'A')
        while total > 21 and ases > 0:
            total -= 10  # Convertimos un As de 11 a 1
            ases -= 1
        return total

    def mostrar_mano(self):
        return ', '.join(str(carta) for carta in self.mano)