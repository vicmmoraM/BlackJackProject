from flask import Flask, render_template, request, jsonify
from blackjack_logic import iniciar_juego, turno_dealer, jugador, dealer

app = Flask(__name__)

@app.route('/')
def index():
    """Página principal del Blackjack."""
    return render_template('index.html')

@app.route('/iniciar', methods=['POST'])
def iniciar():
    """Inicia el juego y detecta las cartas del jugador."""
    iniciar_juego()
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

@app.route('/dealer', methods=['POST'])
def dealer_turn():
    """Ejecuta el turno del dealer usando IA."""
    turno_dealer()
    return jsonify({
        'dealer': {
            'cartas': dealer.mostrar_mano().split(', '),
            'puntos': dealer.calcular_puntaje()
        }
    })

if __name__ == '__main__':
    app.run(debug=True)
