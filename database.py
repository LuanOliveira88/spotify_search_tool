from os import getenv

from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy import Column, Integer, String, UniqueConstraint
from sqlalchemy.orm import sessionmaker, declarative_base
import pandas as pd

from scripts import scrape_artist_tracks

Base = declarative_base()
load_dotenv()


class SearchResult(Base):
	__tablename__ = "search_results"
	id = Column(Integer, primary_key=True, index=True)
	artist_name = Column(String, index=True, nullable=False)
	album_name = Column(String, index=True, nullable=False)
	track_name = Column(String, index=True, nullable=False)
	__table_args__ = (UniqueConstraint('artist_name', 'album_name', 'track_name', name='_artist_album_track_uc'),)


class Connector:
	def __init__(self):
		self.engine = create_engine(getenv("DATABASE_URL"))
		Base.metadata.create_all(bind=self.engine)
		self.SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=self.engine)

	def insert_data(self, data: dict):
		session = self.SessionLocal()
		try:
			existing_result = session.query(SearchResult).filter_by(
				artist_name=data['artist_name'],
				album_name=data['album_name'],
				track_name=data['track_name']
			).first()
			if existing_result:
				print("Registro duplicado encontrado. Nenhuma ação tomada.")
			else:
				new_result = SearchResult(
					artist_name=data['artist_name'],
					album_name=data['album_name'],
					track_name=data['track_name'],
				)
				session.add(new_result)
				session.commit()
		except Exception as err:
			print("Erro:", err)
		finally:
			session.close()

	def check_artist(self, artist_name):
		session = self.SessionLocal()
		try:
			res = session.query(
				session.query(SearchResult).filter(SearchResult.artist_name == artist_name).exists()).scalar()
			return res
		except Exception as err:
			print("Erro", err)

	def insert_artist_results(self, artist_name):
		session = self.SessionLocal()
		if not self.check_artist(artist_name):
			...
		return

	def save_artist_data(self, artist_name):
		for data in scrape_artist_tracks(artist_name):
			self.insert_data(data)

	def return_dataframe(self, artist_name):
		if not self.check_artist(artist_name):
			self.save_artist_data(artist_name)
		query = f"SELECT * FROM search_results WHERE artist_name = '{artist_name}';"
		return pd.read_sql(query, self.engine)

	def return_dataframe_from_all(self):
		query = "SELECT * FROM search_results"
		return pd.read_sql(query, self.engine)



