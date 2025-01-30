class Carta:
    valores = {"As": 11, "Dos": 2, "Tres": 3, "Cuatro": 4, "Cinco": 5, 
               "Seis": 6, "Siete": 7, "Ocho": 8, "Nueve": 9, "Diez": 10, 
               "J": 10, "Q": 10, "K": 10}
    
    simbolos = ["Corazon", "Pica", "Trebol", "Diamante"]

    def __init__(self, simbolo, valor):
        """ Inicializa una carta con su símbolo y valor """
        if simbolo not in self.simbolos:
            raise ValueError(f"❌ Error: '{simbolo}' no es un símbolo válido. Usa {self.simbolos}")
        
        if valor not in self.valores:
            raise ValueError(f"❌ Error: '{valor}' no es un valor válido. Usa {list(self.valores.keys())}")

        self.simbolo = simbolo
        self.valor = self.valores[valor]  # 📌 Convertir el nombre en su valor numérico

    def obtener_valor(self):
        """ Devuelve el valor numérico de la carta """
        return self.valor

    def __str__(self):
        """ Devuelve la carta en formato 'Valor de Símbolo' """
        return f"{self.valor} de {self.simbolo}"
