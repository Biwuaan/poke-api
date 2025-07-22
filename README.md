# 🧬 PokeStats - ETL de Pokémon con API y PostgreSQL

Este proyecto realiza un pipeline **ETL (Extract, Transform, Load)** utilizando la [PokéAPI](https://pokeapi.co/) como fuente de datos. Extrae información de todos los Pokémon, la transforma en estructuras normalizadas, y la carga en una base de datos PostgreSQL para análisis posterior.

---

## 🚀 Tecnologías utilizadas

- Python 3
- PostgreSQL
- SQLAlchemy
- Pandas
- Requests
- VSCode
- Power BI (para visualización opcional)

---

## 🗂️ Estructura del proyecto

```
poke-stats/
│
├── scripts/                  # Módulos del pipeline
│   ├── extraccion.py         # Extrae datos desde la PokéAPI y los carga en la tabla `pokemon`
│   ├── transform_load.py     # Transforma los datos y crea tablas adicionales como `silver_fact`, `catalogos`
│
├── main.py                   # Orquestador del proceso ETL
├── requirements.txt          # Paquetes necesarios
├── README.md                 # Este archivo
└── dashboards/               # Carpeta sugerida para tus reportes Power BI
```

---

## 🔧 Requisitos

- PostgreSQL instalado y corriendo localmente
- Una base de datos creada llamada `pokemon_db`
- Python 3.x
- Acceso a Internet (para consultar la PokéAPI)

---

## 📦 Instalación

1. Clona este repositorio:
   ```bash
   git clone https://github.com/tu_usuario/poke-stats.git
   cd poke-stats
   ```

2. Instala las dependencias:
   ```bash
   pip install -r requirements.txt
   ```

3. Crea tu base de datos `pokemon_db` en PostgreSQL:
   ```sql
   CREATE DATABASE pokemon_db;
   ```

---

## ⚙️ Configuración de conexión

En los scripts `extraccion.py` y `transform_load.py`, se usan estas credenciales por defecto:

```python
usuario = "postgres"
password = "1234"
host = "localhost"
puerto = "5432"
nombre_bd = "pokemon_db"
```

Modifícalas si tienes una configuración distinta.

---

## ▶️ Ejecución del pipeline

Para correr todo el flujo ETL de forma ordenada:

```bash
python main.py
```

Esto ejecutará:

1. `extraccion.py` → Elimina la tabla `pokemon` y la llena desde la API.
2. `transform_load.py` → Limpia, normaliza y carga los datos en tablas tipo *silver* y catálogos.

---

## 📊 Visualización

Puedes conectar **Power BI** a tu base de datos local `pokemon_db` para analizar:

- Número de Pokémon por tipo
- Fuerza promedio por habilidad
- Estadísticas de HP, defensa y ataque
- Distribución por peso, experiencia base y altura

---

## 📌 Notas

- El script descarga más de 1000 Pokémon. Se hace en bloques de 100 con `sleep()` para evitar sobrecarga a la API.
- Usa `json.dumps()` para guardar listas (`types`, `abilities`) como texto y luego las explota para normalización.
- El flujo está listo para escalar y extenderse a otros endpoints de PokéAPI (evoluciones, especies, etc).

---

## 📍 Por hacer

- Agregar validaciones y control de errores
- Incluir transformaciones adicionales como normalización de nombres
- Agregar visualizaciones en Power BI o Streamlit

---

## 🧑‍💻 Autor

- **@obervizu96** – [GitHub](https://github.com/obervizu96)

---

## 🐍 Licencia

Este proyecto es libre y de código abierto. Úsalo para aprender, practicar o expandir.
