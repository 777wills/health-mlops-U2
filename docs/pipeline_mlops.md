# Entregable 1 – Pipeline de MLOps para predicción de enfermedades comunes y huérfanas

## 1. Contexto del problema

En el campo de la medicina existe una gran cantidad de información clínica de pacientes. Sin embargo, no todas las enfermedades cuentan con la misma disponibilidad de datos. Para enfermedades comunes suele existir un volumen amplio de registros, mientras que para enfermedades huérfanas la información puede ser limitada, dispersa o difícil de etiquetar.

El objetivo general es proponer un pipeline de Machine Learning Operations, MLOps, para construir, validar, desplegar y monitorear un modelo que, a partir de síntomas y variables clínicas de un paciente, permita estimar si existe posibilidad de enfermedad y clasificar el resultado en estados como: no enfermo, enfermedad leve, enfermedad aguda, enfermedad terminal o enfermedad crónica.

La solución debe entenderse como un apoyo a la decisión médica, no como un reemplazo del criterio clínico del profesional de salud.

---

## 2. Diagrama general del pipeline propuesto

```mermaid
flowchart LR
    A[Definición del problema clínico] --> B[Recolección de datos]
    B --> C[Validación, anonimización y gobierno de datos]
    C --> D[Preparación y transformación de datos]
    D --> E[Entrenamiento de modelos]
    E --> F[Validación clínica y técnica]
    F --> G[Registro y versionamiento del modelo]
    G --> H[Despliegue del servicio]
    H --> I[Monitoreo en producción]
    I --> J[Reentrenamiento y mejora continua]
    J --> D
```

---

## 3. Etapas del pipeline de MLOps

### 3.1 Diseño de la solución

En esta fase se define el objetivo clínico, el alcance del modelo, las restricciones del problema y los criterios mínimos de aceptación.

**Objetivo del modelo:**

Predecir, a partir de síntomas y variables clínicas, si un paciente podría presentar una enfermedad, diferenciando entre estados como no enfermo, enfermedad leve, enfermedad aguda, enfermedad terminal o enfermedad crónica.

**Restricciones principales:**

- Los datos médicos son sensibles y requieren protección, anonimización y control de acceso.
- Las enfermedades huérfanas tienen pocos registros disponibles, lo que puede generar desbalance de clases.
- El modelo debe ser interpretable o explicable, dado que será utilizado como apoyo para médicos.
- La predicción no debe considerarse diagnóstico definitivo.
- Se deben minimizar falsos negativos, especialmente cuando la enfermedad puede ser grave.
- Debe existir trazabilidad sobre qué datos, versión del modelo y parámetros generaron una predicción.

**Tipos de datos posibles:**

- Síntomas reportados por el paciente.
- Signos vitales: temperatura, frecuencia cardíaca, presión arterial, saturación de oxígeno.
- Antecedentes médicos.
- Resultados de laboratorio.
- Edad, sexo, peso, comorbilidades y otros factores de riesgo.
- Notas clínicas estructuradas o semiestructuradas.
- Etiquetas clínicas previamente validadas por médicos.

---

### 3.2 Recolección de datos

Los datos pueden provenir de diferentes fuentes clínicas. En un escenario real, podrían integrarse historias clínicas electrónicas, bases hospitalarias, registros de laboratorio, sistemas de urgencias, bases de enfermedades huérfanas y formularios de captura directa diligenciados por médicos.

Para enfermedades comunes se podría contar con un volumen alto de observaciones. Para enfermedades huérfanas, se requiere una estrategia especial, porque la baja cantidad de casos puede afectar el aprendizaje del modelo.

**Estrategias para enfermedades huérfanas:**

- Consolidar datos de diferentes instituciones, previa autorización y anonimización.
- Usar aprendizaje por transferencia, aprovechando patrones aprendidos de enfermedades comunes.
- Aplicar técnicas de balanceo de clases, como sobremuestreo controlado.
- Usar modelos robustos para pocos datos, como árboles de decisión, random forest, gradient boosting o modelos bayesianos.
- Incorporar conocimiento experto de médicos para validar reglas clínicas.

---

### 3.3 Gobierno, calidad y anonimización de datos

Antes de entrenar el modelo, los datos deben pasar por controles de calidad y privacidad.

**Actividades principales:**

- Eliminación o anonimización de datos personales identificables.
- Validación de completitud de registros.
- Identificación de valores atípicos o inconsistentes.
- Revisión de variables con demasiados datos faltantes.
- Validación de etiquetas clínicas.
- Control de sesgos por edad, sexo, ubicación, condición socioeconómica o institución médica.
- Definición de responsables sobre el uso de los datos.

Esta etapa es crítica porque un modelo entrenado con datos incorrectos, incompletos o sesgados puede generar predicciones poco confiables.

---

### 3.4 Preparación y transformación de datos

En esta fase los datos se preparan para el entrenamiento.

**Actividades principales:**

- Limpieza de registros duplicados o inconsistentes.
- Tratamiento de valores faltantes.
- Codificación de variables categóricas, por ejemplo síntomas presentes o ausentes.
- Normalización o estandarización de variables numéricas.
- Creación de variables derivadas, como número total de síntomas, severidad acumulada o duración de síntomas.
- Separación de datos en entrenamiento, validación y prueba.
- Manejo del desbalance entre clases.

