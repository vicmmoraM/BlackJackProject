import cv2
import numpy as np
from detectar_cartas import detectar_cartas, card_map
import configuracion as cfg
from mazo import Carta, Mazo
from jugador import Jugador
from dealer_ai import DealerAI
from flask import jsonify

mazo = Mazo()
jugador = Jugador("Jugador")
dealer = Jugador("Dealer")
dealer_ai = DealerAI(mazo)

def iniciar_juego():
    """Reparte 2 cartas al jugador y 2 al dealer al inicio del juego."""
    global mazo, dealer, jugador  
    
    # Repartir cartas iniciales
    jugador.mano = [mazo.repartir_carta(), mazo.repartir_carta()]
    dealer.mano = [mazo.repartir_carta(), mazo.repartir_carta()]
    
    # Eliminar cartas del mazo para evitar duplicados
    mazo.eliminar_cartas_detectadas([str(carta) for carta in jugador.mano + dealer.mano])
    
    print(f"✅ Jugador recibe: {jugador.mostrar_mano()} - Puntos: {jugador.calcular_puntaje()}")
    print(f"✅ Dealer recibe: {dealer.mostrar_mano()} - Puntos: {dealer.calcular_puntaje()}")
    
    return {
        'jugador': {
            'cartas': [str(carta) for carta in jugador.mano],
            'puntos': jugador.calcular_puntaje()
        },
        'dealer': {
            'cartas': [str(carta) for carta in dealer.mano],
            'puntos': dealer.calcular_puntaje()
        }
    }

def capturar_cartas():
    """Detecta en tiempo real las cartas del jugador desde DroidCam y las actualiza en su mano."""
    global mazo, jugador  

    # 📌 Capturar imagen desde DroidCam o la webcam según la configuración
    cap = cv2.VideoCapture(cfg.video_url if cfg.use_droidcam else 0)  
    ret, frame = cap.read()
    cap.release()

    if ret:
        cartas_detectadas = detectar_cartas(frame, conf=cfg.umbral_confianza)  # 📌 Usa el umbral configurado
        for carta_str in cartas_detectadas:
            if carta_str in card_map:
                valor, palo = card_map[carta_str]
                nueva_carta = Carta(valor, palo)
                if str(nueva_carta) not in [str(carta) for carta in jugador.mano]:  # Evita duplicados
                    jugador.mano.append(nueva_carta)

        # 🔥 Eliminamos del mazo solo las cartas detectadas en la vida real
        mazo.eliminar_cartas_detectadas([str(carta) for carta in jugador.mano])

        print(f"🎴 Cartas detectadas en físico: {jugador.mostrar_mano()} - Puntos: {jugador.calcular_puntaje()}")

    return {
        'jugador': {
            'cartas': [str(carta) for carta in jugador.mano],
            'puntos': jugador.calcular_puntaje()
        }
    }


def determinar_ganador():
    """Determina quién gana el juego según los puntajes finales."""
    jugador_puntaje = jugador.calcular_puntaje()
    dealer_puntaje = dealer.calcular_puntaje()
    
    if jugador_puntaje > 21:
        resultado = "Dealer gana, el jugador se pasó de 21!"
    elif dealer_puntaje > 21:
        resultado = "Jugador gana, el dealer se pasó de 21!"
    elif jugador_puntaje > dealer_puntaje:
        resultado = "Jugador gana con más puntos!"
    elif dealer_puntaje > jugador_puntaje:
        resultado = "Dealer gana con más puntos!"
    else:
        resultado = "Empate, ambos tienen la misma puntuación!"
    
    print(f"🏆 {resultado}")
    
    return {
        'resultado': resultado,
        'jugador': {
            'cartas': [str(carta) for carta in jugador.mano],
            'puntos': jugador_puntaje
        },
        'dealer': {
            'cartas': [str(carta) for carta in dealer.mano],
            'puntos': dealer_puntaje
        }
    }



def turno_dealer():
    """El dealer juega su turno usando Minimax tras el plantarse del jugador."""
    global mazo, dealer  
    
    while True:
        accion_dealer = dealer_ai.decidir_accion(dealer.mano, jugador.calcular_puntaje())
        if accion_dealer == "tomar carta":
            nueva_carta = mazo.repartir_carta()
            if nueva_carta:
                dealer.mano.append(nueva_carta)
                mazo.eliminar_cartas_detectadas([str(nueva_carta)])
                print(f"🤖 Dealer toma una carta: {dealer.mostrar_mano()} - Puntos: {dealer.calcular_puntaje()}")
                
                if dealer.calcular_puntaje() > 21:
                    print("💀 Dealer se pasó de 21, el jugador gana!")
                    return {'resultado': 'Jugador gana', 'dealer': dealer.mostrar_mano(), 'puntos': dealer.calcular_puntaje()}
        else:
            print(f"🤖 Dealer decide plantarse con {dealer.mostrar_mano()} - Puntos: {dealer.calcular_puntaje()}")
            break
    
    return {
        'dealer': {
            'cartas': [str(carta) for carta in dealer.mano],
            'puntos': dealer.calcular_puntaje()
        }
    }

