"""
Módulo para detectar el tipo de gráfico de Matplotlib

Este módulo contiene funciones para identificar automáticamente el tipo de gráfico
presente en un objeto Axes de Matplotlib.
"""


def detect_plot_type(ax):
    """
    Detecta el tipo de gráfico en un objeto Axes de Matplotlib.

    Args:
        ax: Un objeto matplotlib.axes.Axes

    Returns:
        str: Una cadena con el tipo de gráfico detectado:
            'scatter': Gráfico de dispersión
            'line': Gráfico de líneas
            'bar': Gráfico de barras
            'histogram': Histograma
            'unknown': Tipo de gráfico no reconocido
    """
    # Verificar en los contenedores si hay algún histograma
    if hasattr(ax, "containers") and ax.containers:
        for container in ax.containers:
            if type(container).__name__ == "BarContainer":
                # Si el contenedor tiene "hist" en la etiqueta o si es un contenedor de barras
                # y las barras tienen anchos similares, es probable que sea un histograma
                if (
                    hasattr(container, "get_label")
                    and "hist" in container.get_label().lower()
                ):
                    return "histogram"

    # Verificar si el método hist se ha llamado (resultado almacenado como _hold_hist)
    for key in dir(ax):
        if key.startswith("_") and "hist" in key.lower():
            return "histogram"

    # Verificar gráficos de dispersión (PathCollection)
    if hasattr(ax, "collections") and ax.collections:
        for collection in ax.collections:
            if type(collection).__name__ == "PathCollection":
                return "scatter"

    # Verificar gráficos de líneas (Line2D)
    if hasattr(ax, "lines") and ax.lines:
        return "line"

    # Verificar gráficos de barras y histogramas (Rectangle patches)
    if hasattr(ax, "patches") and ax.patches:
        if all(type(patch).__name__ == "Rectangle" for patch in ax.patches):
            # Diferenciar entre histogramas y gráficos de barras
            # Los histogramas suelen tener barras de igual anchura y muchos más elementos
            patch_widths = [patch.get_width() for patch in ax.patches]

            # Criterios para identificar un histograma:
            # 1. Muchas barras (> 5)
            # 2. Ancho de barras consistente (pocos valores únicos)
            # 3. Barras adyacentes sin espacios

            if len(patch_widths) > 5:
                unique_widths = len(set(round(w, 5) for w in patch_widths))

                # Si la mayoría de los anchos son iguales (con una pequeña tolerancia)
                if unique_widths <= 3:
                    # Verificar si las barras son adyacentes (criterio adicional para histogramas)
                    x_positions = sorted([patch.get_x() for patch in ax.patches])
                    adjacent = all(
                        abs((x_positions[i + 1] - (x_positions[i] + patch_widths[i])))
                        < 1e-5
                        for i in range(len(x_positions) - 1)
                    )

                    if adjacent:
                        return "histogram"

            # Si no cumple criterios de histograma, es un gráfico de barras
            return "bar"

    # Si no se puede determinar, devolver desconocido
    return "unknown"
