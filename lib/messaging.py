import os
import binascii
import yaml
import paho.mqtt.client as mqtt
import re



# def update_state(value, topic):
#     print(f"State change triggered: {topic} -> {value}")
#
#     client.publish(topic, value, retain=True)
#
# # The callback for when the client receives a CONNACK response from the server.
# def on_connect(client, userdata, rc):
#     print('\n### CONNECTION STATUS ###')
#     print('Connected with result code: \t{}'.format(mqtt.connack_string(rc)))
#     # Showing which topics SecurityQTPi is sending messages too
#     print('Sending updates on events to:')
#     for ap in config['accesspoints']:
#         state_topic = ap['state_topic']
#         print('\t{}'.format(state_topic))

class Messaging(object):

    def __init__(self, config):
        self.user = config['mqtt']['user'] if 'user' in config['mqtt'] else 'username'
        self.password = config['mqtt']['password'] if 'password' in config['mqtt'] else 'password'
        self.host = config['mqtt']['host'] if 'host' in config['mqtt'] else '127.0.01'
        self.port = int(config['mqtt']['port']) if 'port' in config['mqtt'] else 1883
        self.discovery = bool(config['mqtt'].get('discovery')) if 'discovery' in config['mqtt'] else false
        self.discovery_prefix = config['mqtt']['discovery_prefix'] if 'discovery_prefix' in config['mqtt'] else 'homeassistant'

        # # id = 'MQTTEntry_' + str(binascii.b2a_hex(os.urandom(6)))
        # self.client = mqtt.Client(client_id='MQTTEntry_1', clean_session=True, userdata=None, protocol=4)
        #
        # self.client.on_connect = on_connect
        #
        # self.client.username_pw_set(self.user, password=self.password)
        # self.client.connect(self.host, self.port, 60)




        # Main loop
        #client.loop_forever()
