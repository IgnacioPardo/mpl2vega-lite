"""
Módulo para extraer datos de gráficos de Matplotlib

Este módulo contiene funciones para extraer datos de diferentes tipos de gráficos
de Matplotlib y convertirlos en formatos compatibles con Vega-Lite.
"""


def extract_data_from_axes(ax, plot_type):
    """
    Extrae los datos relevantes de un objeto Axes según el tipo de gráfico.

    Args:
        ax: Un objeto matplotlib.axes.Axes
        plot_type: El tipo de gráfico ('scatter', 'line', 'bar', 'histogram')

    Returns:
        dict: Un diccionario con los datos extraídos
    """
    data = {}

    if plot_type == "scatter":
        data = extract_scatter_data(ax)
    elif plot_type == "line":
        data = extract_line_data(ax)
    elif plot_type == "bar":
        data = extract_bar_data(ax)
    elif plot_type == "histogram":
        data = extract_histogram_data(ax)

    return data


def extract_scatter_data(ax):
    """
    Extrae datos de un gráfico de dispersión.

    Args:
        ax: Un objeto matplotlib.axes.Axes

    Returns:
        dict: Un diccionario con los datos extraídos
    """
    data = {}

    if hasattr(ax, "collections") and ax.collections:
        for i, collection in enumerate(ax.collections):
            if type(collection).__name__ == "PathCollection":
                # Extraer coordenadas x, y
                offsets = collection.get_offsets()
                x_data = offsets[:, 0]
                y_data = offsets[:, 1]

                # Extraer tamaños si están disponibles
                sizes = collection.get_sizes()
                if len(sizes) == 1 and len(x_data) > 1:
                    sizes = [sizes[0]] * len(x_data)

                # Extraer colores si están disponibles
                colors = collection.get_facecolors()
                if len(colors) == 1 and len(x_data) > 1:
                    colors = [colors[0]] * len(x_data)

                # Crear etiqueta
                label = collection.get_label() or f"series_{i}"
                labels = [label] * len(x_data)

                # Guardar datos
                data.setdefault("x", []).extend(x_data)
                data.setdefault("y", []).extend(y_data)
                data.setdefault("size", []).extend(sizes)
                data.setdefault("label", []).extend(labels)

    return data


def extract_line_data(ax):
    """
    Extrae datos de un gráfico de líneas.

    Args:
        ax: Un objeto matplotlib.axes.Axes

    Returns:
        dict: Un diccionario con los datos extraídos
    """
    data = {}

    if hasattr(ax, "lines") and ax.lines:
        for i, line in enumerate(ax.lines):
            x_data = line.get_xdata()
            y_data = line.get_ydata()
            label = line.get_label() or f"series_{i}"
            labels = [label] * len(x_data)

            # Guardar datos
            data.setdefault("x", []).extend(x_data)
            data.setdefault("y", []).extend(y_data)
            data.setdefault("label", []).extend(labels)

    return data


def extract_bar_data(ax):
    """
    Extrae datos de un gráfico de barras.

    Args:
        ax: Un objeto matplotlib.axes.Axes

    Returns:
        dict: Un diccionario con los datos extraídos
    """
    data = {}

    if hasattr(ax, "patches") and ax.patches:
        x_data = []
        y_data = []
        width_data = []
        height_data = []

        for patch in ax.patches:
            # Para gráficos de barras, extraer posición x, altura y, ancho
            x = patch.get_x()
            y = patch.get_y()
            width = patch.get_width()
            height = patch.get_height()

            x_data.append(x + width / 2)  # Centro de la barra
            y_data.append(height)
            width_data.append(width)
            height_data.append(height)

        # Guardar datos
        data["x"] = x_data
        data["y"] = y_data
        data["width"] = width_data
        data["height"] = height_data
        data["label"] = ["bars"] * len(x_data)

    return data


def extract_histogram_data(ax):
    """
    Extrae los datos de un histograma de Matplotlib de forma más robusta.

    Args:
        ax: Un objeto matplotlib.axes.Axes

    Returns:
        dict: Un diccionario con los datos extraídos
    """
    data = {}

    # Método 1: Intentar obtener los datos directamente de la salida de hist
    # La función hist() devuelve (n, bins, patches)
    hist_data = None

    # Buscar si tenemos acceso a la tupla de retorno de hist()
    for key in dir(ax):
        if key.startswith("_") and "hist" in key.lower():
            hist_data = getattr(ax, key, None)
            if hist_data and isinstance(hist_data, tuple) and len(hist_data) >= 2:
                # Encontramos los datos del histograma
                hist_counts = hist_data[0]
                hist_bins = hist_data[1]

                # Calcular centros de los bins
                bin_centers = [
                    (hist_bins[i] + hist_bins[i + 1]) / 2
                    for i in range(len(hist_bins) - 1)
                ]

                # Crear datos para DataFrame
                data["bin_start"] = hist_bins[:-1]
                data["bin_end"] = hist_bins[1:]
                data["bin_width"] = [
                    hist_bins[i + 1] - hist_bins[i] for i in range(len(hist_bins) - 1)
                ]
                data["x"] = bin_centers
                data["y"] = hist_counts
                data["count"] = hist_counts
                data["density"] = (
                    hist_counts / sum(hist_counts)
                    if sum(hist_counts) > 0
                    else hist_counts
                )
                data["label"] = ["histogram"] * len(hist_counts)
                return data

    # Método 2: Si no encontramos los datos directamente, extraerlos de los patches
    if not data and hasattr(ax, "patches") and ax.patches:
        edges = []  # Almacena los bordes de los bins
        heights = []  # Almacena las alturas

        # Ordenar los parches por posición x para asegurarnos de que están en orden
        patches = sorted(ax.patches, key=lambda p: p.get_x())

        for patch in patches:
            x = patch.get_x()
            width = patch.get_width()
            height = patch.get_height()

            # Guardar el borde izquierdo y la altura
            edges.append(x)
            heights.append(height)

            # Para el último bin, también necesitamos el borde derecho
            if len(edges) == len(patches):
                edges.append(x + width)

        # Crear valores x para representar el centro de cada bin
        bin_centers = [(edges[i] + edges[i + 1]) / 2 for i in range(len(edges) - 1)]

        # Guardar datos
        data["bin_start"] = edges[:-1]
        data["bin_end"] = edges[1:]
        data["bin_width"] = [edges[i + 1] - edges[i] for i in range(len(edges) - 1)]
        data["x"] = bin_centers
        data["y"] = heights
        data["count"] = heights
        data["density"] = [h / sum(heights) if sum(heights) > 0 else h for h in heights]
        data["label"] = ["histogram"] * len(heights)

    return data
