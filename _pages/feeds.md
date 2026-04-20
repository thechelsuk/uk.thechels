---
layout: pages
title: Available RSS Feeds in XML and JSON formats
permalink: /feeds
seo: Subscribe to various JSON, RSS, and Data feeds

---

A number of RSS feeds are available. All feeds are Atom/XML unless otherwise specified.

- [Main Feed](/feed.xml) - All post feed
- [Main feed as JSON](/feed.json) - All post feed.
- [Daily only](/daily.xml) - A daily briefing of news, notices, quotes, and more.
- [Mixtapes only](/mixtapes.xml) - Mixtape only posts.
- [Posts only](/posts.xml) - Posts without linked/quote posts.
- [Releases only](/releases.xml) - Release only posts.
- [RSS only](/rss.xml) - Secret RSS only posts.
- [TIL only](/til.xml) - TIL only posts.
- [Ways only](/ways.xml) - Ways only posts.
- [Videos only](/videos.xml) - Video only posts.

## Data Feeds

- [Films](/films.xml) - Film reviews.
- [Bluesky](https://bsky.app/profile/did:plc:dz7xwi7wgfyzk4oemurkomax/rss) - A feed directly from Bluesky.
- [Mastodon](https://mastodon.social/@Thechelsuk.rss) - A feed directly from Mastodon.
- [Youtube](https://www.youtube.com/feeds/videos.xml?channel_id=UCwK4oZ8hw9RS6tZKEjw_qLw) - A feed directly from YouTube.

and;

{% assign all_entries = "" | split: "" %}
{% for post in site.posts %}
  {% assign all_entries = all_entries | push: post %}
{% endfor %}
{% for item in site.data.bluesky %}
  {% assign all_entries = all_entries | push: item %}
{% endfor %}
{% for item in site.data.mastodon %}
  {% assign all_entries = all_entries | push: item %}
{% endfor %}
{% for item in site.data.films %}
  {% assign all_entries = all_entries | push: item %}
{% endfor %}

- Firehose [Atom/XML](/firehose.xml) - A firehose feed of all content (**{{ all_entries | size }}** total entries) from all sources  above in one single feed.

## Niche Summary Feeds

- [Dotnet News Summary](https://feeds.thechels.uk/dotnet.rss)
- [SecOps News Summary](https://feeds.thechels.uk/secops.rss)
- [Insurance News Summary](https://feeds.thechels.uk/insurance.rss)
- [Local News Summary](https://cod.thechels.uk/daily.rss)
- [Local Flood Alerts](https://cod.thechels.uk/flood.xml)

If you don’t have a feed reader then I highly recommend using [NetNewsWire](https://netnewswire.com/). It’s really good, offers icloud sync across devices, loads of third-party integrations and is completely free. If you go ahead and use it, you can also try my completely free [themes](/nnw-themes).
