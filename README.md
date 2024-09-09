# Weather Station

Weather station project.

## Bill of Materials (BOM)
The list of materials needed for the weather station is listed here: "docs/BOM.xlsx"

## Setup Raspberry Pi 4

A quick overview of the Raspberry Pi 4 Model B, along with the steps to load a new OS, is presented in the following link:
https://www.raspberrypi.org/app/uploads/2012/12/quick-start-guide-v1.1.pdf

## Pinout

TBD

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

## License
None