from flask import Flask, render_template, request, jsonify
from blackjack_logic import iniciar_juego, detectar_cartas_jugador, turno_dealer, jugador, dealer

app = Flask(__name__)

@app.route('/')
def index():
    """Página principal del Blackjack."""
    return render_template('index.html')

@app.route('/iniciar', methods=['POST'])
def iniciar():
    """Inicia el juego y reparte las cartas iniciales al dealer."""
    iniciar_juego()
    return jsonify({
        'dealer': {
            'cartas': dealer.mostrar_mano().split(', '),
            'puntos': dealer.calcular_puntaje()
        }
    })

@app.route('/capturar_cartas', methods=['POST'])
def capturar_cartas():
    """Captura las cartas del jugador y el dealer juega automáticamente después."""
    detectar_cartas_jugador()
    return jsonify({
        'jugador': {
            'cartas': jugador.mostrar_mano().split(', '),
            'puntos': jugador.calcular_puntaje()
        },
        'dealer': {
            'cartas': dealer.mostrar_mano().split(', '),
            'puntos': dealer.calcular_puntaje()
        }
    })

@app.route('/plantarse', methods=['POST'])
def plantarse():
    """El jugador decide plantarse, el dealer juega automáticamente."""
    turno_dealer()
    return jsonify({
        'dealer': {
            'cartas': dealer.mostrar_mano().split(', '),
            'puntos': dealer.calcular_puntaje()
        }
    })


if __name__ == '__main__':
    app.run(debug=True)