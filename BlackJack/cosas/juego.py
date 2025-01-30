from baraja import Baraja
from detectar_cartas import detectar_cartas

class Juego:
    YOLO_TO_BARAJA = {
        "2C": "Dos de Trebol", "2D": "Dos de Diamante", "2H": "Dos de Corazon", "2S": "Dos de Pica",
        "3C": "Tres de Trebol", "3D": "Tres de Diamante", "3H": "Tres de Corazon", "3S": "Tres de Pica",
        "4C": "Cuatro de Trebol", "4D": "Cuatro de Diamante", "4H": "Cuatro de Corazon", "4S": "Cuatro de Pica",
        "5C": "Cinco de Trebol", "5D": "Cinco de Diamante", "5H": "Cinco de Corazon", "5S": "Cinco de Pica",
        "6C": "Seis de Trebol", "6D": "Seis de Diamante", "6H": "Seis de Corazon", "6S": "Seis de Pica",
        "7C": "Siete de Trebol", "7D": "Siete de Diamante", "7H": "Siete de Corazon", "7S": "Siete de Pica",
        "8C": "Ocho de Trebol", "8D": "Ocho de Diamante", "8H": "Ocho de Corazon", "8S": "Ocho de Pica",
        "9C": "Nueve de Trebol", "9D": "Nueve de Diamante", "9H": "Nueve de Corazon", "9S": "Nueve de Pica",
        "10C": "Diez de Trebol", "10D": "Diez de Diamante", "10H": "Diez de Corazon", "10S": "Diez de Pica",
        "JC": "J de Trebol", "JD": "J de Diamante", "JH": "J de Corazon", "JS": "J de Pica",
        "QC": "Q de Trebol", "QD": "Q de Diamante", "QH": "Q de Corazon", "QS": "Q de Pica",
        "KC": "K de Trebol", "KD": "K de Diamante", "KH": "K de Corazon", "KS": "K de Pica",
        "AC": "As de Trebol", "AD": "As de Diamante", "AH": "As de Corazon", "AS": "As de Pica"
    }

    def __init__(self):
        """ Inicializa el juego con una baraja fija. """
        self.baraja = Baraja()
        self.jugador_mano = []
        self.crupier_mano = []

        # 📌 Crupier toma sus cartas primero
        self.crupier_mano.append(self.baraja.tomar_carta())
        self.crupier_mano.append(self.baraja.tomar_carta())

        print(f"🎭 Mano del Crupier: {self.crupier_mano}")

    def capturar_cartas_jugador(self, frame):
        """ Usa OpenCV para capturar las cartas del jugador. """
        print("📸 Capturando cartas del jugador...")

        cartas_detectadas = detectar_cartas(frame)

        if not cartas_detectadas or "NO DETECTADO" in cartas_detectadas:
            print("❌ No se detectaron cartas correctamente. Verifica la imagen.")
            return []

        # 📌 Convertir nombres de YOLO al formato de la Baraja
        cartas_convertidas = [self.YOLO_TO_BARAJA.get(carta, carta) for carta in cartas_detectadas]

        print(f"🔄 Cartas convertidas a formato de Baraja: {cartas_convertidas}")

        # 📌 Eliminar cartas de la baraja y agregarlas al jugador
        cartas_finales = []
        for carta in cartas_convertidas:
            if carta in self.baraja.cartas_disponibles():
                self.baraja.remover_carta(carta)
                cartas_finales.append(carta)

        self.jugador_mano = cartas_finales
        print(f"🃏 Mano final del Jugador: {self.jugador_mano}")
        return self.jugador_mano

    def calcular_puntos(self, mano):
        """ Calcula el total de puntos de una mano. """
        valores = {
            "Dos": 2, "Tres": 3, "Cuatro": 4, "Cinco": 5, "Seis": 6, "Siete": 7, "Ocho": 8, "Nueve": 9,
            "Diez": 10, "J": 10, "Q": 10, "K": 10, "As": 11
        }
        total = 0
        ases = 0

        for carta in mano:
            partes = carta.split()
            if len(partes) > 1:
                valor = partes[0]
                total += valores.get(valor, 0)
                if valor == "As":
                    ases += 1

        while total > 21 and ases:
            total -= 10
            ases -= 1

        return total

    def iniciar_ronda(self, frame):
        """ Realiza una ronda de Blackjack. """
        puntos_jugador = self.calcular_puntos(self.jugador_mano)
        puntos_crupier = self.calcular_puntos(self.crupier_mano)

        print(f"🃏 Mano del Jugador: {self.jugador_mano} (Total: {puntos_jugador})")
        print(f"🎭 Mano del Crupier: {self.crupier_mano} (Total: {puntos_crupier})")

        if puntos_jugador > 21:
            return "💀 El jugador ha perdido por pasarse de 21."

        while puntos_crupier < 17:
            nueva_carta = self.baraja.tomar_carta()
            self.crupier_mano.append(nueva_carta)
            puntos_crupier = self.calcular_puntos(self.crupier_mano)
            print(f"🎭 El Crupier toma otra carta: {nueva_carta} (Total: {puntos_crupier})")

        if puntos_crupier > 21 or puntos_jugador > puntos_crupier:
            return "🎉 ¡Ganaste contra el Dealer!"
        elif puntos_jugador == puntos_crupier:
            return "🤝 Empate, nadie gana."
        else:
            return "🏆 Gana el Dealer."

