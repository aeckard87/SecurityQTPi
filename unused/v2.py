import os
import binascii
import yaml
import paho.mqtt.client as mqtt
import re

from lib.state import State as Entry

print "Welcome to SecurityQTPi!"

# Update the mqtt state topic
def update_state(value, topic):
    print "State change triggered: %s -> %s" % (topic, value)

    client.publish(topic, value, retain=True)

# The callback for when the client receives a CONNACK response from the server.
def on_connect(client, userdata, rc):
    print "Connected with result code: %s" % mqtt.connack_string(rc)
    # Showing which topics SecurityQTPi is sending messages too
    for config in CONFIG['accesspoints']:
        state_topic = config['state_topic']
        print "Sending updates on events to %s" % state_topic

    # COMING SOON: SETUP FOR RELAYS
    # Showing which topics SecurityQTPi is listening to for cmds
    # for config in CONFIG['accesspoints']:
    #     command_topic = config['command_topic']
    #     print "Listening for commands on %s" % command_topic
    #     client.subscribe(command_topic)

# COMING SOON: SETUP FOR RELAYS
# Execute the specified command for an entry point
# def execute_command(entry, command):
#     try:
#         print "State: {}".format(entry.state)
#         print "Command: {}".format(command)
#         entryName = entry.name
#         print entryName
#     except:
#         entryName = entry.id
#         print entryName
#     print "Executing command %s for entry %s" % (command, entryName)


with open(os.path.join(os.path.abspath(os.path.dirname(__file__)), 'config.yaml'), 'r') as ymlfile:
    CONFIG = yaml.load(ymlfile)

### SETUP MQTT ###
user = CONFIG['mqtt']['user']
password = CONFIG['mqtt']['password']
host = CONFIG['mqtt']['host']
port = int(CONFIG['mqtt']['port'])
discovery = bool(CONFIG['mqtt'].get('discovery'))
if 'discovery_prefix' not in CONFIG['mqtt']:
    discovery_prefix = 'homeassistant'
else:
    discovery_prefix = CONFIG['mqtt']['discovery_prefix']

client = mqtt.Client(client_id="MQTTEntry_" + binascii.b2a_hex(os.urandom(6)), clean_session=True, userdata=None, protocol=4)

client.on_connect = on_connect

client.username_pw_set(user, password=password)
client.connect(host, port, 60)
### SETUP END ###

### MAIN LOOP ###
if __name__ == "__main__":
    # Create entry access objects and create callback functions
    for apconfg in CONFIG['accesspoints']:

        # If no name is set, then set to id - this is used for Home-Assistant Discovery
        if not apconfg['name']:
            apconfg['name'] = apconfg['id']

        # Sanitize id value for mqtt
        apconfg['id'] = re.sub('\W+', '', re.sub('\s', ' ', apconfg['id']))

        if discovery is True:
            # base_topic would look like homeassistant/cover/Front
            base_topic = discovery_prefix + "/cover/" + apconfg['id']
            config_topic = base_topic + "/config"
            # COMING SOON: SETUP FOR RELAYS
            # apconfg['command_topic'] = base_topic + "/set"
            apconfg['state_topic'] = base_topic + "/state"

        # COMING SOON: SETUP FOR RELAYS
        # command_topic = apconfg['command_topic']
        state_topic = apconfg['state_topic']


        entry = Entry(apconfg)

        # COMING SOON: SETUP FOR RELAYS
        # Callback per entry that passes a relay to the entry
        # def on_message(client, userdata, msg, entry=entry):
        #     execute_command(entry, str(msg.payload))

        # client.message_callback_add(command_topic, on_message)

        #Callback per entry that passes the entrys state topic
        def on_state_change(value, topic=state_topic):
            update_state(value, topic)

        #Listener will be executed when the entry state changes
        entry.onStateChange.addHandler(on_state_change)

        # Publish initial entry state
        client.publish(state_topic, entry.state, retain=True)

        # If discovery is enabled publish configuration
        if discovery is True:
            #client.publish(config_topic,'{"name": "' + apconfg['name'] + '", "command_topic": "' + command_topic + '", "state_topic": "' + state_topic + '"}', retain=True)
            client.publish(config_topic,'{"name": "' + apconfg['name'] + '", "state_topic": "' + state_topic + '"}', retain=True)

    # Main loop
    client.loop_forever()
