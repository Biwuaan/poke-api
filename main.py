# main.py

import os
import sys

# Agregar la carpeta de scripts al path
sys.path.append(os.path.join(os.path.dirname(__file__), 'scripts'))

# Importar tus scripts
from scripts import extraccion as extract
from scripts import transform_load as transform_load

def main():
    print("🔄 Iniciando pipeline ETL de Pokémon...")

    print("\n📥 1. Extracción de datos")
    extract.run()

    print("\n⚙️ 2. Transformación y carga")
    transform_load.run()

    print("\n✅ ETL completado con éxito")

if __name__ == "__main__":
    main()