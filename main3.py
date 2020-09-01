import os
import binascii
import yaml
import paho.mqtt.client as mqtt
import re

# from lib.state import State as Entry
from lib.messaging import Messaging as Messaging
def update_state(value, topic):
    print(f"State change triggered: {topic} -> {value}")

    client.publish(topic, value, retain=True)

# The callback for when the client receives a CONNACK response from the server.
def on_connect(client, userdata, rc):
    print('\n### CONNECTION STATUS ###')
    print('Connected with result code: \t{}'.format(mqtt.connack_string(rc)))
    # Showing which topics SecurityQTPi is sending messages too
    print('Sending updates on events to:')
    for ap in config['accesspoints']:
        state_topic = ap['state_topic']
        print('\t{}'.format(state_topic))



with open(os.path.join(os.path.abspath(os.path.dirname(__file__)), 'config.yaml'), 'r') as ymlfile:
    CONFIG = yaml.load(ymlfile, Loader=yaml.FullLoader)
message = Messaging(CONFIG)

message.client = mqtt.Client(client_id='MQTTEntry_1', clean_session=True, userdata=None, protocol=4)

message.client.on_connect = on_connect

message.client.username_pw_set(message.user, password=message.password)
message.client.connect(message.host, message.port, 60)




##### MAIN LOOP #####
if __name__ == "__main__":
    print("Welcome to SecurityQTPi!")
    # message.client.loop_forever()
#
#
#
#
#
# #*************************
#     # Create entry access objects and create callback functions
#     for apconfg in CONFIG['accesspoints']:
#
#         # If no name is set, then set to id - this is used for Home-Assistant Discovery
#         if not apconfg['name']:
#             apconfg['name'] = apconfg['id']
#
#         # Sanitize id value for mqtt
#         apconfg['id'] = re.sub('\W+', '', re.sub('\s', ' ', apconfg['id']))
#
#         if discovery is True:
#             # base_topic would look like homeassistant/cover/Front
#             base_topic = discovery_prefix + "/cover/" + apconfg['id']
#             config_topic = base_topic + "/config"
#
#             apconfg['state_topic'] = base_topic + "/state"
#
#         state_topic = apconfg['state_topic']
#         entry = Entry(apconfg)
#
#         #Callback per entry that passes the entrys state topic
#         def on_state_change(value, topic=state_topic):
#             update_state(value, topic)
#
#         #Listener will be executed when the entry state changes
#         entry.onStateChange.addHandler(on_state_change)
#
#         # Publish initial entry state
#         client.publish(state_topic, entry.state, retain=True)
#
#         # If discovery is enabled publish configuration
#         if discovery is True:
#             client.publish(config_topic,'{"name": "' + apconfg['name'] + '", "state_topic": "' + state_topic + '"}', retain=True)
#
#     # Main loop
#     client.loop_forever()
