import requests
import streamlit as st
import pickle
import pandas as pd

def fetch_poster(movie_id):
    url = f"https://api.themoviedb.org/3/movie/{movie_id}?api_key=efa33feffbd3b0411d09e1ce7ff7bb78&language=en-US"
    try:
        response = requests.get(url)
        response.raise_for_status()  # Raise an error for bad responses
        data = response.json()
        poster_path = data['poster_path']
        full_path = f"https://image.tmdb.org/t/p/w500/{poster_path}"
        return full_path
    except Exception as e:
        print(f"Error fetching poster: {e}")
        return None  # Return None if there's an error

def recommend(movie):
    index = movies[movies['title'] == movie].index[0]
    distances = sorted(list(enumerate(similarity[index])), reverse=True, key=lambda x: x[1])[1:6]
    recommended_movie_names = []
    recommended_movie_posters = []

    for i in distances:
        # Fetch the movie title and poster
        movie_id = movies.iloc[i[0]].movie_id
        recommended_movie_posters.append(fetch_poster(movie_id))
        recommended_movie_names.append(movies.iloc[i[0]].title)

    return recommended_movie_names, recommended_movie_posters

# Load movie data and similarity matrix
movies_dict = pickle.load(open('movies_dict.pkl', 'rb'))
movies = pd.DataFrame(movies_dict)
similarity = pickle.load(open('similarity.pkl', 'rb'))

st.header('Movie Recommendation System')

movie_list = movies['title'].values
selected_movie_name = st.selectbox(
    'Which movie do you like the most',
    movie_list
)

if st.button('Show Recommendations'):
    recommended_movie_names, recommended_movie_posters = recommend(selected_movie_name)

    # Display recommendations in columns
    cols = st.columns(5)  # Create 5 columns
    for i in range(len(recommended_movie_names)):
        with cols[i % 5]:  # Use modulo to cycle through columns
            st.markdown(f"<p style='text-align: center; font-weight: bold;'>{recommended_movie_names[i]}</p>", unsafe_allow_html=True)  # Display movie title
            if recommended_movie_posters[i]:  # Check if poster is fetched successfully
                st.image(recommended_movie_posters[i], width=200)  # Display movie poster
            else:
                st.write("Poster not available")  # Handle missing poster
            st.markdown("<br>", unsafe_allow_html=True)  # Add spacing between posters