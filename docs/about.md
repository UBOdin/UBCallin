---
layout: page
title: More Info
permalink: /about/
---

## CAD Files

Download the STL files for the pi-phone case and make it your own.

* [Back Cover](https://github.com/UBOdin/UBCallin/blob/master/models/BackCover.stl)
* [Front Cover](https://github.com/UBOdin/UBCallin/blob/master/models/FrontCover.stl)
* [Middle Part](https://github.com/UBOdin/UBCallin/blob/master/models/MiddlePart.stl)

## More Documentation

* [The Raspbery Pi Foundation](https://www.raspberrypi.org/help/) - Getting started with Raspberry Pi, how-tos and help from the organization behind the Raspberry Pi.
* [Adafruit](https://adafruit.com): A great resource for customizing raspberry pis and tinkering in general.  Adafruit has some amazing How-Tos, and the AdaFruit Blog is a great place for ideas.  Adafruit also sells parts if you need them.

## Resetting your pi-phone

If you need to reset your pi-phone to its initial state, pull out the microSD card, plug it into the provided adaptor and find a computer with an SD card reader.  You'll need to download [Etcher](https://etcher.io/) and the [PiPhone-Raspbian Image](https://odin.cse.buffalo.edu/public_data/2018-UBCallin-Raspbian.img).  Open the image in Etcher, point it at your SD card, and let it run.  Note: **This will erase everything on your pi-phone**.

## Installing the PiPhone software on an existing Pi OS

If you want to use your own OS with the pi-phone software, you can get it from the [UBCallin GIT repo](https://github.com/UBOdin/UBCallin).  You'll also need some python libraries.
```console
git clone https://github.com/UBOdin/UBCallin.git
sudo pip2 install easygui pigpio
```
If you want to use python to talk to the FONA board, look in `UBCallin/python`.

The following will set up the FONA/Scratch bridge and let Scratch talk to the FONA board.
```console
sudo mv UBCallin /opt/PhoneServer
cd /opt/PhoneServer/setup
sudo systemctl enable /opt/PhoneServer/setup/phoneserver.service
sudo systemctl start phoneserver.service
```
Notes:
1. The FONA/Scratch bridge only works with Scratch 1.4
2. When starting a *new* scratch program, you will need to follow the instructions to [Enable Remote Sensor Connections](https://en.scratch-wiki.info/wiki/Communicating_to_Scratch_via_Python_with_a_GUI#Enable_Remote_Sensor_Connections)
3. To check whether everything is set up correctly, broadcast 'hi' (without the quotes).  A dialog box should pop up with a version string for the FONA.