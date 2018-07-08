---
layout: page
title: Scratch API
permalink: /docs/
---

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
