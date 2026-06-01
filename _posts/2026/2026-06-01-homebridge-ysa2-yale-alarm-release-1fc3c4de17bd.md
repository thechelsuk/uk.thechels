---
layout: post
date: 2026-06-01 19:03
title: Homebridge (YSA2) Yale Alarm Version v2.2.5
type: release
cited: GitHub
link: https://github.com/thechelsuk/homebridge-YSA2-plugin/releases/tag/v2.2.5
release_id: tag:github.com,2008:Repository/1218287392/v2.2.5
release_repo: homebridge-ysa2-plugin
release_project: homebridge-ysa2-yale-alarm
release_version: v2.2.5
---

First release fixing a bunch of bugs and adding tests to get to a working alarm, that can be armed/disarmed in homekit and homebridge.

To use this with automation in homekit. User a dummy device switch. set the switch on as the trigger to arm the alarm, and off to disable. Apple seems to block direct alarm changes, but the one-hop via a dummy switch works fine.

[Read more about my projects](/projects)
