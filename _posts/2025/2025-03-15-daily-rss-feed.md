---
layout: post
title: Daily RSS Feed
seo: How I built a daily page and RSS feed in Jekyll
date: 2025-03-15

---

I have been producing a [daily rundown](/daily) using some scheduled python scripts for a while now. I use a shortcut on my iOS to alert and then open this webpage on a schedule (at sunrise).

However, I am almost always end up in my RSS reader of choice so thought about how I can make an RSS feed published through Jekyll's build process.

Pages are normally static and posts are like a blog and are typically shown in RSS feeds as a new item. So this was a little trickier than anticipated as I needed to find the page and pull it's content using the `assign` method in the Liquid syntax. I was then able to put together a pretty simple xml file.

I've included the `site.time` to process a date in the title and also in the pubDate so this should trigger a new feed everyday... Perhaps I'll need to monitor if this changes on every build, but at best case it'll be daily when the page changes, worst case it might be sent to my RSS reader multiple times a day with the same content. Perhaps changing the PubDate to just have a fixed time might solve that... lets experiment.


```xml

---
---
{% assign contents_of_page = site.pages | where: "name", "daily.md" | first %}
{% assign pub_date = site.time | date: "%Y-%m-%d" %}

<?xml version="1.0" encoding="UTF-8" ?>
<rss version="2.0">
  <channel>
    <title>Daily Rundown</title>
    <link>{{ site.url }}/daily</link>
    <description>{{ site.description }}</description>
    <item>
      <title>Daily Rundown for {{ pub_date }}</title>
      <link>{{ site.url }}/daily</link>
      <description>
      <![CDATA[ {{ contents_of_page.content }} ]]>
      </description>
      <pubDate>{{ site.time }}</pubDate>
    </item>
  </channel>
</rss>

```
