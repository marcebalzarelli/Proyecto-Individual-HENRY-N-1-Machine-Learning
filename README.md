# Proyecto de Machine Learning: Sistema de Recomendación de Películas

Este proyecto académico tiene como objetivo desarrollar un sistema de recomendación de películas utilizando técnicas de Machine Learning. A continuación, se detalla el proceso de desarrollo, las funcionalidades implementadas y la estructura del proyecto.

## Descripción general
El sistema de recomendación de películas consta de las siguientes etapas principales:

**1) ETL (Extracción, Transformación y Carga):** en esta etapa se realiza la limpieza de los datos y se aplican las transformaciones necesarias para el procesamiento posterior. Se utilizan técnicas de limpieza, normalización y manipulación de datos.

**2) Funcionalidades implementadas:**

- Cantidad de filmaciones por mes: permite obtener la cantidad de filmaciones registradas para cada mes.

- Cantidad de filmaciones por día: proporciona el número de filmaciones registradas para cada día.

- Score de una filmación: devuelve el puntaje asociado a una película específica.

- Cantidad de votos de una filmación: muestra la cantidad de votos recibidos por una película.

- Obtener actor: permite obtener información sobre un actor en particular.

- Obtener director: proporciona información sobre un director específico.

**3) Análisis Exploratorio de Datos (EDA):** en esta etapa se realiza una exploración de los datos y se analiza la relación entre las variables relevantes. Esto ayuda a comprender mejor los datos y a identificar patrones o tendencias que puedan influir en el modelo de recomendación.

**4) Modelo de recomendación de películas:** En este proyecto, se ha implementado un modelo de recomendación de películas basado en técnicas de Machine Learning. El proceso de recomendación consta de los siguientes pasos:

- Matriz de características: Se ha creado una matriz de características utilizando variables relevantes como géneros, puntaje promedio y elenco de las películas.

- Cálculo de similitud: Utilizando la matriz de características, se ha calculado la similitud del coseno entre las películas. Esto nos permite medir la similitud entre las películas y determinar qué películas son más parecidas entre sí.

- Función de recomendación: Se ha desarrollado una función que toma el título de una película como entrada y devuelve una lista con los títulos de las películas más similares. Esta función utiliza la matriz de similitud y los índices de las películas para identificar las recomendaciones más relevantes.

**5) Función "get" para agregar a las funcionalidades existentes y crear la API:** se implementa una función adicional para obtener recomendaciones de películas basadas en las funcionalidades anteriores. Esto permite obtener recomendaciones personalizadas para un usuario específico.

**6) Despliegue de la API:** la API se despliega en la plataforma Render para que esté accesible y pueda ser utilizada por los usuarios finales.

**7) Framework utilizado:** el desarrollo de la API se lleva a cabo utilizando el framework FastAPI, que ofrece una forma rápida y sencilla de construir servicios web basados en Python.

## Estructura del proyecto
El proyecto está organizado de la siguiente manera:

- **ETL:** carpeta que contiene los scripts y archivos relacionados con el proceso de extracción, transformación y carga de datos.

- **EDA:** carpeta que contiene los notebooks o scripts utilizados para realizar el análisis exploratorio de datos.

- **Modelo:** carpeta que contiene los archivos relacionados con el modelo de recomendación de películas.

- **API:** carpeta que contiene los archivos necesarios para implementar la API utilizando FastAPI.

- **Deploy:** carpeta que contiene los archivos y configuraciones necesarios para el despliegue de la API en Render.

## Requisitos y dependencias
Para ejecutar este proyecto, se requiere tener instaladas las siguientes dependencias:

-Python (versión 3.x)
-Bibliotecas de Python: pandas, numpy, scikit-learn, fastapi, uvicorn

**LINK DE LA API EN RENDER:** https://proyecto-1-henry-api-de-recomendacion.onrender.com/docs

## ¡Hablemos!

¿Tienes alguna pregunta, sugerencia o simplemente quieres decir "Hola"? No dudes en ponerte en contacto conmigo.

- **Responsable del Proyecto:** María Marcela Balzarelli
- **Correo Electrónico:** marcebalzarelli@gmail.com
- **Linkedin:** https://www.linkedin.com/in/marcela-balzarelli/
