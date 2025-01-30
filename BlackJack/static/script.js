document.addEventListener("DOMContentLoaded", function() {
    let currentBet = 0;
    let hasDoubled = false;

    document.querySelectorAll(".chip").forEach(chip => {
        chip.addEventListener("click", function() {
            currentBet = parseInt(this.getAttribute("data-value"));
            document.getElementById("betAmount").textContent = currentBet;
        });
    });

    document.getElementById("btnConfirmBet").addEventListener("click", function() {
        if (currentBet > 0) {
            document.getElementById("finalBetAmount").textContent = currentBet;
            document.querySelector(".betting-container").style.display = "none";
            document.querySelector(".game-container").style.display = "block";
        } else {
            alert("Por favor, seleccione una apuesta antes de continuar.");
        }
    });

    document.getElementById("btnIniciar").addEventListener("click", function() {
        fetch("/iniciar", { method: "POST" })
        .then(response => response.json())
        .then(data => {
            document.getElementById("dealerCartas").innerHTML = "Dealer: " + data.dealer.cartas.join(", ");
            document.getElementById("dealerPuntos").textContent = "Puntos: " + data.dealer.puntos;
            document.getElementById("resultado").innerText = "";
        });
    });

    document.getElementById("btnCapturar").addEventListener("click", function() {
        fetch("/capturar_cartas", { method: "POST" })
        .then(response => response.json())
        .then(data => {
            document.getElementById("jugadorCartas").innerHTML = "Jugador: " + data.jugador.cartas.join(", ");
            document.getElementById("jugadorPuntos").textContent = "Puntos: " + data.jugador.puntos;
        });
    });

    document.getElementById("btnPlantar").addEventListener("click", function() {
        fetch("/plantarse", { method: "POST" })
        .then(response => response.json())
        .then(data => {
            document.getElementById("dealerCartas").innerHTML = "Dealer: " + data.dealer.cartas.join(", ");
            document.getElementById("dealerPuntos").textContent = "Puntos: " + data.dealer.puntos;
            document.getElementById("resultado").innerText = data.resultado || "Fin del juego";

            // 🔥 Deshabilitar botones después de plantarse
            document.getElementById("btnCapturar").disabled = true;
            document.getElementById("btnTomar").disabled = true;
            document.getElementById("btnDoblar").disabled = true;
        });
    });

    document.getElementById("btnDoblar").addEventListener("click", function() {
        if (!hasDoubled) {
            let betAmountElement = document.getElementById("finalBetAmount");
            let currentBet = parseInt(betAmountElement.textContent);
            let doubledBet = currentBet * 2;
            betAmountElement.textContent = doubledBet;
            hasDoubled = true;
        } else {
            alert("Solo puedes doblar la apuesta una vez.");
        }
    });

    document.getElementById("btnTomar").addEventListener("click", function() {
        fetch("/capturar_cartas", { method: "POST" })  // 🔥 Se mantiene capturar cartas aquí
        .then(response => response.json())
        .then(data => {
            document.getElementById("jugadorCartas").innerHTML = "Jugador: " + data.jugador.cartas.join(", ");
            document.getElementById("jugadorPuntos").textContent = "Puntos: " + data.jugador.puntos;
        });
    });
});

