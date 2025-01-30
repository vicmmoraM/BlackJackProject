import cv2
import numpy as np
from detectar_cartas import detectar_cartas
import configuracion as cfg
from mazo import Carta, Mazo
from jugador import Jugador
from dealer_ai import DealerAI

# Configuración de la cámara
use_droidcam = cfg.use_droidcam
video_url = cfg.video_url
umbral_confianza = cfg.umbral_confianza

# Inicializar el juego
mazo = Mazo()
jugador = Jugador("Jugador")
dealer = Jugador("Dealer")
dealer_ai = DealerAI()

def iniciar_juego():
    """Reparte cartas iniciales al jugador y al dealer, y elimina las cartas usadas del mazo."""
    global mazo, jugador, dealer  # Asegurar que usamos las instancias globales
    
    # 🔥 Detectar cartas en la mesa y asignarlas al jugador
    cap = cv2.VideoCapture(cfg.video_url if cfg.use_droidcam else 0)
    ret, frame = cap.read()
    cap.release()
    
    if ret:
        cartas_detectadas = detectar_cartas(frame, conf=cfg.umbral_confianza)
        cartas_a_eliminar = []
        
        for carta_str in cartas_detectadas:
            valor, palo = carta_str[:-1], carta_str[-1]  # Extraer valor y palo de "8C", "7H", etc.
            nueva_carta = Carta(valor, palo)
            jugador.mano.append(nueva_carta)
            cartas_a_eliminar.append(nueva_carta)
        
        # 🔥 Eliminar las cartas detectadas del mazo
        mazo.cartas = [carta for carta in mazo.cartas if carta not in cartas_a_eliminar]
    
    # 🔥 Repartir 2 cartas al dealer y eliminarlas del mazo
    dealer.mano = [mazo.repartir_carta(), mazo.repartir_carta()]
    for carta in dealer.mano:
        mazo.cartas.remove(carta)  # 🔥 Eliminar cartas del dealer

    print(f"✅ Cartas iniciales del jugador: {jugador.mostrar_mano()} - Puntos: {jugador.calcular_puntaje()}")
    print(f"✅ Cartas iniciales del dealer: {dealer.mostrar_mano()} - Puntos: {dealer.calcular_puntaje()}")

def turno_dealer():
    """El dealer usa la IA para tomar decisiones y elimina las cartas usadas del mazo."""
    global mazo, dealer  # Asegurar que usamos las instancias globales

    while True:
        accion_dealer = dealer_ai.decidir_accion(dealer.calcular_puntaje(), jugador.calcular_puntaje())
        if accion_dealer == "tomar carta":
            nueva_carta = mazo.repartir_carta()
            dealer.mano.append(nueva_carta)
            mazo.cartas.remove(nueva_carta)  # 🔥 Eliminar la carta del mazo
            
            print(f"🤖 Dealer toma una carta: {dealer.mostrar_mano()} - Puntos: {dealer.calcular_puntaje()}")
            if dealer.calcular_puntaje() > 21:
                print("💀 Dealer se pasó de 21, el jugador gana!")
                break
        else:
            print(f"🤖 Dealer decide plantarse con {dealer.mostrar_mano()} - Puntos: {dealer.calcular_puntaje()}")
            break
