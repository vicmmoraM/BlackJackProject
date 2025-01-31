document.addEventListener("DOMContentLoaded", function() {
    let currentBet = 0;
    let hasDoubled = false;

    // Manejar clic en fichas de apuesta para acumular valor
    document.querySelectorAll(".chip").forEach(chip => {
        chip.addEventListener("click", function() {
            let betValue = parseInt(this.getAttribute("data-value"));
            currentBet += betValue; // 🔥 Se suma la apuesta en vez de reemplazarla
            document.getElementById("betAmount").textContent = currentBet;
        });
    });

    // Confirmar apuesta y mostrar pantalla de juego
    document.getElementById("btnConfirmBet").addEventListener("click", function() {
        if (currentBet > 0) {
            document.getElementById("finalBetAmount").textContent = currentBet;
            document.querySelector(".betting-container").style.display = "none";
            document.querySelector(".game-container").style.display = "block";
        } else {
            alert("Por favor, seleccione una apuesta antes de continuar.");
        }
    });

    // 📌 FONDO DINÁMICO DE CASINO (SIN ROMPER NADA)
    const iconos = ["🎲", "🎰", "🃏", "♦️", "♠️", "♥️", "♣️", "💰", "🎟️", "🏆"]; // Iconos de casino

    const fondoCasino = document.createElement("div");
    fondoCasino.classList.add("fondo-casino");
    document.body.appendChild(fondoCasino);

    const bordeNeon = document.createElement("div");
    bordeNeon.classList.add("borde-neon");
    document.body.appendChild(bordeNeon);

    for (let i = 0; i < 15; i++) { // 🔥 Agrega 15 elementos flotantes
        let icono = document.createElement("div");
        icono.classList.add("icono-casino");
        icono.textContent = iconos[Math.floor(Math.random() * iconos.length)];

        // Posición aleatoria en la pantalla
        icono.style.left = Math.random() * 100 + "vw";
        icono.style.top = Math.random() * 100 + "vh";
        icono.style.animationDuration = (8 + Math.random() * 5) + "s"; // 🔥 Duración aleatoria
        icono.style.animationDelay = Math.random() * 5 + "s"; // 🔥 Empiezan en tiempos distintos

        fondoCasino.appendChild(icono);
    }

    // 📌 AQUÍ SIGUEN TUS FUNCIONES ORIGINALES (NO SE BORRAN)
    
    function obtenerSimbolo(palo) {
        const simbolos = {
            "Corazones": "♥",
            "Diamantes": "♦",
            "Tréboles": "♣",
            "Picas": "♠"
        };
        return simbolos[palo] || "";
    }

    function generarCartaHTML(carta) {
        let partes = carta.split(" de "); 
        let valor = partes[0];
        let palo = partes[1];

        let simbolo = obtenerSimbolo(palo);
        
        let divCarta = document.createElement("div");
        divCarta.classList.add("card");
        divCarta.setAttribute("data-value", valor);

        if (palo === "Corazones" || palo === "Diamantes") {
            divCarta.classList.add("red");
        }

        let divPalo = document.createElement("div");
        divPalo.classList.add("palo");
        divPalo.textContent = simbolo;

        divCarta.appendChild(divPalo);
        return divCarta;
    }

    function actualizarCartas(elementId, cartas) {
        let container = document.getElementById(elementId);
        container.innerHTML = ""; 

        cartas.forEach(carta => {
            let cartaHTML = generarCartaHTML(carta);
            container.appendChild(cartaHTML);
        });
    }

    document.getElementById("btnIniciar").addEventListener("click", function() {
        fetch("/iniciar", { method: "POST" })
        .then(response => response.json())
        .then(data => {
            actualizarCartas("dealerCartas", data.dealer.cartas);
            actualizarCartas("jugadorCartas", data.jugador.cartas);
            document.getElementById("dealerPuntos").textContent = "Puntos: " + data.dealer.puntos;
            document.getElementById("jugadorPuntos").textContent = "Puntos: " + data.jugador.puntos;
            document.getElementById("resultado").innerText = "";
        });
    });

    document.getElementById("btnCapturar").addEventListener("click", function() {
        fetch("/capturar_cartas", { method: "POST" })
        .then(response => response.json())
        .then(data => {
            actualizarCartas("jugadorCartas", data.jugador.cartas);
            document.getElementById("jugadorPuntos").textContent = "Puntos: " + data.jugador.puntos;
        });
    });

    document.getElementById("btnPlantar").addEventListener("click", function() {
        fetch("/plantarse", { method: "POST" })
        .then(response => response.json())
        .then(data => {
            actualizarCartas("dealerCartas", data.dealer.cartas);
            document.getElementById("dealerPuntos").textContent = "Puntos: " + data.dealer.puntos;
            document.getElementById("resultado").innerText = data.resultado || "Fin del juego";

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
        fetch("/capturar_cartas", { method: "POST" })
        .then(response => response.json())
        .then(data => {
            actualizarCartas("jugadorCartas", data.jugador.cartas);
            document.getElementById("jugadorPuntos").textContent = "Puntos: " + data.jugador.puntos;
        });
    });
});