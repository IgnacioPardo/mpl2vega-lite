"""
Módulo principal para la conversión de Matplotlib a Vega-Lite

Este módulo proporciona la función principal para convertir gráficos
de Matplotlib a especificaciones Vega-Lite.
"""

import numpy as np
import pandas as pd
import altair as alt
import json
import matplotlib.pyplot as plt

from .plot_detection import detect_plot_type
from .data_extraction import (
    extract_data_from_axes,
    extract_scatter_data,
    extract_line_data,
    extract_bar_data,
    extract_histogram_data,
)
from .vega_conversion import (
    create_vega_lite_spec,
    create_vega_lite_scatter,
    create_vega_lite_line,
    create_vega_lite_bar,
    create_vega_lite_histogram,
)


def mpl_to_vega(fig=None, ax=None, verbose=False):
    """
    Convierte un gráfico de Matplotlib a una especificación Vega-Lite.

    Args:
        fig: Objeto matplotlib.figure.Figure (opcional)
        ax: Objeto matplotlib.axes.Axes (opcional)
        verbose: Si es True, imprime información de depuración

    Returns:
        alt.Chart: Un gráfico de Altair con la especificación Vega-Lite

    Notes:
        Si no se proporciona ax, se usará el axes actual de Matplotlib (plt.gca()).
        Si no se proporciona fig, se usará la figura actual de Matplotlib (plt.gcf()).
    """
    if ax is None:
        ax = plt.gca()

    if fig is None:
        fig = plt.gcf()

    # Detectar el tipo de gráfico
    plot_type = detect_plot_type(ax)

    if verbose:
        print(f"Tipo de gráfico detectado: {plot_type}")

    # Extraer datos según el tipo de gráfico
    data = extract_data_from_axes(ax, plot_type)

    if not data:
        raise ValueError(
            f"No se pudieron extraer datos para el tipo de gráfico: {plot_type}"
        )

    # Crear la especificación Vega-Lite
    chart = create_vega_lite_spec(fig, ax, data, plot_type)

    return chart


def save_vega_spec(chart, filename, format="json"):
    """
    Guarda una especificación Vega-Lite en un archivo.

    Args:
        chart: Un gráfico de Altair
        filename: Nombre del archivo de salida
        format: Formato de salida ('json', 'html')

    Returns:
        str: Ruta al archivo guardado
    """
    if format == "json":
        chart.save(filename)
    elif format == "html":
        chart.save(filename, embed_options={"renderer": "svg"})
    else:
        raise ValueError(f"Formato no soportado: {format}. Use 'json' o 'html'")

    return filename
