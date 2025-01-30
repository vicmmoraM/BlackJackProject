def valor_blackjack(carta):
    """Convierte una carta en su valor de Blackjack."""
    if carta in ["J", "Q", "K"]:
        return 10
    elif carta == "A":
        return 11
    else:
        return int(carta)

def calcular_puntaje(cartas):
    """
    Calcula el puntaje total en Blackjack.
    Ajusta los As (A) si el total supera 21.
    """
    total = 0
    ases = 0

    for carta in cartas:
        valor = valor_blackjack(carta)
        total += valor
        if carta == "A":
            ases += 1

    while total > 21 and ases > 0:
        total -= 10
        ases -= 1

    return total