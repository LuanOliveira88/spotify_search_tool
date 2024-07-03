import streamlit as st

from database import Connector

connector = Connector()


@st.cache_data
def get_dataframe(artistName):
	if connector.check_artist(artistName):
		return connector.return_dataframe(artistName)
	connector.insert_artist_results(artistName)
	return connector.return_dataframe(artistName)


st.sidebar.header('Busca')
st.header('Resultados da Busca')
artist_name = st.sidebar.text_input('Nome do Artista')
submit_btn = st.sidebar.button('Submit')
if submit_btn:
	df = get_dataframe(artist_name)
	st.dataframe(df)
