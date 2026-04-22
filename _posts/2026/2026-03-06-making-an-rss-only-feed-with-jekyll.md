---

layout: post
date: 2026-03-06
title: Making an RSS only feed with Jekyll

type: blog
---

Building on top of the recent work on releasing [1.7](/version-1-7). I am now able to publish a RSS only feed on a Jekyll site, adding a collections property to `config.yml` enables a new data type in my case that is _RSS_ but by also setting the output to false none of the item in the new `_rss` folder get processed or output to the `_site` folder in the deployment. This is a very clever way to manage data and will allow me to post items to my new feed without it appearing on the website or clog it up the main feed.

```yaml
collections:
      RSS:
        output: false
```

I am a big fan of RSS in its indie web roots and its open standard. I consume most content via RSS as it's much more accessible (no flashing adverts, autoplaying videos, sounds, or cookie notices). I wish all sites that have a news/blog/time series based publishing format were mandated to have a feed.

Apparently thanks to Dave Rupert's [RSS Club](https://daverupert.com/rss-club/) I understand I am not alone.
