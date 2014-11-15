from flask import Flask
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, Float, DateTime

engine = create_engine('sqlite:///thermostat.sqlite', echo=True)
Base = declarative_base()

class User(Base):
	__tablename__ = 'temperatures'

	id = Column(Integer, primary_key=True)
	date = Column(DateTime)
	temperature = Column(Float)

	def __repr__(self):
		return "<Temperature(date='%s', temperature='%s'>" % (
                             self.date, self.temperature)

Base.metadata.create_all(engine)

app = Flask(__name__)

@app.route('/')
def hello_world():
    return 'Hello World!'

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)
