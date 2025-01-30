import webview

html = """
<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Mesa de Blackjack</title>
    <style>
        body {
            background-color: green;
            color: white;
            text-align: center;
            font-family: Arial, sans-serif;
        }
        .card {
            display: inline-block;
            width: 80px;
            height: 120px;
            background-color: white;
            color: black;
            border-radius: 10px;
            text-align: center;
            line-height: 120px;
            font-size: 24px;
            margin: 10px;
            box-shadow: 2px 2px 5px rgba(0, 0, 0, 0.3);
        }
    </style>
</head>
<body>
    <h1>Mesa de Blackjack</h1>
    <div class="card">A ♠</div>
    <div class="card">10 ♥</div>
    <div class="card">K ♦</div>
    <div class="card">7 ♣</div>
</body>
</html>
"""

webview.create_window("Blackjack UI", html=html)
webview.start()