import pickle
import streamlit as st
import requests

st.header('Movie Recommender System', divider='rainbow')

def fetch_poster(movie_id):
    url = "https://api.themoviedb.org/3/movie/{}?api_key=8265bd1679663a7ea12ac168da84d2e8&language=en-US".format(movie_id)
    data = requests.get(url)
    data = data.json()
    poster_path = data['poster_path']
    full_path = "https://image.tmdb.org/t/p/w500/" + poster_path
    return full_path

def recommend(movie):
    index = movies[movies['title'] == movie].index[0]
    distances = sorted(list(enumerate(similarity[index])), reverse=True, key=lambda x: x[1])
    recommended_movie_names = []
    recommended_movie_posters = []
    for i in distances[1:11]:
        movie_id = movies.iloc[i[0]].movie_id
        recommended_movie_posters.append(fetch_poster(movie_id))
        recommended_movie_names.append(movies.iloc[i[0]].title)

    return recommended_movie_names, recommended_movie_posters

# Initialize session state
if 'displayed_count' not in st.session_state:
    st.session_state.displayed_count = 5


movies = pickle.load(open(r'C:\Users\SEN\stramlit\movie_list.pkl', 'rb'))
similarity = pickle.load(open(r'C:\Users\SEN\stramlit\similarity.pkl', 'rb'))

movie_list = movies['title'].values
selected_movie = st.selectbox("Type or select a movie from the dropdown", movie_list)

if st.button('Show Recommendation'):
    recommended_movie_names, recommended_movie_posters = recommend(selected_movie)
    st.write(len(recommended_movie_names))
    
    # Create two columns for displaying images
    col1, col2 = st.columns(2)

    for i in range(min(st.session_state.displayed_count, 6)):  # Display up to 6 recommendations
        with col1 if i < 3 else col2:  # Split into two columns
            st.text(recommended_movie_names[i])
            st.image(recommended_movie_posters[i])




footer="""<style>
a:link , a:visited{
color: blue;
background-color: transparent;
text-decoration: underline;
}

a:hover,  a:active {
color: red;
background-color: transparent;
text-decoration: underline;
}

.footer {
position: fixed;
left: 0;
bottom: 0;
width: 100%;
background-color: white;
color: black;
text-align: center;
}
</style>
<div class="footer">
<p>Developed with ❤ by <a style='display: block; text-align: center;' href="https://github.com/" target="_blank">Rohit sen </a></p>
</div>
"""
st.markdown(footer,unsafe_allow_html=True)