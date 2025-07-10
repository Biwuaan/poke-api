#Librerias ocupadas
from sqlalchemy import create_engine, text
from time import sleep
import pandas as pd
import requests
import time
import json

#Creacion de listas que se usan para los manejar JSON
tipos_list = []
habilidades_list = []
lista_poke = []

#Credenciales para conectarnos a la BD
usuario = "postgres"         # o el que hayas definido
password = "1234"  # la que pusiste al instalar PostgreSQL
host = "localhost"
puerto = "5432"
nombre_bd = "pokemon_db"

#Conexión a la BD
engine = create_engine(f'postgresql+psycopg2://{usuario}:{password}@{host}:{puerto}/{nombre_bd}')

#Drop a la tabla ya que si se corre sera para actualizarla toda
with engine.connect() as conn:
    conn.execute(text("DROP TABLE IF EXISTS pokemon"))
    conn.commit()  # <-- esto es lo que probablemente faltaba

#Respuesta de API para encontrar el total de pokemons
resp = requests.get('https://pokeapi.co/api/v2/pokemon')
data = resp.json()
total_pokemons = data['count']


#Se crea la funcion para extraer los datos de pokemons
def extrae_pokemons(id):
    try:
        resp = requests.get(f'https://pokeapi.co/api/v2/pokemon/{id}')
        time.sleep(0.5)
        if resp.status_code != 200:
            print(f"Fallo en el id {id}")
            return None
        data = resp.json()

         # Stats como diccionario
        stats = {s["stat"]["name"]: s["base_stat"] for s in data["stats"]}

        # Tipos y habilidades como listas
        tipos = [t["type"]["name"] for t in data["types"]]
        habilidades = [a["ability"]["name"] for a in data["abilities"]]

        # También llenamos las tablas relacionales si las vas a usar luego
        for t in tipos:
            tipos_list.append({"pokemon_id": data["id"], "tipo": t})
        for h in habilidades:
            habilidades_list.append({"pokemon_id": data["id"], "habilidad": h})

        return{
            "id": data["id"],
            "name": data["name"],
            "height": data["height"],
            "weight": data["weight"],
            "base_experience": data["base_experience"],
            "types": json.dumps(tipos),       # Guardado como texto
            "abilities": json.dumps(habilidades),
            "hp": stats.get("hp"),
            "attack": stats.get("attack"),
            "defense": stats.get("defense")
        }
    except Exception as e:
        print(f"error con id{id}: {e}")
        return None
    

#loop para insertarlos
for i in range(1, total_pokemons, 100):
    grupo = list(range(i, min(i + 100, total_pokemons)))

    for poke_id in grupo:
        info = extrae_pokemons(poke_id)  # <--- aquí defines `info`
        if info:                         # <--- validas que no sea None
            lista_poke.append(info)

    df = pd.DataFrame(lista_poke)
    df.to_sql('pokemon', engine, if_exists='append', index=False)
    sleep(1)