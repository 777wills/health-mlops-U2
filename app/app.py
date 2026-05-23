from flask import Flask, request, jsonify, render_template_string

app = Flask(__name__)

HTML_FORM = """
<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <title>Servicio de Predicción Médica Simulada</title>
    <style>
        body { font-family: Arial, sans-serif; margin: 40px; background: #f5f7fa; }
        .container { max-width: 600px; margin: auto; background: white; padding: 25px; border-radius: 12px; box-shadow: 0 2px 10px rgba(0,0,0,0.1); }
        input, button { width: 100%; padding: 10px; margin-top: 8px; margin-bottom: 15px; }
        button { background: #1f6feb; color: white; border: none; border-radius: 6px; cursor: pointer; }
        .result { padding: 15px; background: #eef6ff; border-left: 5px solid #1f6feb; margin-top: 15px; }
    </style>
</head>
<body>
<div class="container">
    <h2>Predicción médica simulada</h2>
    <p>Ingrese tres valores clínicos simulados para obtener una clasificación.</p>
    <form method="post" action="/predecir_form">
        <label>Temperatura corporal °C:</label>
        <input type="number" step="0.1" name="temperatura" required>

        <label>Número de síntomas reportados:</label>
        <input type="number" name="sintomas" required>

        <label>Días de evolución:</label>
        <input type="number" name="dias_evolucion" required>

        <button type="submit">Predecir</button>
    </form>

    {% if resultado %}
    <div class="result">
        <strong>Resultado:</strong> {{ resultado }}
    </div>
    {% endif %}
</div>
</body>
</html>
"""


def predecir_estado(temperatura: float, sintomas: int, dias_evolucion: int) -> str:
    """
    Función simulada de predicción.

    Recibe tres variables clínicas básicas:
    - temperatura: temperatura corporal del paciente.
    - sintomas: cantidad de síntomas reportados.
    - dias_evolucion: días desde el inicio de los síntomas.

    Retorna uno de los cinco estados requeridos:
    - NO ENFERMO
    - ENFERMEDAD LEVE
    - ENFERMEDAD AGUDA
    - ENFERMEDAD TERMINAL
    - ENFERMEDAD CRÓNICA
    """

    if temperatura < 37.2 and sintomas <= 1 and dias_evolucion <= 2:
        return "NO ENFERMO"

    if temperatura < 38.0 and sintomas <= 3 and dias_evolucion <= 5:
        return "ENFERMEDAD LEVE"

    if temperatura >= 38.0 and sintomas >= 4 and dias_evolucion <= 14:
        return "ENFERMEDAD AGUDA"

    if temperatura >= 39.5 and sintomas >= 6 and dias_evolucion > 21:
        return "ENFERMEDAD TERMINAL"

    return "ENFERMEDAD CRÓNICA"


@app.route("/", methods=["GET"])
def home():
    return render_template_string(HTML_FORM, resultado=None)


@app.route("/predecir_form", methods=["POST"])
def predecir_form():
    temperatura = float(request.form["temperatura"])
    sintomas = int(request.form["sintomas"])
    dias_evolucion = int(request.form["dias_evolucion"])
    resultado = predecir_estado(temperatura, sintomas, dias_evolucion)
    return render_template_string(HTML_FORM, resultado=resultado)


@app.route("/predecir", methods=["POST"])
def predecir_api():
    data = request.get_json()

    if not data:
        return (
            jsonify(
                {
                    "error": "Debe enviar un JSON con temperatura, sintomas y dias_evolucion"
                }
            ),
            400,
        )

    campos_requeridos = ["temperatura", "sintomas", "dias_evolucion"]
    for campo in campos_requeridos:
        if campo not in data:
            return jsonify({"error": f"Falta el campo requerido: {campo}"}), 400

    try:
        temperatura = float(data["temperatura"])
        sintomas = int(data["sintomas"])
        dias_evolucion = int(data["dias_evolucion"])
    except ValueError:
        return jsonify({"error": "Los valores deben ser numéricos"}), 400

    resultado = predecir_estado(temperatura, sintomas, dias_evolucion)

    return jsonify(
        {
            "entrada": {
                "temperatura": temperatura,
                "sintomas": sintomas,
                "dias_evolucion": dias_evolucion,
            },
            "prediccion": resultado,
            "nota": "Predicción simulada con fines académicos. No corresponde a un diagnóstico médico real.",
        }
    )


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
