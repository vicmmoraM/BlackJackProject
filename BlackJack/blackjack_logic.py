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
dealer_ai = DealerAI()

def iniciar_juego():
    """Reparte 2 cartas al dealer y prepara el juego."""
    global mazo, dealer  
    dealer.mano = [mazo.repartir_carta(), mazo.repartir_carta()]  # 🔥 Dealer recibe 2 cartas al inicio
    for carta in dealer.mano:
        if carta in mazo.cartas:
            mazo.cartas.remove(carta)  # 🔥 Eliminar cartas del mazo
    
    print(f"✅ Dealer recibe sus 2 cartas: {dealer.mostrar_mano()} - Puntos: {dealer.calcular_puntaje()}")

def detectar_cartas_jugador():
    """Captura las cartas del jugador con la cámara, las convierte a formato estándar y elimina esas cartas del mazo."""
    global mazo, jugador  

    cap = cv2.VideoCapture(cfg.video_url if cfg.use_droidcam else 0)
    ret, frame = cap.read()
    cap.release()

    if ret:
        cartas_detectadas = detectar_cartas(frame, conf=cfg.umbral_confianza)
        cartas_a_eliminar = []

        for carta_str in cartas_detectadas:
            if carta_str in card_map:  # 🔥 Convertimos la carta al formato correcto según `card_map`
                valor, palo = card_map[carta_str]
                nueva_carta = Carta(valor, palo)
                jugador.mano.append(nueva_carta)
                cartas_a_eliminar.append(str(nueva_carta))  # Convertimos a string para comparar correctamente

        # ✅ 🔥 Eliminar las cartas detectadas del mazo ANTES de que el dealer juegue
        mazo.cartas = [carta for carta in mazo.cartas if str(carta) not in cartas_a_eliminar]

        print(f"✅ Cartas detectadas y convertidas para el jugador: {jugador.mostrar_mano()} - Puntos: {jugador.calcular_puntaje()}")

    # 🚨 **Verificar si el jugador se pasó de 21**
    if jugador.calcular_puntaje() > 21:
        print("💀 ¡Te pasaste de 21, has perdido automáticamente!")
        return jsonify({
            'jugador': {
                'cartas': jugador.mostrar_mano().split(', '),
                'puntos': jugador.calcular_puntaje(),
                'mensaje': "💀 ¡Te pasaste de 21, has perdido automáticamente!"
            }
        })

    return jsonify({
        'jugador': {
            'cartas': jugador.mostrar_mano().split(', '),
            'puntos': jugador.calcular_puntaje()
        }
    })



def turno_dealer():
    """El dealer usa la IA para tomar decisiones y solo toma cartas que realmente estén en el mazo."""
    global mazo, dealer  

    while True:
        accion_dealer = dealer_ai.decidir_accion(dealer.calcular_puntaje(), jugador.calcular_puntaje())
        if accion_dealer == "tomar carta":
            nueva_carta = mazo.repartir_carta()  # 🔥 Dealer toma solo 1 carta
            if nueva_carta:
                dealer.mano.append(nueva_carta)

                # ✅ Solo eliminamos la carta si realmente está en el mazo y no la tiene el jugador
                if nueva_carta in mazo.cartas and str(nueva_carta) not in [str(c) for c in jugador.mano]:
                    mazo.cartas.remove(nueva_carta)
                else:
                    print(f"⚠️ Advertencia: La carta {nueva_carta} ya fue tomada por el jugador y no está en el mazo.")

                print(f"🤖 Dealer toma una carta: {dealer.mostrar_mano()} - Puntos: {dealer.calcular_puntaje()}")
                if dealer.calcular_puntaje() > 21:
                    print("💀 Dealer se pasó de 21, el jugador gana!")
                    break
        else:
            print(f"🤖 Dealer decide plantarse con {dealer.mostrar_mano()} - Puntos: {dealer.calcular_puntaje()}")
            break

    # ✅ Retornar la actualización para que se muestre en la interfaz
    return jsonify({
        'dealer': {
            'cartas': dealer.mostrar_mano().split(', '),
            'puntos': dealer.calcular_puntaje()
        }
    })
