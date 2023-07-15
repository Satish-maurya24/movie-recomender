import streamlit as st
import pickle
import pandas as pd
import requests
st.title("Movie Recomendation System")

movie_dict = pickle.load(open('movie_dict.pkl','rb'))
movies  = pd.DataFrame(movie_dict)
movie_list = ['hare raam', 'raam raam hare ']

selected_movie_name  = st.selectbox(
'enter the name of the movie',movies['title'].values
)





similarity = pickle.load(open('similarity.pkl' , 'rb'))



def fetch_image(movie_id):

    headers = {
        "accept": "application/json",
        "Authorization": "Bearer eyJhbGciOiJIUzI1NiJ9.eyJhdWQiOiIyYmVkMmM2N2RiZDMxMmQ2OTE3Njc3NjIyYzM2MjlhNSIsInN1YiI6IjY0YjA2NGQ3ZDY1OTBiMDBlNDBiYzczOSIsInNjb3BlcyI6WyJhcGlfcmVhZCJdLCJ2ZXJzaW9uIjoxfQ.s2T7NX3u6eUQw_nsP42UW9notjHVzmnxPlB9f9P1jUg"
    }

    response = requests.get( " https://api.themoviedb.org/3/movie/{}?append_to_response=rwd&language=en-US".format(movie_id), headers=headers)
    data = response.json()

    return "https://image.tmdb.org/t/p/w185/"+ data['poster_path']

def recommend(movie):
    movie_index = movies[movies['title']==movie].index[0]
    distances = similarity[movie_index]
    movies_list = sorted(list(enumerate(distances)),reverse=True , key = lambda x:x[1])[1:6]
    recommend_movie = []
    recommended_movies_poster = []
    for i in movies_list:
        movie_id = movies.iloc[i[0]].id
        recommended_movies_poster.append(fetch_image(movie_id))

        recommend_movie.append(movies.iloc[i[0]].title)
    return recommend_movie,recommended_movies_poster
if st.button('Recommend'):
    names,poster =  recommend(selected_movie_name)
    col1,col2,col3,col4,col5 = st.columns(5)
    with col1:
        st.text(names[0])
        st.image(poster[0])
    with col2:
        st.text(names[1])
        st.image(poster[1])
    with col3:
        st.text(names[2])
        st.image(poster[2])
    with col4:
        st.text(names[3])
        st.image(poster[3])
    with col5:
        st.text(names[4])
        st.image(poster[4])
    # st.image(poster[0])

