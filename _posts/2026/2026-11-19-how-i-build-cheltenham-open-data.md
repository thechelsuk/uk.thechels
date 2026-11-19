---
layout: post
syndicate:
  - mastodon
  - bluesky
  - rss
  - textlog
  - devnull
date: 2026-11-19 21:45
title: How I Build 800 Pages of Cheltenham Open Data
link: https://dev.to/thechelsuk/how-i-build-800-pages-of-local-open-data-with-jekyll-python-and-a-raspberry-pi-of8
cited: dev.to
type: linked
---

I've written up the technology behind [Cheltenham Open Data](https://cheltenham-od.uk) on dev.to: how around 90 Python fetchers, JSON files kept in git and a handful of Jekyll plugins turn into a little over 800 pages, with no database or server.

The bit I'd pass on to anyone building something similar is scheduling. GitHub Actions ran my "hourly" job once or twice a day, so now a Raspberry Pi at home runs the fast feeds and starts every workflow on time, with a Cloudflare Worker standing in when the Pi goes quiet.
