#!/bin/zsh
set -e

echo "=== Configurando entorno para Draco ==="
echo "Creando un entorno conda para Draco con Python 3.11..."

# Crear el entorno si no existe
if conda env list | grep -q "draco-env"; then
    echo "El entorno draco-env ya existe"
else
    conda create -y -n draco-env python=3.11
    echo "Entorno draco-env creado con Python 3.11"
fi

# Activar el entorno
echo "Activando el entorno draco-env..."
source $(conda info --base)/etc/profile.d/conda.sh
conda activate draco-env

# Instalar draco directamente desde el repositorio de GitHub
echo "Clonando e instalando draco desde GitHub..."
cd /tmp
# Si el directorio ya existe, eliminarlo para evitar conflictos
if [ -d "draco2" ]; then
    echo "Eliminando directorio draco2 existente..."
    rm -rf draco2
fi
git clone https://github.com/cmudig/draco2.git
cd draco2
pip install -e .
cd -

# Verificar la instalación
echo "Verificando la instalación de draco..."
python -c "import draco; print(f'Draco {draco.__version__} se ha instalado correctamente')"

# Instalar otras dependencias del proyecto
echo "Instalando otras dependencias del proyecto..."
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
if [ -f "$SCRIPT_DIR/requirements.txt" ]; then
    pip install -r "$SCRIPT_DIR/requirements.txt"
else
    echo "No se encontró el archivo requirements.txt en $SCRIPT_DIR"
fi

echo "=== Configuración completada ==="
echo ""
echo "Para usar este entorno en el notebook:"
echo "1. Ejecuta: conda activate draco-env"
echo "2. Inicia Jupyter Notebook/Lab dentro del entorno activado"
echo "3. En el notebook, asegúrate de elegir el kernel 'draco-env'"
echo ""
echo "Para salir del entorno ejecuta: conda deactivate"
