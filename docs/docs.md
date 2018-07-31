---
layout: page
title: For Students
permalink: /docs/
---

## Connecting to your Pi Phone

Your Pi Phone has two sets of connectors, two on the Pi itself, and three on the FONA.  On the Pi (under the grip):

* **MiniHDMI**: Use the included HDMI adapter to plug this into your monitor (or a TV).  
* **MicroUSB**: Use the included MicroUSB to USB adapter to plug in a mouse or keyboard, or a USB Hub that will let you connect more than one thing (Most computer monitors have built-in USB hubs!)

On the FONA (top of the phone):

* **Battery**: Plug the battery in here to turn the FONA on.
* **MicroUSB**: Plug a standard cell-phone charger like the one included with your kit in to charge your battery.
* **Four-pole Audio** Plug in any four-pole headphones (the kind with a mic) to call in private (and see the audio broadcasts below).

<img src="../images/piphone-ports.jpg" />

<hr />

## More Documentation

* [Scratch](https://en.scratch-wiki.info/wiki/Scratch_User_Interface_(1.4)) - Learn more about programming in Scratch (your phones have Scratch version 1.4)
* [The Raspbery Pi Foundation](https://www.raspberrypi.org/help/) - Getting started with Raspberry Pi, how-tos and help from the organization behind the Raspberry Pi.
* [Adafruit](https://adafruit.com): A great resource for customizing raspberry pis and tinkering in general.  Adafruit has some amazing How-Tos, and the AdaFruit Blog is a great place for ideas.  Adafruit also sells parts if you need them.

<hr />

## FONA Scratch Broadcasts

<p>Here's a list of broadcast messages that you can send in scratch to activate different features of your FONA board.  If you don't already see one of these in the pop-up menu on the <i>Broadcast</i> (or <i>When I Receive</i>) block, pick "New/Edit..." and enter the broadcast messages exactly as it's written below.</p>

<table>
  <tr>
    <th style="width: 160px">Broadcast</th>
    <th>Explanation</th>
  </tr>
  <tr><td colspan="2" style="font-weight: bold" align="center">
    Broadcast messages that check if things are working
  </td></tr>
  <tr>
    <td style="font-weight: bold">hi</td>
    <td>The FONA will respond with a dialog box that shows you the details of the FONA board you're connected to.</td>
  </tr><tr>
    <td style="font-weight: bold">ping</td>
    <td>The FONA will respond by broadcasting <b>pong</b></td>
  </tr><tr>
    <td style="font-weight: bold">test-rssi</td>
    <td>The FONA will respond with a dialog box that shows you the current signal strength as a percentage from 0 to 100.</td>
  </tr>

  <tr><td colspan="2" style="font-weight: bold" align="center">Broadcast messages for managing calls</td></tr>
    <tr>
      <td style="font-weight: bold">start-call</td>
      <td>The FONA will dial the number stored in the all-sprites variable named <b>outgoing-number</b> if it is 10 digits long, or broadcast <b>error</b> otherwise.</td>
    </tr><tr>
      <td style="font-weight: bold">hang-up</td>
      <td>If you're currently on a call, the FONA will hang up the call.  If the FONA is ringing, the call will go to voicemail.</td>
    </tr><tr>
      <td style="font-weight: bold">pick-up</td>
      <td>If the FONA is ringing, it will pick up the call</td>
    </tr>
  <tr><td colspan="2" style="font-weight: bold" align="center">Broadcast messages for managing audio</td></tr>
    <tr>
      <td style="font-weight: bold">audio-speaker</td>
      <td>The FONA will use the connected speaker/microphone for calls.</td>
    </tr><tr>
      <td style="font-weight: bold">audio-headphones</td>
      <td>The FONA will use the headphone jack for calls (this is the default).</td>
    </tr>
  <tr><td colspan="2" style="font-weight: bold" align="center">Other Broadcast messages</td></tr>
    <tr>
      <td style="font-weight: bold">turn-led-on</td>
      <td>Ties <a href="https://pinout.xyz/pinout/pin31_gpio6#">GPIO Pin 6</a> to 'high' (3.3V).</td>
    </tr><tr>
      <td style="font-weight: bold">turn-led-off</td>
      <td>Ties <a href="https://pinout.xyz/pinout/pin31_gpio6#">GPIO Pin 6</a> to 'low' (Gnd).</td>
    </tr>
  <tr><td colspan="2" style="font-weight: bold" align="center">Broadcast messages you'll get from the FONA.</td></tr>
    <tr>
      <td style="font-weight: bold">incoming-call</td>
      <td>The FONA broadcasts this when you get a phone call.  The incoming caller ID should show up in the all-sprites variable named <b>incoming-number</b>.</td>
    </tr><tr>
      <td style="font-weight: bold">error</td>
      <td>When something bad happens.</td>
    </tr><tr>
      <td style="font-weight: bold">button-1-pushed</td>
      <td>Broadcast when the leftmost PiTFT button is pushed (GPIO #27)</td>
    </tr><tr>
      <td style="font-weight: bold">button-2-pushed</td>
      <td>Broadcast when the center-left PiTFT button is pushed (GPIO #23)</td>
    </tr><tr>
      <td style="font-weight: bold">button-3-pushed</td>
      <td>Broadcast when the center-right PiTFT button is pushed (GPIO #22)</td>
    </tr><tr>
      <td style="font-weight: bold">button-4-pushed</td>
      <td>Broadcast when the rightmost PiTFT button is pushed (GPIO #17)</td>
    </tr>


</table>
