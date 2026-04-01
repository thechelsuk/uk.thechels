---
layout: post
title: How to reset WiFi on Homebridge
seo: Ways - How to reset WiFi on Homebridge
tag: ways
permalink: /ways/reset-wifi-homebridge
link: https://github.com/homebridge/homebridge-raspbian-image/wiki/How-To-Reset-WiFi
cited: Homebridge
date: 2026-03-01

---

If you have a Raspberry Pi running the Homebridge Raspberry Pi and need to disconnect it from your local WiFi network, you can do this by following these steps.

Run sudo hb-config and select the Networking option to run the NetworkManager Terminal UI.

1. This will bring up this screen, select Edit a connection.
2. Select your WiFi connection from the list and delete it.
3. Confirm you want to delete it.
4. Exit the NetworkManager Terminal UI and reboot your Raspberry Pi.

_After rebooting, your Raspberry Pi will no longer be connected to your local WiFi network. You can then set up a new WiFi connection using the Homebridge Config UI X or by running sudo hb-config and selecting the Networking option again._
