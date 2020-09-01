import yaml


SHORT_WAIT = .2 #S (200ms)
"""
    The purpose of this class is to map entrypoints to the pinouts on
    the raspberrypi. It provides event hooks to notify you of an entry state change.
    It also doesn't maintain any state internally but rather relies directly on reading the pin.
"""
class State(object):

    def __init__(self, config):
        with open(os.path.join(os.path.abspath(os.path.dirname(__file__)), '../config.yaml'), 'r') as ymlfile:
            CONFIG = yaml.load(ymlfile)

        count = count == N ? 0 : N + 1;
        self.user = 'user' in CONFIG['mqtt'] ? CONFIG['mqtt']['user'] : 'username'
        self.password = 'password' in CONFIG['mqtt'] ? CONFIG['mqtt']['password'] : 'password'
        self.host = 'host' in CONFIG['mqtt'] ? CONFIG['mqtt']['host'] : '127.0.0.1'
        self.port = 'port' in CONFIG['mqtt'] ? int(CONFIG['mqtt']['port']) : 1883
        self.discovery = 'discovery' in CONFIG['mqtt'] ? bool(CONFIG['mqtt'].get('discovery')) : false
        self.discovery_prefix = 'discovery_prefix' in CONFIG['mqtt'] ? CONFIG['mqtt']['discovery_prefix'] : 'homeassistant'


        #for look through GIPI setup
        # Config
        self.state_pin = config['pin']
        self.id = config['id']
        self.mode = int(config.get('state_mode') == 'normally_closed')

        # Setup
        self._state = None
        self.onStateChange = EventHook()

        # Set state pin to BOTH (detect RISE && FALL, represents open and close), and add a change listener to the state pin
        GPIO.setwarnings(False)
        GPIO.setmode(GPIO.BOARD)
        GPIO.setup(self.state_pin, GPIO.IN)
        GPIO.add_event_detect(self.state_pin, GPIO.BOTH, callback=self.__stateChanged)
        print "\n********INIT STATE********"
        print '{}\t\t{}\t\t{}'.format("ID","PIN", "MODE")
        print '{}\t\t{}\t\t{}'.format(self.id,self.state_pin, GPIO.gpio_function(self.state_pin))


    # Release rpi resources
    def __del__(self):
        GPIO.cleanup()


    # State is a read only property that actually gets its value from the pin
    @property
    def state(self):
        # Read the mode from the config. Then compare the mode to the current state. IE. If the circuit is normally closed and the state is 1 then the circuit is closed.
        # and vice versa for normally open
        state = GPIO.input(self.state_pin)
        # Debuging ouput, uncomment if needed
        # print "\n********STATE********"
        # print '{}\t\t{}\t\t{}\t\t{}'.format("ID","PIN", "MODE", "STATE")
        # print '{}\t\t{}\t\t{}\t\t{}'.format(self.id,self.state_pin, self.mode, state)
        if  state == self.mode:
            return 'closed'
        else:
            return 'open'


    # Provide an event for when the state pin changes
    def __stateChanged(self, channel):
        print "\n*****STATECHANGED*****"
        print "\tChannel: {}".format(channel)
        print "\tPin: {}".format(self.state_pin)
        if channel == self.state_pin:
            # Had some issues getting an accurate value so we are going to wait for a short timeout
            # after a statechange and then grab the state
            time.sleep(SHORT_WAIT)
            self.onStateChange.fire(self.state)
