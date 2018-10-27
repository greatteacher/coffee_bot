from sqlalchemy import create_engine, Column, Integer, String, Float
from sqlalchemy import Text, DateTime, ForeignKey
from sqlalchemy.orm import relationship, scoped_session, sessionmaker
from sqlalchemy.ext.declarative import declarative_base


engine = create_engine('sqlite:///drinksAndSweets.sqlite')

db_session = scoped_session(sessionmaker(bind=engine))

Base = declarative_base()
Base.query = db_session.query_property()


class Items (Base):
	__tablename__ = 'cafe_menu'
	id = Column(Integer, primary_key=True)
	items_name = Column(String(50), unique=True)
	price = Column(Float)
	description = Column(String(50))
	appointment = Column(String(50))
	posts = relationship('Sweets', backref='author')
	

	def __init__(self, items_name=None, price=None, description=None, appointment=None ):
		self.items_name = items_name 
		self.price = price
		self.description = description
		self.appointment = appointment

	def __repr__(self):
		return '<Our main menu {} {} {}>'.format(self.items_name, self.price, self.description, self.appointment)


class Sweets(Base):
	__tablename__ = 'sweet_bar'
	id = Column(Integer, primary_key=True)
	items_name = Column(String(50))
	day_week = Column(String, unique=True)  # исправить на DateTime бы
	sweets_id = Column(Integer, ForeignKey('cafe_menu.id'))	

	def __init__(self, items_name=None, day_week=None, sweets_id=None):
		self.items_name = items_name 
		self.day_week = day_week
		self.sweets_id = sweets_id

	def __repr__(self):
		return '<Our sweets are {} {} {}>'.format(self.items_name, self.day_week, self.sweets_id)


if __name__ == "__main__":
	Base.metadata.create_all(bind=engine)










