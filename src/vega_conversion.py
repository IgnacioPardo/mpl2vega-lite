"""
Módulo para crear especificaciones Vega-Lite a partir de datos extraídos

Este módulo contiene funciones para generar especificaciones Vega-Lite
para diferentes tipos de gráficos utilizando Altair.
"""

import altair as alt


def create_vega_lite_spec(fig, ax, data, plot_type):
    """
    Crea una especificación Vega-Lite a partir de los datos extraídos y el tipo de gráfico.

    Args:
        fig: Objeto matplotlib.figure.Figure
        ax: Objeto matplotlib.axes.Axes
        data: Diccionario con los datos extraídos
        plot_type: Tipo de gráfico a crear ('scatter', 'line', 'bar', 'histogram')

    Returns:
        alt.Chart: Un gráfico de Altair con la especificación Vega-Lite
    """
    if plot_type == "scatter":
        return create_vega_lite_scatter(ax, data)
    elif plot_type == "line":
        return create_vega_lite_line(ax, data)
    elif plot_type == "bar":
        return create_vega_lite_bar(ax, data)
    elif plot_type == "histogram":
        return create_vega_lite_histogram(ax, data)
    else:
        raise ValueError(
            f"No se admite la conversión para el tipo de gráfico: {plot_type}"
        )


def create_vega_lite_scatter(ax, data):
    """
    Crea una especificación Vega-Lite para un gráfico de dispersión.

    Args:
        ax: Objeto matplotlib.axes.Axes
        data: Diccionario con los datos extraídos

    Returns:
        alt.Chart: Un gráfico de dispersión de Altair
    """
    import pandas as pd

    df = pd.DataFrame(data)

    chart = (
        alt.Chart(df)
        .mark_circle()
        .encode(
            x=alt.X("x", title=ax.get_xlabel() or "X"),
            y=alt.Y("y", title=ax.get_ylabel() or "Y"),
            size="size" if "size" in df.columns else alt.value(40),
            color="label",
        )
        .properties(title=ax.get_title(), width=400, height=300)
    )

    return chart


def create_vega_lite_line(ax, data):
    """
    Crea una especificación Vega-Lite para un gráfico de líneas.

    Args:
        ax: Objeto matplotlib.axes.Axes
        data: Diccionario con los datos extraídos

    Returns:
        alt.Chart: Un gráfico de líneas de Altair
    """
    import pandas as pd

    df = pd.DataFrame(data)

    chart = (
        alt.Chart(df)
        .mark_line()
        .encode(
            x=alt.X("x", title=ax.get_xlabel() or "X"),
            y=alt.Y("y", title=ax.get_ylabel() or "Y"),
            color="label",
        )
        .properties(title=ax.get_title(), width=400, height=300)
    )

    return chart


def create_vega_lite_bar(ax, data):
    """
    Crea una especificación Vega-Lite para un gráfico de barras.

    Args:
        ax: Objeto matplotlib.axes.Axes
        data: Diccionario con los datos extraídos

    Returns:
        alt.Chart: Un gráfico de barras de Altair
    """
    import pandas as pd

    df = pd.DataFrame(data)

    chart = (
        alt.Chart(df)
        .mark_bar()
        .encode(
            x=alt.X("x", title=ax.get_xlabel() or "X"),
            y=alt.Y("y", title=ax.get_ylabel() or "Y"),
            color="label",
        )
        .properties(title=ax.get_title(), width=400, height=300)
    )

    return chart


def create_vega_lite_histogram(ax, data):
    """
    Crea una especificación Vega-Lite para un histograma.

    Args:
        ax: Objeto matplotlib.axes.Axes
        data: Diccionario con los datos extraídos

    Returns:
        alt.Chart: Un histograma de Altair
    """
    import pandas as pd

    df = pd.DataFrame(data)

    # Crear un gráfico de barras que represente el histograma
    chart = (
        alt.Chart(df)
        .mark_bar(tooltip=True, opacity=0.7, stroke="black", strokeWidth=0.5)
        .encode(
            x=alt.X(
                "x:Q",
                title=ax.get_xlabel() or "Valores",
                scale=alt.Scale(domain=[df["bin_start"].min(), df["bin_end"].max()]),
                axis=alt.Axis(tickCount=min(20, len(df))),
            ),
            y=alt.Y("y:Q", title=ax.get_ylabel() or "Frecuencia"),
            tooltip=[
                alt.Tooltip("bin_start", title="Inicio", format=".2f"),
                alt.Tooltip("bin_end", title="Fin", format=".2f"),
                alt.Tooltip("count", title="Frecuencia"),
            ],
        )
        .properties(title=ax.get_title() or "Histograma", width=600, height=400)
    )

    return chart
