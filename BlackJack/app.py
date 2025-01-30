from flask import Flask, render_template, request, jsonify
from blackjack_logic import iniciar_juego, capturar_cartas, turno_dealer, determinar_ganador

app = Flask(__name__)

@app.route('/')
def index():
    """Página principal del Blackjack."""
    return render_template('index.html')

@app.route('/iniciar', methods=['POST'])
def iniciar():
    """Inicia el juego y reparte las cartas iniciales al dealer y jugador."""
    respuesta = iniciar_juego()
    return jsonify(respuesta)

@app.route('/capturar_cartas', methods=['POST'])
def capturar():
    """El jugador toma una nueva carta."""
    respuesta = capturar_cartas()
    return jsonify(respuesta)

@app.route('/plantarse', methods=['POST'])
def plantarse():
    """El jugador se planta, el dealer juega su turno y se determina el ganador."""
    turno_dealer()
    respuesta = determinar_ganador()
    return jsonify(respuesta)

@app.route('/doblar_apuesta', methods=['POST'])
def doblar():
    """Doble la apuesta del jugador (manejado en el frontend también)."""
    nueva_apuesta = int(request.json['apuesta']) * 2
    return jsonify({'nueva_apuesta': nueva_apuesta})

if __name__ == '__main__':
    app.run(debug=True)
