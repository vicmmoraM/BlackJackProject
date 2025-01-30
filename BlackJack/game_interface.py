import sys
import cv2
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QPushButton, QVBoxLayout
from blackjack_logic import iniciar_juego, repartir_cartas_dealer, jugador, dealer

class BlackjackGUI(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setWindowTitle("Blackjack - Visión Artificial")
        self.setGeometry(100, 100, 400, 300)
        
        self.layout = QVBoxLayout()
        
        self.label_info = QLabel("Bienvenido al Blackjack", self)
        self.layout.addWidget(self.label_info)
        
        self.label_jugador = QLabel("Jugador: ", self)
        self.layout.addWidget(self.label_jugador)
        
        self.label_dealer = QLabel("Dealer: ", self)
        self.layout.addWidget(self.label_dealer)
        
        self.btn_iniciar = QPushButton("Iniciar Juego", self)
        self.btn_iniciar.clicked.connect(self.iniciar_juego)
        self.layout.addWidget(self.btn_iniciar)
        
        self.btn_repartir = QPushButton("Repartir Cartas al Dealer", self)
        self.btn_repartir.clicked.connect(self.repartir_cartas)
        self.btn_repartir.setEnabled(False)  # Desactivado hasta iniciar el juego
        self.layout.addWidget(self.btn_repartir)
        
        self.setLayout(self.layout)

    def actualizar_pantalla(self):
        """Actualiza las etiquetas con las cartas y puntos actuales."""
        self.label_jugador.setText(f"Jugador: {jugador.mostrar_mano()} - Puntos: {jugador.calcular_puntaje()}")
        self.label_dealer.setText(f"Dealer: {dealer.mostrar_mano()} - Puntos: {dealer.calcular_puntaje()}")

    def iniciar_juego(self):
        iniciar_juego()
        self.actualizar_pantalla()
        self.label_info.setText("✅ Cartas detectadas y asignadas al jugador.")
        self.btn_repartir.setEnabled(True)  # Habilitar el botón de repartir al dealer

    def repartir_cartas(self):
        repartir_cartas_dealer()
        self.actualizar_pantalla()
        self.label_info.setText("✅ Cartas repartidas al dealer.")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = BlackjackGUI()
    window.show()
    sys.exit(app.exec_())
