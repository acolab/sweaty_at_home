from flask import Flask
from flask import request
from flask import abort, redirect, url_for
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, Float, DateTime
from sqlalchemy.orm import sessionmaker
import datetime
from flask import render_template
import pigpio


engine = create_engine('sqlite:///thermostat.sqlite', convert_unicode=True, echo=True)
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

class Settings(Base):
	__tablename__ = 'settings'

	id = Column(Integer, primary_key=True)
	target_temperature = Column(Float)
	spread = Column(Float)

pi = pigpio.pi()
pi.set_mode(17, pigpio.OUTPUT)

class Heater(Base):
	__tablename__ = 'heaters'
	id = Column(Integer, primary_key=True)
	state = Column(Integer)

	OFF = 0
	ON = 1

	def active(self):
		if self.state == Heater.ON:
			return True
		else:
			return False

	def activate(self):
		print "activating heater"
		self.state = Heater.ON
		db_session.commit()
		pi.write(17, 1)
	
	def deactivate(self):
		print "deactivating heater"
		self.state = Heater.OFF
		db_session.commit()
		pi.write(17, 0)

	def hold(self):
		print "holding heater"

Base.metadata.create_all(bind=engine)

settings = Settings.query.first()
if settings == None:
	settings = Settings(target_temperature=20, spread=0.5)
	db_session.add(settings)
	db_session.commit()
	
heater = Heater.query.first()
if heater == None:
	heater = Heater(state = Heater.OFF)
	db_session.add(heater)
	db_session.commit()
	
print repr(settings)

app = Flask(__name__)

@app.teardown_appcontext
def shutdown_session(exception=None):
    db_session.remove()

@app.route('/')
def index():
	settings = Settings.query.first()
	temperatures = Temperature.query.order_by("date DESC").limit(5).all()
	heater = Heater.query.first()
	return render_template('index.html', temperatures=temperatures, count=len(temperatures), settings=settings, heater=heater)

@app.route('/new-temperature', methods=['POST'])
def new_temperature():
	temperature = Temperature(temperature=request.form["value"], date=datetime.datetime.now())
	db_session.add(temperature)
	db_session.commit()
	update_thermostat()
	return "ok"

@app.route('/set-target')
def set_target():
	settings = Settings.query.first()
	settings.target_temperature = request.args.get("target")
	db_session.commit()
	update_thermostat()
	return redirect(url_for('index'))

def update_thermostat():
	temperature = Temperature.query.order_by("date DESC").first()
	settings = Settings.query.first()
	actual = temperature.temperature
	target = settings.target_temperature
	spread = settings.spread
	heater = Heater.query.first()
	print [actual, target, spread]
	if actual < target - spread:
		heater.activate()
	elif actual > target + spread:
		heater.deactivate()
	else:
		heater.hold()
	

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)
