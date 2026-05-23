# Servicio Docker para predicción médica simulada

# Presentado por Anderson Trujillo y William suaza

## 1. Finalidad de la solución

La solución simula un servicio de predicción médica que permite a un médico ingresar tres variables clínicas básicas y recibir una clasificación general del estado del paciente.

La función no corresponde a un modelo real entrenado. Se desarrolló para simular el comportamiento esperado de un modelo de Machine Learning.

## 2. Estados que retorna la solución

La solución puede retornar los siguientes estados:

- NO ENFERMO
- ENFERMEDAD LEVE
- ENFERMEDAD AGUDA
- ENFERMEDAD TERMINAL
- ENFERMEDAD CRÓNICA

## 3. Variables de entrada

El servicio recibe tres valores:

| Variable       | Descripción                                         | Ejemplo |
| -------------- | --------------------------------------------------- | ------- |
| temperatura    | Temperatura corporal del paciente en grados Celsius | 38.5    |
| sintomas       | Número de síntomas reportados                       | 5       |
| dias_evolucion | Días desde el inicio de los síntomas                | 7       |

## 4. Estructura del proyecto

```text
mlops_entregable_enfermedades/
│
├── Dockerfile
├── README.md
│
├── app/
│   ├── app.py
│   └── requirements.txt
│
└── docs/
    └── pipeline_mlops.md
```

## 5. Construir la imagen Docker

Desde la raíz del proyecto, ejecutar:

```bash
docker build -t prediccion-medica-mlops .
```

## 6. Correr el contenedor

Ejecutar:

```bash
docker run -p 5000:5000 prediccion-medica-mlops
```

Luego abrir en el navegador:

```text
http://localhost:5000
```

## 7. Usar la solución desde la página web

Al abrir `http://localhost:5000`, el médico encontrará un formulario sencillo donde podrá ingresar:

- Temperatura corporal.
- Número de síntomas.
- Días de evolución.

Después de presionar el botón **Predecir**, la aplicación mostrará el estado estimado.

## 8. Usar la solución desde API

También se puede consumir el servicio mediante una petición POST al endpoint:

```text
http://localhost:5000/predecir
```

Ejemplo con `curl`:

```bash
curl -X POST http://localhost:5000/predecir \
  -H "Content-Type: application/json" \
  -d '{"temperatura": 38.5, "sintomas": 5, "dias_evolucion": 7}'
```

Respuesta esperada:

```json
{
  "entrada": {
    "temperatura": 38.5,
    "sintomas": 5,
    "dias_evolucion": 7
  },
  "prediccion": "ENFERMEDAD AGUDA",
  "nota": "Predicción simulada con fines académicos. No corresponde a un diagnóstico médico real."
}
```

## 9. Reporte de estadísticas

Los médicos pueden consultar un reporte con estadísticas de las predicciones realizadas accediendo a:

```text
http://localhost:5000/reporte
```

El reporte incluye:

- **Número total de predicciones por categoría.**
- **Últimas 5 predicciones realizadas** (con fecha, datos de entrada y resultado).
- **Fecha de la última predicción.**

También se puede obtener el reporte en formato JSON:

```bash
curl http://localhost:5000/reporte?format=json
```

Respuesta esperada:

```json
{
  "total_por_categoria": {
    "NO ENFERMO": 2,
    "ENFERMEDAD AGUDA": 1
  },
  "ultimas_5": [
    {
      "temperatura": 38.5,
      "sintomas": 5,
      "dias_evolucion": 7,
      "prediccion": "ENFERMEDAD AGUDA",
      "fecha": "2026-05-23T10:30:00.123456"
    }
  ],
  "fecha_ultima_prediccion": "2026-05-23T10:30:00.123456"
}
```

> **Nota:** Las predicciones se almacenan en un archivo interno del contenedor. Si se reinicia el contenedor, el historial se pierde.

## 10. Casos de prueba sugeridos

| Temperatura | Síntomas | Días de evolución | Resultado esperado |
| ----------: | -------: | ----------------: | ------------------ |
|        36.8 |        0 |                 1 | NO ENFERMO         |
|        37.5 |        2 |                 3 | ENFERMEDAD LEVE    |
|        39.0 |        5 |                 4 | ENFERMEDAD AGUDA   |
|        37.8 |        4 |                20 | ENFERMEDAD CRÓNICA |

## 11. Nota académica

Esta solución fue diseñada para demostrar el empaquetamiento y despliegue de un servicio de inferencia mediante Docker. En un escenario real, la función de reglas sería reemplazada por un modelo de Machine Learning entrenado, validado, versionado y monitoreado bajo un pipeline de MLOps.
