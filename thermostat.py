from flask import Flask
from flask import request
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, Float, DateTime
from sqlalchemy.orm import sessionmaker
import datetime
from flask import render_template


engine = create_engine('sqlite:///thermostat.sqlite', convert_unicode=True)
db_session = scoped_session(sessionmaker(autocommit=False,
                                         autoflush=False,
                                         bind=engine))
Base = declarative_base()
Base.query = db_session.query_property()

class Temperature(Base):
	__tablename__ = 'temperatures'

	id = Column(Integer, primary_key=True)
	date = Column(DateTime)
	temperature = Column(Float)

	def __repr__(self):
		return "<Temperature(date='%s', temperature='%s'>" % (
                             self.date, self.temperature)

Base.metadata.create_all(bind=engine)

app = Flask(__name__)

@app.teardown_appcontext
def shutdown_session(exception=None):
    db_session.remove()

@app.route('/')
def hello_world():
	temperatures = Temperature.query.all()
	return render_template('index.html', temperatures=temperatures)

@app.route('/new-temperature')
def new_temperature():
	temperature = Temperature(temperature=request.args.get("value"), date=datetime.datetime.now())
	db_session.add(temperature)
	db_session.commit()
	return str(temperature.id)

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)
