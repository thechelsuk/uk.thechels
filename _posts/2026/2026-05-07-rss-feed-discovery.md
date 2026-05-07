---
date: 2026-05-07 21:00
title: "RSS Feed Discovery in well known is better than guessing"
cited: "Stuart Breckenridge"
link: "https://stuartbreckenridge.net/2026-05-04-moving-feed-discovery-to-well-known/"
seo: "RSS feed discovery in .well-known/feed-menu.json"
type: linked
---

I really like this idea, and I hope to see more sites adopt it, and more things move to within the .well-known namespace. So many sites are bloated with all sorts of random files in the root and in the `<head>`. I've added a feed-menu.json and syndication.json to my site.

> There’s an Internet-Draft that proposes moving feed discovery to /.well-known/feed-menu.json, which I think, in principle, is a great idea. Take the following very common use case:
>
> the user provides a website `<https://example.com>` to a feed reader
> the feed reader scans `<head>`and can’t find any feeds
> the feed reader then makes educated guesses to find feeds, e.g.,
> `/feed`
> `/rss`
> `rss.xml`
> `/atom`
> and so on
> Contrast that with:
>
> the user provides a website `<https://example.com>` to a feed reader
> the feed reader reads `<https://example.com/.well-known/feed-menu.json>` and immediately has a full rundown of the feeds the site offers
> The benefits are clear.
