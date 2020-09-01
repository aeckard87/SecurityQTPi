import os
import binascii
import yaml
import paho.mqtt.client as mqtt
import re



##### MAIN LOOP #####
class AccessPoint(object):
    def __init__(self, config):
        # Create entry access objects and create callback functions
        if 'accesspoints' in config:

            for ap in config['accesspoints']:

                # If no name is set, then set to id - this is used for Home-Assistant Discovery
                if not ap['name']:
                    ap['name'] = ap['id']

                # Sanitize id value for mqtt
                ap['id'] = re.sub('\W+', '', re.sub('\s', ' ', ap['id']))

                if discovery is True:
                    # base_topic would look like homeassistant/cover/Front
                    base_topic = discovery_prefix + "/cover/" + ap['id']
                    config_topic = base_topic + "/config"

                    ap['state_topic'] = base_topic + "/state"

                state_topic = ap['state_topic']
                entry = Entry(ap)

                #Callback per entry that passes the entrys state topic
                def on_state_change(value, topic=state_topic):
                    update_state(value, topic)

                #Listener will be executed when the entry state changes
                entry.onStateChange.addHandler(on_state_change)

                # Publish initial entry state
                client.publish(state_topic, entry.state, retain=True)

                # If discovery is enabled publish configuration
                if discovery is True:
                    client.publish(config_topic,'{"name": "' + ap['name'] + '", "state_topic": "' + state_topic + '"}', retain=True)

        # Main loop
        client.loop_forever()
