# Importamos las bibliotecas necesarias

from fastapi import FastAPI, HTTPException
import uvicorn
import csv
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

app = FastAPI()

# http://127.0.0.1:8000/

# Se carga el archivo CSV una vez

try:
    data = pd.read_csv('dataset/dataset_f1.csv', encoding='utf-8')
except FileNotFoundError:
    raise HTTPException(status_code=500, detail="Archivo CSV no encontrado")

@app.get('/PlayTimeGenre/{genero}')
def PlayTimeGenre(genero):
    # Verificar si el tipo de dato de 'genero' es una cadena (string)
    if not isinstance(genero, str):
        return "El género debe ser una cadena de texto."

    filtro_genero = data[data['genres'] == genero]
    
    if filtro_genero.empty:
        return f"No se encontraron datos para el género {genero}"
    
    max_horas_jugadas = filtro_genero['sum_playtime_forever'].max()
    ano_max_horas_jugadas = filtro_genero[filtro_genero['sum_playtime_forever'] == max_horas_jugadas]['anio_release'].values[0]
    
    return f"Año de lanzamiento con más horas jugadas para Género {genero} : {ano_max_horas_jugadas}"


# Endpoints 2
# Se carga el archivo CSV 
try:
    data_2 = pd.read_csv('dataset/dataset_f2.csv', encoding='utf-8')  
except FileNotFoundError:
    raise HTTPException(status_code=500, detail="Archivo CSV no encontrado")

@app.get('/UserForGenre/{genero}')
def UserForGenre(genero: str):
    # Filtra el DataFrame por el género deseado
    df_genero = data_2[data_2['genres'] == genero]

    if df_genero.empty:
        return "No se encontraron datos para el género especificado."

    # Calcula la acumulación de horas jugadas por año
    horas_por_anio = df_genero.groupby('anio_posted')['sum_playtime_forever'].sum().reset_index()
    horas_por_anio = horas_por_anio.rename(columns={'anio_posted': 'Año', 'sum_playtime_forever': 'Horas'})
    lista_horas_por_anio = horas_por_anio.to_dict(orient='records')

    # Encuentra al usuario con más horas jugadas para el género dado
    usuario_max_horas = df_genero.groupby('user_id')['sum_playtime_forever'].sum().idxmax()

    # Crea el diccionario de retorno directamente en el formato requerido
    resultado = {
        "Usuario con más horas jugadas para " + genero: usuario_max_horas,
        "Horas jugadas": lista_horas_por_anio
    }

    return resultado

# Endpoints 3
# Se carga el archivo CSV 
try:
    data_3 = pd.read_csv('dataset/dataset_f34.csv', encoding='utf-8')  
except FileNotFoundError:
    raise HTTPException(status_code=500, detail="Archivo CSV no encontrado")


@app.get('/UsersRecommend/{year}')
def UsersRecommend(year: int):
    # Verificar si el año es igual a -1 y mostrar un mensaje personalizado
    if year == -1:
        return "El año ingresado es -1, lo cual no es válido."

    # Verificar que el año sea un número entero
    if not isinstance(year, int):
        return "El año debe ser un número entero."

    # Verificar que el año ingresado esté en la columna 'anio_posted'
    if year not in data_3['anio_posted'].unique():
        return "El año no se encuentra en la columna 'anio_posted'."

    # Filtrar el dataset para obtener solo las filas correspondientes al año dado
    juegos_del_año = data_3[data_3['anio_posted'] == year]

    # Calcular la cantidad de recomendaciones para cada juego
    recomendaciones_por_juego = juegos_del_año.groupby('app_name')['recommend'].sum().reset_index()

    # Ordenar los juegos por la cantidad de recomendaciones en orden descendente
    juegos_ordenados = recomendaciones_por_juego.sort_values(by='recommend', ascending=False)

    # Tomar los tres juegos más recomendados
    top_3_juegos = juegos_ordenados.head(3)

    # Crear la lista de resultados en el formato deseado
    resultados = [{"Puesto 1": top_3_juegos.iloc[0]['app_name']},
                 {"Puesto 2": top_3_juegos.iloc[1]['app_name']},
                 {"Puesto 3": top_3_juegos.iloc[2]['app_name']}]

    return resultados


