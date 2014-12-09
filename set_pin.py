import pigpio
pi = pigpio.pi()

pin = 17
pi.set_mode(pin, pigpio.OUTPUT)

pi.write(pin, 0)
