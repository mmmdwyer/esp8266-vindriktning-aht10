<p align="center"><h2>MQTT connectivity for the Ikea VINDRIKTNING</h2></p>

See also the original project at [https://github.com/Hypfer/esp8266-vindriktning-particle-sensor](https://github.com/Hypfer/esp8266-vindriktning-particle-sensor).

This repository contains an ESP8266 firmware, which adds MQTT to the Ikea VINDRIKTNING PM2.5 air quality sensor.  The modification  doesn't interfere with normal operation of the device in any way.  The ESP8266 just adds another data sink beside the colored LEDs. This modification adds and AHT10 i2c temperature and humidity sensor.

The Home Assistant Autodiscovery stuff hasn't been modified, because I can't test it, so it is very likely wrong at the moment.

## Prerequisites

To extend your air quality sensor, you will need

- An ESP8266 with a 5v voltage regulator (e.g. a Wemos D1 Mini)
 - The D1 Mini fits inside the box. Larger devices, Feather and NodeMCU are a BIT too big.
- An AHT10 Temperature/Humidity sensor module (with all the i2c resistors already on board)
- Some short solid wires
- Some short stranded wires
- A soldering iron
- A long PH0 Screwdriver (e.g. Wera 118022)

Directions
- Use about 15mm of solid wire to wire the AHT10 to your WEMOS D1 Mini.
 - Run power (red) to the 3.3v port.
 - Run ground (black) to the G port. Do not yet solder this!
 - Run SCL (I used green) to the D1 port.
 - Run SDA (I used blue) to the D2 port.
- Use about 40mm of stranded wire to wire the WEMOS to the Vindriktning.
 - Near the top you will find 5 circular test points. Tin each with some solder.
 - Run power (Blue?) to the 5V port.
 - Run ground (Green?) to the G port. You can now solder this and the AHT10 ground.
 - Run the pad 'rest' (yellow?) to the D3 port.
- Gently flex the AHT10 so it is sort of floating over the WEMOS.
- Program the WEMOS now.
- Tuck the whole mess back into the Vindriktning case. The WEMOS will sit flat on the roof of the case, and the temp sensor will dangle down into the air stream from the dust sensor.

## Software

The firmware can be built and flashed using the Arduino IDE.

For this, you will need to add ESP8266 support to it by [using the Boards Manager](https://github.com/esp8266/Arduino#installing-with-boards-manager).

Furthermore, you will also need to install the following libraries using the Library Manager:

* ArduinoOTA 1.0.3
* ArduinoJSON 6.10.1
* PubSubClient 2.8.0
* WiFiManager 0.15.0
* Adafruit AHT10 0.1.0
* Adafruit BusIO 1.9.1
* Adafruit Unified Sensor 1.1.4

Just build, flash, and you're done.

When connecting everything up, you should see an open Wi-Fi Access Point to configure your Wi-Fi and MQTT credentials.

## References and sources

- [Original Source](https://github.com/Hypfer/esp8266-vindriktning-particle-sensor)
- [RevSpace](https://revspace.nl/VINDRIKTNING) - Details about the device
- [Adam Hořčica](https://twitter.com/horcicaa/status/1415291684569632768) - More detail