# Endpoints 4
# Se carga el archivo CSV 
try:
    data_3 = pd.read_csv('dataset/dataset_f34.csv', encoding='utf-8')  
except FileNotFoundError:
    raise HTTPException(status_code=500, detail="Archivo CSV no encontrado")


@app.get('/UsersNotRecommend/{year}')
def UsersNotRecommend(year: int):
    # Verificar si el año es igual a -1 y mostrar un mensaje personalizado
    if year == -1:
        return "El año ingresado es -1, lo cual no es válido."

    # Verificar que el año sea un número entero
    if not isinstance(year, int):
        return "El año debe ser un número entero."

    # Verificar que el año ingresado esté en la columna 'anio_posted'
    if year not in data_3['anio_posted'].unique():
        return "El año no se encuentra en la columna 'anio_posted'."

    # Filtrar el dataset para obtener solo las filas correspondientes al año dado
    juegos_del_año = data_3[data_3['anio_posted'] == year]

    # Filtrar los juegos menos recomendados (reviews.recommend = False)
    juegos_no_recomendados = juegos_del_año[juegos_del_año['recommend'] == False]

    # Contar la cantidad de veces que cada juego recibió recomendaciones negativas
    juegos_contados = juegos_no_recomendados['app_name'].value_counts().reset_index()
    juegos_contados.columns = ['app_name', 'count']

    # Ordenar los juegos por la cantidad de recomendaciones negativas en orden descendente
    juegos_ordenados = juegos_contados.sort_values(by='count', ascending=False)

    # Tomar los tres juegos menos recomendados
    top_3_juegos = juegos_ordenados.head(3)

    # Crear la lista de resultados en el formato deseado
    resultados = [{"Puesto 1": top_3_juegos.iloc[0]['app_name']},
                 {"Puesto 2": top_3_juegos.iloc[1]['app_name']},
                 {"Puesto 3": top_3_juegos.iloc[2]['app_name']}]

    return resultados


# Endpoints 5
# Se carga el archivo CSV 
try:
    data_5 = pd.read_csv('dataset/dataset_f5.csv', encoding='utf-8')
except FileNotFoundError:
    raise HTTPException(status_code=500, detail="Archivo CSV no encontrado")


@app.get('/sentiment_analysis/{year}')
def sentiment_analysis(year: int):
    # Verifica si el año es un entero positivo
    if not isinstance(year, int) or year < 0:
        raise ValueError("El año debe ser un entero positivo")

    # Verifica si el año se encuentra en la columna 'anio_release'
    if year not in data_5['anio_release'].unique():
        raise ValueError(f"No se encontraron registros para el año {year}")

    # Filtra las filas del DataFrame para el año dado
    df_filtered = data_5[data_5['anio_release'] == year]

    # Cuenta la cantidad de registros para cada categoría de sentimiento
    sentiment_counts = df_filtered['sentiment_analysis'].value_counts()

    # Convierte el resultado en un diccionario
    result = {
    'Negative': int(sentiment_counts.get(0, 0)),
    'Neutral': int(sentiment_counts.get(1, 0)),
    'Positive': int(sentiment_counts.get(2, 0))
}

    return result


# Modelo de Machine LEarning:

# Cargar la base de datos
df = pd.read_csv('dataset/modelo.csv', encoding='utf-8')

# Crear un vectorizador TF-IDF para convertir títulos en vectores numéricos
# Crear una matriz TF-IDF para representar los juegos
tfidf_vectorizer = TfidfVectorizer()
tfidf_matrix = tfidf_vectorizer.fit_transform(df['title'] + ' ' + df['tags'] + ' ' + df['genres'])

