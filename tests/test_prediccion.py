"""Pruebas unitarias para el modelo de predicción médica simulada."""

import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from app.app import predecir_estado


class TestPrediccionResultadoEsperado:
    """Prueba A: Dados parámetros específicos, verificar la categoría esperada."""

    def test_no_enfermo(self):
        resultado = predecir_estado(36.5, 0, 1)
        assert resultado == "NO ENFERMO"

    def test_enfermedad_leve(self):
        resultado = predecir_estado(37.5, 2, 3)
        assert resultado == "ENFERMEDAD LEVE"

    def test_enfermedad_aguda(self):
        resultado = predecir_estado(38.5, 5, 10)
        assert resultado == "ENFERMEDAD AGUDA"

    def test_enfermedad_terminal(self):
        resultado = predecir_estado(40.0, 8, 30)
        assert resultado == "ENFERMEDAD TERMINAL"

    def test_enfermedad_cronica(self):
        resultado = predecir_estado(37.0, 5, 20)
        assert resultado == "ENFERMEDAD CRÓNICA"


class TestCincoCategoriasAlcanzables:
    """Prueba D: Verificar que las 5 categorías de enfermedad son alcanzables."""

    def test_todas_las_categorias_son_obtenidas(self):
        casos = [
            (36.0, 0, 1),  # NO ENFERMO
            (37.5, 2, 4),  # ENFERMEDAD LEVE
            (38.5, 5, 10),  # ENFERMEDAD AGUDA
            (40.0, 8, 25),  # ENFERMEDAD TERMINAL
            (37.0, 5, 20),  # ENFERMEDAD CRÓNICA
        ]

        categorias_esperadas = {
            "NO ENFERMO",
            "ENFERMEDAD LEVE",
            "ENFERMEDAD AGUDA",
            "ENFERMEDAD TERMINAL",
            "ENFERMEDAD CRÓNICA",
        }

        resultados = {predecir_estado(*params) for params in casos}

        assert resultados == categorias_esperadas, (
            f"No se obtuvieron todas las categorías. "
            f"Faltantes: {categorias_esperadas - resultados}"
        )
