# Miffy's Super Powers

When my oldest daughter was born, one my dearest friend [Britt Selvitelle](https://twitter.com/bs) gave us a gift of [Miffy Lamp](https://mrmaria.com/miffy-xl-lamp/) from Japan.

![Mr Maria Miffy Lamp](pics/miffy.png)

Figure 1: Mr Maria Miffy Lamp

## My problems with power

Miffy had two "problems", the first being the power cord for the lamp didn't fit into american outlets. The second was the bulb being incandescent consumed lots of power and created lots of heat (and rather bright for a night-light).

## Solution: Let's put it on the network!

Having learned about ESP-8266, a cheap & tiny microcontroller that has WiFi, I thought it would be cool to give the bunny an API.

I grabbed an [AdaFruit](https://adafruit.com) NeoPixel (RGB led), and figured out how to wire it up to ESP8266 (seen in the breadboard below)

After adapting the code to connect to my WiFi, I found code that implemented a webserver on the ESP8266.

This allowed me to expose an API to change the brightness and color via HTTP calls.

![miffy circuit](pics/circuit.jpg)

Figure 2: Miffy's new brain & light

## Build

The build was pretty simple. After prototyping the circuit design and field testing it with my daughters (using it as a night light), I decided to upgrade from a single NeoPixel to a [16 LED NeoPixel Ring](https://www.adafruit.com/product/1463). This allows more light and some interesting patterns.

![back together](pics/build.jpg)

Figure 3: Miffy put back together, glowing

A quick solder job, then I hot glued the circuit where the lamp had been attached.

## A better nightlight

My kids like the lights to be brighter when going to bed, but stay in bed longer if the light isn't as bright through the night.

I was able to add logic to set the light brightness higher during bedtime, but then fade slowly over the next hour.

## Idea 1: Exposing via HTTP API

While it was cool having an API and webpage to change the colors, I decided to explore integration with Google Home via [ifftt](https://ifttt.com) (if this then that - a web service that lets you connect APIs together with minimal fuss).

Enabling IFTTT to talk to my web service required me to punch a hole in my router to expose bunny to the internet.

Now you could ask google to change the color of the light.


```
+-------+   +-------------+   +------------+   +------------+
| human +-->| google home +-->| google.com |-->| ifttt.com  |
+-------+   +-------------+   +------------+   +-----+------+
                                                     |
                                                     v
                           +--------------------------------+
                           | my-house-domain/bunnyapi?color |
                           +----------+---------------------+
                                      |
                                      v
+--------------+   +---------+    +-------+
| bunny lights |<--+ esp8266 |<--+ router |
+--------------+   +---------+    +-------+
```

## Idea 2: Micropython + mqtt + programmable spaces!

Since the original implementation, the hardware hasn't changed, but the software and method of exposing it has.

After reading [how to build a programmable space](https://haiperspace.com/writing/21-09-25-growing-a-space/) by [@jhaip](https://twitter.com/jhaip), and reading/watching demos on [Programmable.Space](https://programmable.space/), I was motivated to rebuild this project (and others) using similar ideas.

Hacking time is quite limited, so after failing/fumbling trying to get zeromq working on the esp8266, I switched to using mqtt.

Thanks to an [MicroPython – Getting Started with MQTT on ESP32/ESP8266](https://randomnerdtutorials.com/micropython-mqtt-esp32-esp8266/), I was able to really quickly convert my http based system to listening for mqtt messages.

Now I can "wish" miffy to become a color by publishing an message with the 3 or 6 hex digits (ffdd00 or 08f).

I wrote a quick "miffy" golang program to publish to it.

Currently I'm using [hmq](https://github.com/fhmq/hmq) as my broker (server), and [paho.mqtt.golang](https://github.com/eclipse/paho.mqtt.golang) as my client library.

One step closer to the vision that @jhaip shared!