# Calcular la similitud de coseno entre los juegos
cosine_sim = cosine_similarity(tfidf_matrix, tfidf_matrix)


# Función definida para el sistema de recomendación item-item:
def recomendacion_juego(title, num_recommendations=5):
    # Comprobar si 'title' es una cadena
    if not isinstance(title, str):
        return "El título debe ser una cadena."

    # Comprobar si 'title' existe en la lista de títulos
    if title not in df['title'].values:
        return "El título proporcionado no se encuentra en la lista de títulos."

    idx = df[df['title'] == title].index[0]
    sim_scores = list(enumerate(cosine_sim[idx]))
    sim_scores = sorted(sim_scores, key=lambda x: x[1], reverse=True)
    num_recommendations = int(num_recommendations)
    sim_scores = sim_scores[1:num_recommendations+1]  
    game_indices = [i[0] for i in sim_scores]
    return df['title'].iloc[game_indices].tolist()  

# Función definida para el sistema de recomendación user-item:
def recomendacion_usuario(user_id, num_recommendations=5):
    # Verificar si 'user_id' es una cadena
    if not isinstance(user_id, str):
        return "El ID de usuario debe ser una cadena."

    # Filtrar el DataFrame para obtener los juegos que le gustan al usuario
    user_likes = df[df['user_id'] == user_id]
    
    if user_likes.empty:
        return "No se encontraron juegos que le gusten al usuario."

    # Calcular el promedio de las puntuaciones de similitud para los juegos que le gustan al usuario
    avg_similarity_scores = cosine_sim[user_likes.index].mean(axis=0)

    # Obtener los índices de los juegos recomendados ordenados por similitud
    game_indices = avg_similarity_scores.argsort()[::-1]

    # Excluir los juegos que ya le gustan al usuario
    recommended_games = [game for game in game_indices if game not in user_likes.index]

    # Tomar los primeros 'num_recommendations' juegos recomendados
    recommended_games = recommended_games[:num_recommendations]

    # Obtener los títulos de los juegos recomendados
    recommended_titles = df.iloc[recommended_games]['title'].tolist()

    return recommended_titles


#Respuesta del sistema de recomendación item-item
@app.get("/recomendar_juegos/{title}")
async def recomendaciones(title: str):
    num_recommendations = 5  # Puedes ajustar este valor según tus necesidades
    recomendaciones = recomendacion_juego(title, num_recommendations)
    
    if isinstance(recomendaciones, list):
        return {"recommended_users": recomendaciones}
    else:
        raise HTTPException(status_code=404, detail=recomendaciones)

@app.post("/recomendar_juegos/{title}")
async def actualizar_recomendaciones(user_id: str):
    num_recommendations = 5  # Puedes ajustar este valor según tus necesidades
    recomendaciones = recomendacion_usuario(user_id, num_recommendations)
    
    if isinstance(recomendaciones, list):
        return {"recommended_users": recomendaciones}
    else:
        raise HTTPException(status_code=404, detail=recomendaciones)





@app.get("/recomendar_usuario/{user_id}")
async def obtener_recomendaciones(user_id: str):
    num_recommendations = 5  # Puedes ajustar este valor según tus necesidades
    recomendaciones = recomendacion_usuario(user_id, num_recommendations)
    
    if isinstance(recomendaciones, list):
        return {"recommended_games": recomendaciones}
    else:
        raise HTTPException(status_code=404, detail=recomendaciones)

@app.post("/recomendar_usuario/{user_id}")
async def actualizar_recomendaciones(user_id: str):
    num_recommendations = 5  # Puedes ajustar este valor según tus necesidades
    recomendaciones = recomendacion_usuario(user_id, num_recommendations)
    
    if isinstance(recomendaciones, list):
        return {"recommended_games": recomendaciones}
    else:
        raise HTTPException(status_code=404, detail=recomendaciones)