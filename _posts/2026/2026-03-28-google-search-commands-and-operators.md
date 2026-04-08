---

layout: post
date: 2026-03-28
title: Dorking - Search Commands and Operators
type: rss

---

Search dorking tips and tricks and how to the best from your search engine. Documented for archive purposes before AI takes over.

## Precision Operators

- **`site:`** — Limits results to a specific website or domain (e.g. `site:gov vaccine`)
- **`-site:`** — Excludes a specific site from results (e.g. `electric vehicles -site:Kia.com`)
- **`"exact phrase"`** — Forces Google to match those exact words in that exact order
- **`-word`** — Removes a word from results entirely (e.g. `jaguar -car`)
- **`X..Y` (number range)** — Filters by numerical range; works for prices, years, or any measurement (e.g. `laptop £500..£800`)
- **`*` (wildcard)** — Stands in for any missing word or phrase (e.g. `"the * of artificial intelligence"`)
- **`AROUND(#)`** — Undocumented proximity operator; returns results where two terms appear within # words of each other (e.g. `climate AROUND(3) policy`)
- **Verbatim mode** — Via Tools > All Results > Verbatim; disables synonym-swapping and personalisation, returns exactly what you typed

## Finding Primary Sources

- **`filetype:`** — Returns only a specific file type (e.g. `filetype:pdf remote work productivity`)
- **`intitle:"index of"`** — Surfaces open file directories on servers with directory listing enabled (e.g. `intitle:"index of" /pdf "media literacy"`)
- **`before:` / `after:`** — Sets a date boundary on results (e.g. `mental health research after:2023`)
- **`intitle:`** — Filters to pages where a phrase appears in the page title (e.g. `intitle:"media literacy"`)
- **`inurl:`** — Filters by text appearing in the URL (e.g. `inurl:gov intitle:"AI policy"`)

## Finding Real Human Opinions

- **`"can anyone recommend"`** — Surfaces forum threads and community posts asking for genuine recommendations, bypassing SEO content
- **`@reddit` (or other platform)** — Biases results toward social/community discussions from that platform
- **Omitted results link** — Click “include omitted results” at the bottom of a page; shows less-trafficked, less SEO-optimised sources

## Stacking Operators

- Combine multiple operators for precision (e.g. `filetype:pdf "information literacy" site:edu before:2015`)

## Fast Answer Shortcuts (type directly into search bar)

- **Flight number** (e.g. `UA 2157`) — Live gate, times, delay status, and real-time tracker
- **Package tracking number** — Auto-detects UPS/FedEx/USPS format and shows live delivery status
- **`run speed test`** — Measures download/upload speed in-browser, no third-party site needed
- **`[thing] vs [thing]`** — Side-by-side comparison panel (works for food, software, medications, etc.)
- **`define: [word]`** — Full dictionary definition plus etymology
- **`how to pronounce [word]`** — Audio button and phonetic spelling
- **`[food] calories`** — Nutritional information inline
- **`sunrise [city]`** / **`sunset [city]`** — Exact times for any location
- **`time in [city]`** — Current local time anywhere in the world
- **`[amount] [currency] to [currency]`** — Live exchange rate
- **`stock [ticker]`** — Live price chart with trading volume
- **`tip for $[amount]`** — Tip calculator with percentage and split options
- **`translate [phrase] to [language]`** — Full translation widget with audio
- **`what is my IP`** — Returns your IP address immediately
- **`random number between X and Y`** — Instant random number generator
- **`color picker`** — Interactive colour wheel with hex and RGB codes
- **`timer [X] minutes`** — Starts a countdown without leaving Google
- **`metronome`** — Working, adjustable metronome
- **`bubble level`** — Uses phone gyroscope as an actual level
- **`breathing exercise`** — Guided timed breath pattern
- **`what sound does a [animal] make`** — Plays actual audio
- **`flip a coin`** / **`roll a die`** — Works as described
- **Any maths equation** — Solved immediately in the search bar

## Image Search Tip

- **Tools > Usage Rights** — Filters image results to only those licensed for reuse (two clicks deep, easy to miss)

Source: <https://cardcatalogforlife.substack.com/p/google-has-a-secret-reference-desk>
Author: cardcatalogforlife
Date: 2026-03-22
