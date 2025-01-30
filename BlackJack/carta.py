class Carta:

    cartas = {"As":10,"Dos":2,"Tres":3,"Cuatro":4,"Cinco":5,"Seis":6,"Siete":7,"Ocho":8,"Nueve":9,"Diez":10,"J":10,"Q":10,"K":10}
    simbolos = ["Corazon","Pica","Trebol","Diamante"]

    def __init__(self,simbolo,valor):
        self.simbolo = simbolo
        self.valor = valor
