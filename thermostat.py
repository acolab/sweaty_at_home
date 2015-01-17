from flask import Flask, Response
from flask import request
from flask import abort, redirect, url_for
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, Float, DateTime, Boolean, Time
from sqlalchemy.orm import sessionmaker
import datetime
import time
from flask import render_template
from random import randrange
import os

try:
    import pigpio
    PI = True
except ImportError:
    PI = False

engine = create_engine('sqlite:///thermostat.sqlite', convert_unicode=True, echo=False)
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

class Schedule(Base):
    __tablename__ = 'schedule'

    id = Column(Integer, primary_key=True)
    start_time = Column(Time)
    end_time = Column(Time)
    monday = Column(Boolean, default = False)
    tuesday = Column(Boolean, default = False)
    wednesday = Column(Boolean, default = False)
    thursday = Column(Boolean, default = False)
    friday = Column(Boolean, default = False)
    saturday = Column(Boolean, default = False)
    sunday = Column(Boolean, default = False)


class Settings(Base):
    __tablename__ = 'settings'

    id = Column(Integer, primary_key=True)
    target_temperature = Column(Float)
    spread = Column(Float)

if PI:
    pi = pigpio.pi()

class Heater(Base):
    __tablename__ = 'heaters'
    id = Column(Integer, primary_key=True)
    state = Column(Integer)
    pin = Column(Integer)

    OFF = 0
    ON = 1

    def setup(self):
        if PI:
            pi.set_mode(self.pin, pigpio.OUTPUT)

    def active(self):
        if self.state == Heater.ON:
            return True
        else:
            return False

    def activate(self):
        print "Activating heater"
        if self.state != Heater.ON:
            change = HeaterStateChange(heater_id=self.id, state=Heater.ON, date=datetime.datetime.now())
            db_session.add(change)
        self.state = Heater.ON
        db_session.commit()
        if PI:
            pi.write(self.pin, 1)
            
    def deactivate(self):
        print "Deactivating heater"
        if self.state != Heater.OFF:
            change = HeaterStateChange(heater_id=self.id, state=Heater.OFF, date=datetime.datetime.now())
            db_session.add(change)
        self.state = Heater.OFF
        db_session.commit()
        if PI:
            pi.write(self.pin, 0)

    def hold(self):
        print "Holding heater"


class HeaterStateChange(Base):
	__tablename__ = 'heater_state_changes'
	id = Column(Integer, primary_key=True)
	heater_id = Column(Integer)
	date = Column(DateTime)
	state = Column(Integer)


Base.metadata.create_all(bind=engine)

settings = Settings.query.first()
if settings == None:
    settings = Settings(target_temperature=20, spread=0.5)
    db_session.add(settings)
    db_session.commit()
print repr(settings)

heater = Heater.query.first()
if heater == None:
    heater = Heater(state=Heater.OFF, pin=17)
    db_session.add(heater)
    db_session.commit()
    
app = Flask(__name__)

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
    return "Temperature saved: {temp}".format(temp=temperature.temperature)

@app.route('/set-target')
def set_target():
    settings = Settings.query.first()
    settings.target_temperature = request.args.get("target")
    settings.spread = request.args.get("spread")
    db_session.commit()
    update_thermostat()
    return redirect(url_for('index'))

@app.route('/schedule', methods=['GET' , 'POST'])
def schedule():
    if request.method == 'POST':
        Schedule.query.delete()
        i = 0
        table = []
        while 1:
            line={}
            for item in ["start_time", "end_time", "monday", "tuesday", "wednesday", "thursday", "friday", "saturday", "sunday"]:
                   value = request.form.get(item + "_" + str(i))
                   if value and (item == "start_time" or item == "end_time"):
                       time_struct = time.strptime(value,"%H:%M")
                       line[item]=datetime.time(time_struct.tm_hour, time_struct.tm_min)
                   else:
                       line[item] = value
            if line["start_time"]:
                i += 1
                schedule = Schedule(**line)
                print schedule
                db_session.add(schedule)
                db_session.commit()
            else:
                break
        print repr(table)
    return render_template('schedule.html')

fire = 0
@app.route('/lcd')
def lcd():
    global fire
    temperature = Temperature.query.order_by("date DESC").first()
    if temperature == None:
        return
    settings = Settings.query.first()
    actual = temperature.temperature
    target = settings.target_temperature
    str =  "Actuelle :% 4.1f \xdfC\n" % actual
    str += "Consigne :% 4.1f \xdfC" % settings.target_temperature
    heater = Heater.query.first()
    if heater.active():
        if fire == 0:
            str += " \xc2"
        else:
            str += " \xaf"
        fire = (fire + 1) % 2
    else:
        str += " \x2a"
    return str
    

def root_dir():  # pragma: no cover
    return os.path.abspath(os.path.dirname(__file__))

def get_file(filename):  # pragma: no cover
    try:
        src = os.path.join(root_dir(), filename)
        # Figure out how flask returns static files
        # Tried:
        # - render_template
        # - send_file
        # This should not be so non-obvious
        return open(src).read()
    except IOError as exc:
        return str(exc)

@app.route('/', defaults={'path': ''})
@app.route('/<path:path>')
def get_resource(path):
    mimetypes = {
        ".css": "text/css",
        ".html": "text/html",
        ".js": "application/javascript",
    }
    complete_path = os.path.join(root_dir(), path)
    ext = os.path.splitext(path)[1]
    mimetype = mimetypes.get(ext, "text/html")
    content = get_file(complete_path)
    return Response(content, mimetype=mimetype)

def update_thermostat():
    temperature = Temperature.query.order_by("date DESC").first()
    if temperature == None:
        return
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
