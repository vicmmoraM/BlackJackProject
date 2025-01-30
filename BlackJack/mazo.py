class Carta:
    def __init__(self, valor, palo):
        self.valor = valor
        self.palo = palo
    
    def __str__(self):
        return f"{self.valor} de {self.palo}"
    
    def obtener_valor(self):
        if self.valor in ['J', 'Q', 'K']:
            return 10
        elif self.valor == 'A':
            return 11
        else:
            return int(self.valor)

class Mazo:
    def __init__(self):
        valores = ['2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K', 'A']
        palos = ['Corazones', 'Diamantes', 'Tréboles', 'Picas']
        self.cartas = [Carta(valor, palo) for valor in valores for palo in palos]
    
    def repartir_carta(self):
        return self.cartas.pop(0) if self.cartas else None

    def eliminar_cartas_detectadas(self, cartas_detectadas):
        self.cartas = [carta for carta in self.cartas if str(carta) not in cartas_detectadas]
