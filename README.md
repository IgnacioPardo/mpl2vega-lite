# Matplotlib a Vega-Lite

Conversor de gráficos de Matplotlib a especificaciones Vega-Lite, permitiendo una integración seamless con Altair y aplicaciones web.

## Instalación

```bash
pip install -e .
```

## Uso

### Conversión básica

```python
import matplotlib.pyplot as plt
import numpy as np
from mpl2vega.converter import mpl_to_vega

# Crear un gráfico en Matplotlib
fig, ax = plt.subplots()
ax.scatter(np.array([1, 2, 3]), np.array([4, 5, 6]))
ax.set_title('Scatter Plot Example')

# Convertir a Vega-Lite
vega_spec = mpl_to_vega(fig, ax)

# Mostrar el gráfico de Vega-Lite
vega_spec
```

### Guardar la especificación

```python
from mpl2vega.converter import save_vega_spec

# Guardar como JSON
save_vega_spec(vega_spec, 'mi_grafico.json')

# Guardar como HTML
save_vega_spec(vega_spec, 'mi_grafico.html', format='html')
```

## Tipos de gráficos soportados

- Gráficos de dispersión (`scatter`)
- Gráficos de líneas (`line`)
- Gráficos de barras (`bar`)
- Histogramas (`histogram`)

## Conversión a hechos ASP con Draco2

El proyecto ahora soporta la conversión de especificaciones Vega-Lite a hechos ASP (Answer Set Programming) utilizando Draco2:

```python
from draco.fact_utils import dict_to_facts

# Obtener la especificación Vega-Lite
vega_spec = mpl_to_vega(fig, ax)

# Convertir a hechos ASP
facts = dict_to_facts(vega_spec)

# Guardar los hechos ASP en un archivo
with open('mi_grafico.lp', 'w') as f:
    for fact in facts:
        f.write(fact + "\n")
```

## Estructura del proyecto

```
mpl2vega-lite/
├── src/
│   ├── __init__.py
│   ├── converter.py         # Módulo principal
│   ├── plot_detection.py    # Detección del tipo de gráfico
│   ├── data_extraction.py   # Extracción de datos
│   └── vega_conversion.py   # Conversión a Vega-Lite
└── setup.py
```

## Contribuir

Las contribuciones son bienvenidas. Asegúrate de agregar pruebas para cualquier nueva funcionalidad.

## Licencia

Este proyecto está licenciado bajo la Licencia MIT.
