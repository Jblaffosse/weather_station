# Weather Station

Weather station project.

## Bill of Materials (BOM)
The list of materials needed for the weather station is listed here: "docs/BOM.xlsx"

## Setup Raspberry Pi 4

A quick overview of the Raspberry Pi 4 Model B, along with the steps to load a new OS, is presented in the following link:
https://www.raspberrypi.org/app/uploads/2012/12/quick-start-guide-v1.1.pdf

## Pinout

As shown in the image "docs/Raspberry Pi 4 Model B - Pinout.png," please connect the following cables:

Raspberry Pi 4 Model B <-> Sensors using STEMMA QT

3V3 Power (Pin 1) <-> VIN (Red)

GPIO 2 - SDA (Pin 3) <-> SDA (Blue)

GPIO 3 - SCL (Pin 5) <-> SCL (Yellow)

Ground (Pin 9) <-> GND (Black)


## Installation

Import the git repository with [git](https://github.com/) in order to obtain the source code.

```bash
git clone https://github.com/Jblaffosse/weather_station.git
```

Then you can run the following script in order to verify and if needed install the following dependencies:
- time
- board
- adafruit_ahtx0
- adafruit_tsl2591
- flask

```bash
cd config/
./install.sh
```

## Execute Application
You can execute the Weather Station with:

```bash
TBD
```

## Troubleshooting
Here are the potential errors you may encounter:

- Impossible to install any python packages using pip:

```bash
$ pip3 install board
error: externally-managed-environment

× This environment is externally managed
╰─> To install Python packages system-wide, try apt install
    python3-xyz, where xyz is the package you are trying to
    install.

    If you wish to install a non-Debian-packaged Python package,
    create a virtual environment using python3 -m venv path/to/venv.
    Then use path/to/venv/bin/python and path/to/venv/bin/pip. Make
    sure you have python3-full installed.

    For more information visit http://rptl.io/venv
```

**Correction:**

```bash
sudo rm /usr/lib/python3.11/EXTERNALLY-MANAGED
```

- Impossible to install **adafruit_ahtx0** using pip:

```bash
$ python -m pip install adafruit_ahtx0
Looking in indexes: https://pypi.org/simple, https://www.piwheels.org/simple
ERROR: Could not find a version that satisfies the requirement adafruit_ahtx0 (from versions: none)
ERROR: No matching distribution found for adafruit_ahtx0
```

**Correction:**

```bash
pip3 install adafruit-circuitpython-ahtx0
```

- Impossible to install **adafruit_tsl2591** using pip:

```bash
$ python -m pip install adafruit_tsl2591
Looking in indexes: https://pypi.org/simple, https://www.piwheels.org/simple
ERROR: Could not find a version that satisfies the requirement adafruit_tsl2591 (from versions: none)
ERROR: No matching distribution found for adafruit_tsl2591
```

**Correction:**

```bash
pip3 install adafruit-circuitpython-tsl2591
```

- Impossible to use the I2C port:

```bash
$ python test_TSL2591.py
Traceback (most recent call last):
  File "/home/jblaffosse/weather_station/test/test_TSL2591.py", line 36, in <module>
    i2c_port = board.I2C()
               ^^^^^^^^^^^
  File "/home/jblaffosse/.local/lib/python3.11/site-packages/board.py", line 458, in I2C
    return busio.I2C(SCL, SDA)
           ^^^^^^^^^^^^^^^^^^^
  File "/home/jblaffosse/.local/lib/python3.11/site-packages/busio.py", line 36, in __init__
    self.init(scl, sda, frequency)
  File "/home/jblaffosse/.local/lib/python3.11/site-packages/busio.py", line 170, in init
    raise ValueError(
ValueError: No Hardware I2C on (scl,sda)=(3, 2)
Valid I2C ports: ((1, 3, 2), (0, 1, 0), (10, 45, 44))
```

**Correction:**

Please activate the I2C interface by following the instructions given here:
https://www.mathworks.com/help/matlab/supportpkg/enablei2c.html

Open the configuration for the Raspberry Pi 4 Model B by executing the following command:

```bash
$ sudo raspi-config
```

Then, go to "Interfacing Options > I2C" and select "Yes".
Finally you can exit when the I2C has been activated.

- Install SQLAlchemy:

```bash
$ python -m pip install flask-sqlalchemy
$ python -m pip install flask-migrate
```


## License
None