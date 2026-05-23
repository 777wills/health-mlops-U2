import json
import os
from collections import Counter
from datetime import datetime

from flask import Flask, request, jsonify, render_template_string, send_file

app = Flask(__name__)

LOG_FILE = os.path.join(
    os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "predicciones.jsonl"
)

HTML_FORM = """
<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <title>Servicio de Predicción Médica Simulada</title>
    <style>
        body { font-family: Arial, sans-serif; margin: 40px; background: #f5f7fa; }
        .container { max-width: 600px; margin: auto; background: white; padding: 25px; border-radius: 12px; box-shadow: 0 2px 10px rgba(0,0,0,0.1); }
        input, button { box-sizing: border-box; width: 100%; padding: 10px; margin-top: 8px; margin-bottom: 15px; }
        button { background: #1f6feb; color: white; border: none; border-radius: 6px; cursor: pointer; }
        .btn-reporte { background: #28a745; margin-top: 10px; display: inline-block; text-align: center; text-decoration: none; padding: 10px; border-radius: 6px; color: white; width: 100%; box-sizing: border-box; }
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

    <a href="/reporte" class="btn-reporte">Ver reporte de predicciones</a>
</div>
</body>
</html>
"""


def registrar_prediccion(
    temperatura: float, sintomas: int, dias_evolucion: int, resultado: str
):
    registro = {
        "temperatura": temperatura,
        "sintomas": sintomas,
        "dias_evolucion": dias_evolucion,
        "prediccion": resultado,
        "fecha": datetime.now().isoformat(),
    }
    with open(LOG_FILE, "a", encoding="utf-8") as f:
        f.write(json.dumps(registro, ensure_ascii=False) + "\n")


def obtener_estadisticas() -> dict:
    if not os.path.exists(LOG_FILE):
        return {
            "total_por_categoria": {},
            "ultimas_5": [],
            "fecha_ultima_prediccion": "Sin predicciones",
        }

    registros = []
    with open(LOG_FILE, "r", encoding="utf-8") as f:
        for linea in f:
            linea = linea.strip()
            if linea:
                registros.append(json.loads(linea))

    if not registros:
        return {
            "total_por_categoria": {},
            "ultimas_5": [],
            "fecha_ultima_prediccion": "Sin predicciones",
        }

    conteo = Counter(r["prediccion"] for r in registros)
    ultimas_5 = registros[-5:]
    ultimas_5.reverse()
    fecha_ultima = registros[-1]["fecha"]

    return {
        "total_por_categoria": dict(conteo),
        "ultimas_5": ultimas_5,
        "fecha_ultima_prediccion": fecha_ultima,
    }


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
    registrar_prediccion(temperatura, sintomas, dias_evolucion, resultado)
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
    registrar_prediccion(temperatura, sintomas, dias_evolucion, resultado)

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


HTML_REPORTE = """
<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <title>Reporte de Predicciones</title>
    <style>
        body { font-family: Arial, sans-serif; margin: 40px; background: #f5f7fa; }
        .container { max-width: 700px; margin: auto; background: white; padding: 25px; border-radius: 12px; box-shadow: 0 2px 10px rgba(0,0,0,0.1); }
        table { width: 100%; border-collapse: collapse; margin-top: 15px; }
        th, td { padding: 10px; border: 1px solid #ddd; text-align: left; }
        th { background: #1f6feb; color: white; }
        .fecha { padding: 10px; background: #eef6ff; border-left: 5px solid #1f6feb; margin-top: 15px; }
        a { color: #1f6feb; }
        .btn-descargar { display: block; margin-top: 20px; background: #1f6feb; color: white; text-align: center; padding: 10px; border-radius: 6px; text-decoration: none; }
    </style>
</head>
<body>
<div class="container">
    <h2>Reporte de Predicciones</h2>
    <p><a href="/">← Volver al formulario</a></p>

    <h3>Total de predicciones por categoría</h3>
    {% if total_por_categoria %}
    <table>
        <tr><th>Categoría</th><th>Total</th></tr>
        {% for categoria, total in total_por_categoria.items() %}
        <tr><td>{{ categoria }}</td><td>{{ total }}</td></tr>
        {% endfor %}
    </table>
    {% else %}
    <p>No hay predicciones registradas.</p>
    {% endif %}

    <h3>Últimas 5 predicciones</h3>
    {% if ultimas_5 %}
    <table>
        <tr><th>Fecha</th><th>Temperatura</th><th>Síntomas</th><th>Días</th><th>Predicción</th></tr>
        {% for r in ultimas_5 %}
        <tr>
            <td>{{ r.fecha }}</td>
            <td>{{ r.temperatura }}</td>
            <td>{{ r.sintomas }}</td>
            <td>{{ r.dias_evolucion }}</td>
            <td>{{ r.prediccion }}</td>
        </tr>
        {% endfor %}
    </table>
    {% else %}
    <p>No hay predicciones registradas.</p>
    {% endif %}

    <h3>Fecha de la última predicción</h3>
    <div class="fecha">
        <strong>{{ fecha_ultima_prediccion }}</strong>
    </div>

    <a href="/reporte/descargar" class="btn-descargar">⬇ Descargar reporte JSON</a>
</div>
</body>
</html>
"""


@app.route("/reporte", methods=["GET"])
def reporte():
    estadisticas = obtener_estadisticas()

    if request.args.get("format") == "json":
        return jsonify(estadisticas)

    return render_template_string(HTML_REPORTE, **estadisticas)


@app.route("/reporte/descargar", methods=["GET"])
def descargar_reporte():
    estadisticas = obtener_estadisticas()
    reporte_json = json.dumps(estadisticas, ensure_ascii=False, indent=2)

    from io import BytesIO

    buffer = BytesIO(reporte_json.encode("utf-8"))
    buffer.seek(0)
    return send_file(
        buffer,
        mimetype="application/json",
        as_attachment=True,
        download_name="reporte_predicciones.json",
    )


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
