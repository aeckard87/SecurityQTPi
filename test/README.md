## TESTING

using python 2.7.16

### testio.py

Tests the given pins function/Current state on run.

- You will need to add the pin numbers in here yourself, this program is simple in that it isn't reading from a configuration file. Comments in code explain.
- Run: `python testio.py`

Example Output:
```bash
pi@IOTest:~ $ python testio.py
RASPBERRY INFO:
	P1_REVISION: 2
	RAM: 512M
	REVISION: e
	TYPE: Model B
	PROCESSOR: BCM2835
	MANUFACTURER: Sony UK
RPi.GIPO INFO:
	Version: 0.7.0
	MODE: 11
PINS
	2: 1
	3: 1
```
---

### open.py

Continuously running python app that watches for state changes in pins.

- You will need to add the pin numbers in here yourself, this program is simple in that it isn't reading from a configuration file. Comments in code explain.
- Run: `python open.py`
- Close: ctrl+c

Example Output:
```bash
pi@IOTest:~ $ python ion.py
Living Room Zone opened!
Living Room Zone closed!
DownStairs Zone opened!
DownStairs Zone closed!
```
