# What is SecurityQTPi

SecurityQTPi is a security retro fitted system that provides methods to communicate via the MQTT protocol, with a Raspberry Pi connected to your old security system's wiring.

## Motivation

My home was already wired up with a very elaborate security system. Unfortunately that system is heavily outdated (late 90's). But all the wiring is still in place and has low current, so I put it back in use! With a lot of help from my father (the electrical master) and my programmatic skills, we setup a breadboard connected to the old security system's wiring and listen for changes on the pins. When an entity (or access point) changes state, a MQTT message is sent out which is integrated for Home-Assistant!

---

## Software

  1. Test Folder - for help testing GPIO's  
    - There is a guide in the test folder on how to use the testing programs and what they do. [Click here](/test) to go there now.
  1. Root folder `main.py` <- SecurityQTPi, jump to [Setup](#setup)

### Prereqs

* Raspberry pi 3
* Python 2.7.x
* pip (python 2 pip)

### Tips if you feel stuck

* Knowing which GPIO mode to use! And other things about [RPi.GPIO](https://raspi.tv/2013/rpi-gpio-basics-4-setting-up-rpi-gpio-numbering-systems-and-inputs)
* [HomeAssistant MQTT Setup](https://home-assistant.io/components/mqtt/)
* [Bruh Automation](https://www.youtube.com/watch?v=AsDHEDbyLfg)
* [More MQTT stuff](https://learn.adafruit.com/diy-esp8266-home-security-with-lua-and-mqtt/configuring-mqtt-on-the-raspberry-pi)

---

## Setup

1. [Setup MQTT Broker](#setup-mqtt-broker)
1. [Setup SecurityQTPi](#setup-securityqtpi)



## Setup MQTT Broker

For simplicity - lets setup MQTT Broker on the same pi where securityqtpi will be running

1. Install - In terminal:
    ```bash
    sudo apt-get update
    sudo apt-get upgrade

    sudo apt-get install mosquitto
    sudo apt-get install mosquitto-clients
    ```

1. Setup mosquitto configuration file.
    - `sudo nano /etc/mosquitto/mosquitto.conf`
    - add the following contents into this file:
    ```txt
    allow_anonymous false
    password_file /etc/mosquitto/pwfile
    listener 1883
    ```

1. Set MQTT Broker username and password - In terminal:
    ```bash
    sudo mosquitto_passwd -c /etc/mosquitto/pwfile USERNAME_GOES_HERE
    ```

      - set USERNAME to what ever username you want
      - You will now be prompted to enter a password twice.
      ![MQTT Broker Password setup][1]

1. Start the MQTT Broker!
    ```bash
    sudo mosquitto -c /etc/mosquitto/mosquitto.conf -v -d
    ```

      - flag c: tells masquitto where to load it's configuration from
      - flag v: verbose mode - enable all logging types. This overrides
        any logging options given in the config file.
      - flag d: put the broker into the background after starting.

1. If you need to make updates to your mosquitto.conf reboot it with: `sudo systemctl restart mosquitto`
1. MQTT is already set to boot on startup because of the mosquitto.conf file!
1. Test MQTT broker
    - We're making sure the broker can subscribe and publish to a test topic. You will need 2 terminals open. For examples sake I set my username to **username** and password to **password**. I can't stress enough how important it is to set a strong password and good username.

    terminal 1:

    ```bash
    mosquitto_sub -d -u username -P password -t "homeassistant/cover/Zone1"
    ```

    terminal 2:

    ```bash
    mosquitto_pub -d -u username -P password -t "homeassistant/cover/Zone1" -m "Hello world"
    ```

    Example: _click to enlarge_
    ![MQTT Broker Test][2]



**NOTE**
> I set the topic in the example "homeassistant/cover/Zone1" to match what is currently in the config.template.yaml
>
> More on this config file is coming up soon!

---

### Setup SecurityQTPi

On your raspberrypi machine:

1. `git clone https://github.com/aeckard87/DoorQTPi.git` or [download zip](https://github.com/aeckard87/DoorQTPi/archive/dev.zip)
1. `cd DoorQTPi`or unzip and then cd into
1. `pip install -r requirements.txt`
1. Copy the config.template.yaml into a new file called `config.yaml`. Modify it accordingly, there are lots of comments in there to help.
  - Sample config.yaml:

    ```yaml
    mqtt:
        host: 127.0.0.1 #ip of where MQTT Broker is running, maintain 127.0.0.1 if running broker in the same place as security app
        port: 1883 #required MQTT port is 1883
        user: username #change username to what you setup when you ran "sudo mosquitto_passwd -c /etc/mosquitto/pwfile [YOUR USER NAME HERE]"
        password: password #change password to what you setup when you ran "sudo mosquitto_passwd -c /etc/mosquitto/pwfile [username]"
        discovery: true #defaults to false, comment to disable home-assistant discovery
        discovery_prefix: homeassistant #maintain homeassistant as discovery_prefix if you want home-assistant to discover this service
    accesspoints:
        -
            id: Zone1 #Descriptive text, this will be used as TOPIC
            name: test # Not required, if empty it defaults to an unsanitized version of the id paramater
            pin: 15 #PIN_NUM
            state_mode: normally_closed #defaults to normally open, comment this line to switch
            #invert_relay: true #defaults to false, uncomment to turn relay pin on by default

            # If you'd like to use your own topics, set discovery to false and update fields with format: "[discover_prefix]/cover/[topic]" and "[discover_prefix]/cover/[topic]/set"
            state_topic: "homeassistant/cover/Zone1"
            command_topic: "homeassistant/cover/Zone1/set"
        -
            id: Zone2
            name:
            pin: 17
            state_mode: normally_closed
            #invert_relay: true #defaults to false, uncomment to turn relay pin on by default
            state_topic: "homeassistant/cover/Zone2"
            command_topic: "homeassistant/cover/Zone2/set"
    ```


1. Make sure SecurityQTPi is running as intended.
    1. on run, you should see successful output. Example:
    ![Successful Start][3]
    1. Open/Close something your GPIO is wired to to verify STATECHANGED is triggered:
    ![State Changed][4]

1. Lets also make sure SecurityQTPi is sending messages to the topics it listed:
    ```text
    Sending updates on events to:
       homeassistant/cover/Zone1/state
       homeassistant/cover/Zone2/state
    ```

    - You will have to do this in a second terminal. Subscribe to one of the topics listed in the image above.
        - `mosquitto_sub -d -u username -P password -t "homeassistant/cover/Zone1"`
        - Open/Close a thing you have your GPIO wires connected to - you should see a response similar to this:
        ![MQTT Topic Success][5]


1. You're ready to run!
    1. To start the app on boot, run: `sudo ./autostart_systemd.sh`
        - you may need to `chmod +x autostart_systemd.sh`


---

[1]: images/mqtt_pass.png
[2]: images/test_mqtt.png
[3]: images/securityqtpi_start.png
[4]: images/state_changed.png
[5]: images/mqtt_sub_rec.png
