from fastapi import FastAPI
import pandas as pd
from pandas import read_csv
import zipfile

app = FastAPI()

# Ruta del archivo ZIP en el repositorio de GitHub
archivo_zip = 'df_final_limpio.zip'

# Descomprimo el archivo ZIP y cargo el DataFrame CSV
with zipfile.ZipFile(archivo_zip, 'r') as zip_ref:
    with zip_ref.open('df_final_limpio.csv') as csv_file:
        # Lee el archivo CSV y lo carga en un DataFrame
        df_final = pd.read_csv(csv_file)


@app.get('/cantidad_filmaciones_mes')
def cantidad_filmaciones_mes(Mes: str):
    mes_lower = Mes.lower()   ## para ignorar mayusculas y minusculas
    # Contar la cantidad de películas estrenadas en el mes
    cantidad = df_final[df_final['Mes'].str.lower() == mes_lower].shape[0]
    return f"{cantidad} cantidad de películas fueron estrenadas en el mes de {Mes}"


@app.get('/cantidad_filmaciones_dia')
def cantidad_filmaciones_dia(Dia: str):
    dia_lower = Dia.lower()  ## para ignorar mayusculas y minusculas
    #Contar la cantidad de películas estrenadas en el día
    cantidad = df_final[df_final['DiaSemana'].str.lower() == dia_lower].shape[0]
    return f"{cantidad} cantidad de películas fueron estrenadas en los días {Dia}"


@app.get('/score_titulo')
def score_titulo(titulo_de_la_filmación: str):
    titulo_lower = titulo_de_la_filmación.lower() ## para ignorar mayusculas y minusculas
    # Obtener el título, año de estreno y score
    row = df_final[df_final['title'].str.lower() == titulo_lower].iloc[0]
    titulo = row['title']
    año = row['release_year']
    score = row['popularity']
    return f"La película {titulo} fue estrenada en el año {año} con un score/popularidad de {score}"


@app.get('/votos_titulo')
def votos_titulo(titulo_de_la_filmación: str):
    titulo_lower = titulo_de_la_filmación.lower() ## para ignorar mayusculas y minusculas
    # Obtener el título, cantidad de votos y valor promedio
    row = df_final[df_final['title'].str.lower() == titulo_lower].iloc[0]
    titulo = row['title']
    año = row['release_year']
    cantidad_votos = row['vote_count']
    promedio_votos = row['vote_average']

    if cantidad_votos < 2000:
        return "La película no cumple la condición de tener al menos 2000 valoraciones."
    else:
        return f"La película {titulo} fue estrenada en el año {año}. La misma cuenta con un total de {cantidad_votos} valoraciones, con un promedio de {promedio_votos}"


@app.get('/get_actor')
def get_actor(nombre_actor: str):
    nombre_actor_lower = nombre_actor.lower()  ## para ignorar mayusculas y minusculas
    # Relleno los valores NaN en las columnas relevantes con valores adecuados para que no me largue error
    df_final['cast'] = df_final['cast'].fillna('')
    df_final['return'] = df_final['return'].fillna(0)
    # Obtener el éxito del actor, cantidad de filmaciones y promedio de retorno
    actor_data = df_final[df_final['cast'].str.lower().str.contains(nombre_actor_lower, case=False)]
    cantidad_filmaciones = actor_data.shape[0]
    éxito = actor_data['return'].sum()
    promedio_retorno = éxito / cantidad_filmaciones if cantidad_filmaciones > 0 else 0

    return f"El actor {nombre_actor} ha participado de {cantidad_filmaciones} filmaciones. El mismo ha conseguido un retorno de {éxito} con un promedio de {promedio_retorno} por filmación"

@app.get('/get_director')
def get_director(nombre_director: str):
    nombre_director = nombre_director.lower()  ## para ignorar mayusculas y minusculas
    # Relleno los valores NaN en las columnas relevantes con valores adecuados para que no largue error
    df_final['crew'] = df_final['crew'].fillna('')
    df_final['return'] = df_final['return'].fillna(0)
    # Obtener el éxito del director, detalles de las películas, costo y ganancia
    director_data = df_final[df_final['crew'].str.contains(nombre_director, case=False)]
    éxito = director_data['return'].sum()
    peliculas = []

    for _, row in director_data.iterrows():
        titulo = row['title']
        fecha_lanzamiento = row['release_date']
        retorno_individual = row['return']
        costo = row['budget']
        ganancia = row['revenue']
        peliculas.append({
            'Título': titulo,
            'Fecha de lanzamiento': fecha_lanzamiento,
            'Retorno individual': retorno_individual,
            'Costo': costo,
            'Ganancia': ganancia
        })

    return {
        'Éxito': éxito,
        'Películas': peliculas
    }

uvicorn main:app --host 0.0.0.0 --port 10000
