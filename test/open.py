# Simple program that watches for state changes on given pins, press ctrl+c to exit program
# USES GPIO MODE BOARD!!!

import RPi.GPIO as GPIO

#HANDLE EVENT
def my_callback(channel):
    if GPIO.input(channel):
        print ("{} closed!".format(locations.get(channel, "none")))
    else:
        print ("{} opened!".format(locations.get(channel, "none")))

# INIT VALUES
# channel list gives us proper int array list for GPIO.setup as locations is a dictionary that GPIO.setup cannot ingest.
chan_list = []
# Set pin number : "Description"
# if more than one pin put a comma on the second to last item as shown below.
locations = {
		13 : "Living Room Zone",
		15 : "DownStairs Zone"
	}

# Setting only int values to channel list in preperation for GPIO.setup
for key, value in locations.items():
    chan_list.append(key)


#SETUP GPIO
GPIO.setmode(GPIO.BOARD)
GPIO.setup(chan_list, GPIO.IN)

for key, value in locations.items():
    GPIO.add_event_detect(key, GPIO.BOTH, callback=my_callback)


#KEEP ON RUNNING!
while True:
    try:
        pass

    except KeyboardInterrupt:
        stored_exception=sys.exc_info()
#EXIT
if stored_exception:
    print("Forcably Closing App! Cleaning up...")

GPIO.cleanup()

print("Cleaning completed.")
exit(1)
