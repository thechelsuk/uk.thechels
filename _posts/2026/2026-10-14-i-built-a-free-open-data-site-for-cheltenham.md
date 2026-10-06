---
layout: post
syndicate:
  - mastodon
  - bluesky
  - textlog
date: 2026-10-14 08:00
title: I Built a Free Open Data Site for My Town
seo_title: "Building Cheltenham Open Data - A Free, Independent Local Data Site"
seo_description: "Why I built Cheltenham Open Data, a free and independent site that puts local public data in one place, and why it now needs local sponsors."
type: blog
---

For the last couple of months a lot of my spare time has gone into [Cheltenham Open Data](https://cheltenham-od.uk). It started because I wanted one place to check things about where I live: house prices, planning applications, fuel prices, flood warnings, bus disruption. All of it is public, but it's scattered across council PDFs, government spreadsheets and APIs that nobody outside a dev team would ever look at.

So it pulls everything together and refreshes on a schedule. Fuel prices update hourly, care home ratings monthly, and plenty in between. A Raspberry Pi does the frequent jobs now, after GitHub Actions turned out to run my "hourly" job once or twice a day.

A few rules I set myself:

- **Free to use**, with no accounts and no paywall.
- **No tracking cookies.** No ad tech, anonymised cookie-free stats, and newsletter addresses never shared with anyone.
- **Plain English.** Each page should answer a question a normal person might actually have.

The bit I'm still working out is how to pay for it. The plan is a handful of local sponsors, one business per section, each with a single "supported by" card. No pop-ups, no flashing banners. If you run a Cheltenham business, or know someone who does, the [sponsor page](https://cheltenham-od.uk/sponsor) explains how it works. Founding sponsors are £100 a month.

If you live locally, [The Cheltenham Week Ahead](https://cheltenham-od.uk/newsletter) is a free Monday email with the weather, roadworks, what's on and the top local stories. And if there's something about Cheltenham you wish you could look up in one place, tell me and I'll see if the data exists.
