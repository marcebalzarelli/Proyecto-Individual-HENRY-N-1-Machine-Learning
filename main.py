from fastapi import FastAPI
import pandas as pd
from pandas import read_csv
import csv
from fastapi.openapi.utils import get_openapi
from fastapi.openapi.docs import get_swagger_ui_html
from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from fastapi import FastAPI, HTTPException



app = FastAPI()

# Leo df_final para las primeras funciones
df_final = pd.read_csv('df_final_limpio.csv')

#Leo df_2000 para el modelo de recomendación
df=pd.read_csv('df_2000.csv')
        

@app.get('/cantidad_filmaciones_mes')
def cantidad_filmaciones_mes(Mes: str):
    mes_lower = Mes.lower()   ## para ignorar mayusculas y minusculas
    # Cuento la cantidad de películas estrenadas en el mes
    cantidad = df_final[df_final['Mes'].str.lower() == mes_lower].shape[0]
    return f"{cantidad} cantidad de películas fueron estrenadas en el mes de {Mes}"


@app.get('/cantidad_filmaciones_dia')
def cantidad_filmaciones_dia(Dia: str):
    dia_lower = Dia.lower()  ## para ignorar mayusculas y minusculas
    #Cuento la cantidad de películas estrenadas en el día
    cantidad = df_final[df_final['DiaSemana'].str.lower() == dia_lower].shape[0]
    return f"{cantidad} cantidad de películas fueron estrenadas en los días {Dia}"


@app.get('/score_titulo')
def score_titulo(titulo_de_la_filmación: str):
    titulo_lower = titulo_de_la_filmación.lower() ## para ignorar mayusculas y minusculas
    # Obtengo el título, año de estreno y score
    row = df_final[df_final['title'].str.lower() == titulo_lower].iloc[0]
    titulo = row['title']
    año = row['release_year']
    score = row['popularity']
    return f"La película {titulo} fue estrenada en el año {año} con un score/popularidad de {score}"


@app.get('/votos_titulo')
def votos_titulo(titulo_de_la_filmación: str):
    titulo_lower = titulo_de_la_filmación.lower() ## para ignorar mayusculas y minusculas
    # Obtengo el título, cantidad de votos y valor promedio
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
    # Obtengo el éxito del actor, cantidad de filmaciones y promedio de retorno
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

# Creo la matriz de características y calculo la similitud del coseno
features = ['genres', 'vote_average', 'cast']
df['combined_features'] = df[features].apply(lambda row: ' '.join(row.values.astype(str)), axis=1)
count_matrix = CountVectorizer().fit_transform(df['combined_features'])
cosine_sim = cosine_similarity(count_matrix)

@app.get('/recomendacion/{titulo}')
def get_recomendacion(titulo: str):
    titulo = titulo.lower()

    # Busco la película en el DataFrame
    matches = df[df['title'].str.lower() == titulo]

    if matches.empty:
        raise HTTPException(status_code=404, detail='Película no encontrada')

    idx = matches.index[0]
    sim_scores = list(enumerate(cosine_sim[idx]))
    sim_scores = sorted(sim_scores, key=lambda x: x[1], reverse=True)
    sim_indices = [i[0] for i in sim_scores if i[0] != idx]
    top_movies = df['title'].iloc[sim_indices[:5]].values.tolist()

    return {'recomendacion': top_movies}

# Endpoint para obtener la especificación OpenAPI en formato JSON
@app.get("/openapi.json", include_in_schema=False)
async def get_openapi_endpoint():
    return JSONResponse(get_openapi(title="Documentación de la API", version="1.0.0", routes=app.routes))

# Endpoint para obtener la interfaz Swagger HTML
@app.get("/docs", include_in_schema=False)
async def get_documentation(request: Request):
    openapi_url = app.url_path_for("get_openapi_endpoint")
    return {"openapi_url": openapi_url}

# Ejecuta el servidor Uvicorn
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8001)
