---
layout: post
title: How to manage raspberry pi
seo: Ways - how to manage raspberry pi
tag: ways
date: 2026-06-19 18:00
type: ways
syndicate: true
---

## Re-flash the Pi with Raspberry Pi OS

1. On your Mac, install  Raspberry Pi Imager.
2. Put the Pi's SD card in the Mac.
3. In Pi Imager:
    - Choose OS → Raspberry Pi OS (64‑bit, with desktop).
    - Choose Storage → your SD card.
    - Click the gear icon:
        - Set hostname.
        - Enable SSH.
        - Set username/password.
        - Optional: preconfigure Wi‑Fi.
    - Click Write.

Stick the card back in the Pi and boot.

## Tailscale

```bash
curl -fsSL https://tailscale.com/install.sh | sh

sudo tailscale up
```

## Rustdesk

```bash
wget https://github.com/rustdesk/rustdesk/releases/download/1.4.6/rustdesk-1.4.6-aarch64.deb

sudo apt install ./rustdesk-1.4.6-aarch64.deb
```

- Enable direct IP access.
- Set a password if the Pi will be a host.
- Use Tailscale IPs to connect between devices.

## Mouse via bluetooth

```bash
Bluetoothctl
```

then...

```bash
discoverable on
pairable on
agent on
default-agent
```

then... type the following commands to pair, connect, and trust the mouse, change the MAC address to your mouse's MAC address.

```bash
pair 11:22:33:44:55:66
connect 11:22:33:44:55:66
trust 11:22:33:44:55:66
```

## Homebridge

```bash
curl -sL https://repo.homebridge.io/raspbian | sudo -E bash -
sudo apt install homebridge -y
```

Then

```bash
sudo systemctl status homebridge
```

## pi-hole

```bash
curl -sSL https://install.pi-hole.net | bash
```

## Notes

### move to root

```bash
sudo -i
```
