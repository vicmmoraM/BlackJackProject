document.getElementById("btnIniciar").addEventListener("click", function() {
    fetch("/iniciar", { method: "POST" })
    .then(response => response.json())
    .then(data => {
        document.getElementById("jugador-cartas").innerHTML = data.jugador.cartas.join(", ");
        document.getElementById("jugador-puntos").textContent = "Puntos: " + data.jugador.puntos;
        document.getElementById("dealer-cartas").innerHTML = data.dealer.cartas.join(", ");
        document.getElementById("dealer-puntos").textContent = "Puntos: " + data.dealer.puntos;
        document.getElementById("btnDealer").disabled = false; // Habilitar botón del dealer
    });
});

document.getElementById("btnDealer").addEventListener("click", function() {
    fetch("/dealer", { method: "POST" })
    .then(response => response.json())
    .then(data => {
        document.getElementById("dealer-cartas").innerHTML = data.dealer.cartas.join(", ");
        document.getElementById("dealer-puntos").textContent = "Puntos: " + data.dealer.puntos;
    });
});

