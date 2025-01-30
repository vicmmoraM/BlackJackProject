from nodo import Nodo 

class Arbol:

    def __init__(self,carta):
        self.raiz = Nodo(carta)

    def agregar_hijo(self,nodo_padre, nodo_hijo):
        nodo_padre.agregar(nodo_hijo)

    def puntaje_total(self, nodo):
        total = self.raiz.carta.valor  
        ases = 1 if self.raiz.carta.simbolo == "As" else 0

        for hijo in nodo.children:
            total += hijo.carta.valor
            if hijo.carta.simbolo == "As":
                ases += 1

        # Ajustamos el valor de los Ases si es necesario
        while total > 21 and ases > 0:
            total -= 10
            ases -= 1

        return total
