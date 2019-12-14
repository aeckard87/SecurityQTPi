# Simple program to check pins are functioning

import RPi.GPIO as GPIO

# Manually put in GIPO pin # here. # will depend on which GPIO mode you want to use. BCM | BOARD
pins = [2,3]

print('RASPBERRY INFO:')
for key, value in GPIO.RPI_INFO.items():
    print('\t{}: {}'.format(key,value))

print ('RPi.GIPO INFO:')

print ('\tVersion: {}'.format(GPIO.VERSION))

mode = GPIO.getmode()
if mode == None:
    # Mentioned earlier, depending on which MODE you need, set this occordingly
    #GPIO.setmode(GPIO.BOARD)
    GPIO.setmode(GPIO.BCM)
    mode = GPIO.getmode()

print ('\tMODE: {}'.format(mode))

GPIO.setup(pins, GPIO.IN)

print ('PINS')
for pin in pins:
    print ('\t{}: {}'.format(pin, GPIO.gpio_function(pin)))

GPIO.cleanup(pins)
