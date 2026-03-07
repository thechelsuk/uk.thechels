---

layout: post
date: 2026-03-07
title: Pompidou Section 1 - Site Improvements

---

I've added this RSS only feed, web mentions, syndication of content under the POSSE principle, and markdown copies of files into the deployment of the site all computed at build time over recent days. 

The cost to the build time is enormous though, previously it was about 2 minutes, but having to move away from GitHub's default simple pages deployment process to an actions based deploy action (in order to control the copy of the markdown it actually reduced to about 45 seconds. The webmention functionality has added about 3 minutes despite some aggressive throttling... such that I only look for mentions for posts published more recently.

``` yaml
throttle_lookups:
    last_week: daily
    last_month: weekly
    last_year: monthly
    older: monthly
``` 

Thanks to the following resources for the documentation and inspiration.

- <https://daverupert.com/rss-club/>
- <https://benjaminwil.info/antisocial/02/>
- <https://webmention.io>
- <https://brid.gy>
- <https://code.dblock.org/2026/01/15/serving-markdown-for-ai-agents.html>