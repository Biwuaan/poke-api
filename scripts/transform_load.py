#Librerias ocupadas
import pandas as pd
from sqlalchemy import create_engine
import ast
import psycopg2

def run():
    try:
        connection = psycopg2.connect(
            database="pokemon_db",
            user="postgres",
            password="1234",
            host="localhost",
            port="5432"
        )
        print("Conexión exitosa")

        cursor = connection.cursor()

        # Resto del código para consultas
    except psycopg2.Error as e:
        print(f"Error de conexión: {e}")

    cursor.execute("SELECT * FROM pokemon")
    resultados = cursor.fetchall()

    columnas = [desc[0] for desc in cursor.description]
    df = pd.DataFrame(resultados, columns=columnas)

    df['height'] = df['height'].astype(int)  
    df['weight'] = df['weight'].astype(int)  
    df['base_experience'] = df['base_experience'].astype(int)
    df['types']= df['types'].apply(ast.literal_eval)
    df['abilities'] = df['abilities'].apply(ast.literal_eval)
    df['hp'] = df['hp'].astype(int)  
    df['attack'] = df['attack'].astype(int)  
    df['defense'] = df['defense'].astype(int)  

    df_fact = df[['id', 'name', 'height', 'weight', 'base_experience']]


    #convirtiendo type a catalogo
    todos_los_tipos = [tipo for sublista in df['types'] for tipo in sublista]
    tipos_unicos = sorted(set(todos_los_tipos))
    catalogo_tipos = [{'id_type': i + 1, 'tipo_name': tipo} for i, tipo in enumerate(tipos_unicos)]
    df_tipos = pd.DataFrame(catalogo_tipos)


    #convirtiendo abilities a catalogo
    todos_las_habilidades = [tipo for sublista in df['abilities'] for tipo in sublista]
    habilidades_unicos = sorted(set(todos_las_habilidades))
    catalogo_habilidades = [{'id_abilities': i + 1, 'tipo_name': tipo} for i, tipo in enumerate(habilidades_unicos)]
    df_habilidades = pd.DataFrame(catalogo_habilidades)

    #creando tabla de habilidades
    df_hab = df[['id', 'abilities']].explode('abilities')
    df_hab = df_hab.rename(columns={'abilities': 'abilitie'})

    #creando tabla de tipos
    df_type = df[['id', 'types']].explode('types')
    df_type = df_type.rename(columns={'types': 'type'})


    usuario = "postgres"         # o el que hayas definido
    password = "1234"  # la que pusiste al instalar PostgreSQL
    host = "localhost"
    puerto = "5432"
    nombre_bd = "pokemon_db"

    #Conexión a la BD
    engine = create_engine(f'postgresql+psycopg2://{usuario}:{password}@{host}:{puerto}/{nombre_bd}')

    df_fact.to_sql('pokemon_silver_fact', engine, if_exists='append', index=False)
    df_tipos.to_sql('pokemon_silver_cat_tipos', engine, if_exists='append', index=False)
    df_habilidades.to_sql('pokemon_silver_cat_habilidades', engine, if_exists='append', index=False)
    df_hab.to_sql('pokemon_silver_habilidades', engine, if_exists='append', index=False)
    df_type.to_sql('pokemon_silver_tipos', engine, if_exists='append', index=False)