Para el caso de enfermedades huérfanas, se recomienda evitar dividir los pocos casos de forma inadecuada. La validación debe realizarse con cuidado para no sobreestimar el desempeño del modelo.

---

### 3.5 Desarrollo y entrenamiento del modelo

Se pueden evaluar varios tipos de modelos, empezando por modelos simples e interpretables y avanzando hacia modelos más complejos si el volumen y la calidad de los datos lo permiten.

**Modelos posibles:**

- Regresión logística, como línea base interpretable.
- Árboles de decisión, útiles para explicar reglas clínicas.
- Random Forest o Gradient Boosting, adecuados para datos tabulares.
- Redes neuronales, si existe suficiente volumen de datos.
- Modelos híbridos que combinen reglas clínicas con predicción estadística.
- Modelos de aprendizaje por transferencia para apoyar enfermedades con pocos datos.

**Enfoque recomendado:**

Para este problema se recomienda iniciar con modelos tabulares interpretables, como árboles de decisión, random forest o gradient boosting, porque permiten trabajar con síntomas y variables clínicas estructuradas. En enfermedades huérfanas, se puede complementar con reglas clínicas definidas por expertos y técnicas de balanceo.

---

### 3.6 Validación y pruebas

La validación debe combinar criterios técnicos y clínicos.

**Métricas técnicas:**

- Accuracy, para una visión general del desempeño.
- Recall o sensibilidad, especialmente importante para detectar pacientes enfermos.
- Precision, para controlar falsos positivos.
- F1-score, útil cuando hay desbalance de clases.
- Matriz de confusión, para entender errores por categoría.
- AUC-ROC o AUC-PR, según la distribución de clases.

**Validación clínica:**

- Revisión de resultados por médicos especialistas.
- Análisis de casos mal clasificados.
- Evaluación del impacto de falsos negativos.
- Comparación con criterios clínicos conocidos.
- Pruebas en datos de instituciones diferentes a las usadas en entrenamiento.

Para enfermedades huérfanas, el recall debe ser una métrica prioritaria, porque no detectar un posible caso puede tener un impacto clínico alto.

---

### 3.7 Registro y versionamiento

Una práctica clave de MLOps es mantener trazabilidad completa del modelo.

**Elementos a versionar:**

- Dataset usado para entrenamiento.
- Código fuente.
- Parámetros del modelo.
- Métricas obtenidas.
- Versión del modelo.
- Fecha de entrenamiento.
- Criterios de aprobación.

Esto permite saber qué modelo fue usado, con qué datos fue entrenado y qué desempeño tenía al momento de ser desplegado.

---

### 3.8 Despliegue en producción

El modelo puede exponerse como un servicio para que el médico ingrese los datos del paciente y reciba una respuesta.

**Opciones de despliegue:**

- API REST.
- Aplicación web sencilla.
- Servicio empaquetado en Docker.
- Integración futura con sistemas clínicos.

En este entregable se propone una solución sencilla usando Docker y una API web. El médico puede ejecutar el contenedor localmente, enviar datos del paciente y recibir una clasificación simulada.

---

### 3.9 Monitoreo del modelo

El monitoreo es necesario porque el comportamiento de los datos puede cambiar con el tiempo.

**Aspectos a monitorear:**

- Volumen de predicciones realizadas.
- Distribución de síntomas ingresados.
- Cambios en la frecuencia de cada categoría predicha.
- Tiempo de respuesta del servicio.
- Errores de la API.
- Posible degradación del desempeño del modelo.
- Aparición de nuevos síntomas, enfermedades o patrones clínicos.

También se debe monitorear si el modelo está generando demasiados falsos positivos o falsos negativos cuando se cuente con validación médica posterior.

---

### 3.10 Reentrenamiento y mejora continua

Con el tiempo pueden aparecer nuevos datos clínicos, nuevos casos de enfermedades huérfanas o cambios en los criterios médicos. Por esta razón, el pipeline debe contemplar reentrenamiento.

**Criterios para reentrenar:**

- Se recolecta un volumen suficiente de nuevos datos validados.
- El desempeño del modelo disminuye.
- Se identifican sesgos en las predicciones.
- Se incorporan nuevas variables clínicas.
- Se agregan nuevas enfermedades al alcance.
- Los médicos reportan errores recurrentes.

El reentrenamiento debe pasar nuevamente por validación técnica y clínica antes de liberar una nueva versión.

---

## 4. Resumen ejecutivo de la solución propuesta

El pipeline propuesto cubre el ciclo completo de MLOps: definición del problema, recolección y gobierno de datos, preparación, entrenamiento, validación, despliegue, monitoreo y reentrenamiento. Para enfermedades comunes se aprovecha el alto volumen de datos, mientras que para enfermedades huérfanas se recomienda combinar datos multicéntricos, aprendizaje por transferencia, técnicas de balanceo y validación clínica experta.

La solución debe operar como una herramienta de apoyo al médico, con trazabilidad, monitoreo y mejora continua. Debido a la sensibilidad del contexto clínico, la privacidad, la explicabilidad y el control de falsos negativos son elementos críticos del diseño.
