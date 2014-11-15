from flask import Flask
from flask import request
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, Float, DateTime
from sqlalchemy.orm import sessionmaker
import datetime

engine = create_engine('sqlite:///thermostat.sqlite', echo=True)
Base = declarative_base()

class Temperature(Base):
	__tablename__ = 'temperatures'

	id = Column(Integer, primary_key=True)
	date = Column(DateTime)
	temperature = Column(Float)

	def __repr__(self):
		return "<Temperature(date='%s', temperature='%s'>" % (
                             self.date, self.temperature)

Base.metadata.create_all(engine)

Session = sessionmaker(bind=engine)
session = Session()

app = Flask(__name__)

@app.route('/')
def hello_world():
    return 'Hello World!'

@app.route('/new-temperature')
def new_temperature():
	temperature = Temperature(temperature=request.args.get("value"), date=datetime.datetime.now())
	session.add(temperature)
	session.commit()
	return temperatre.id

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)
