---
layout: post
date: 2025-04-28
title: RSS Feed Generation

---


I’ve been building out some RSS feeds recently as I really value the nature of RSS delivery in a reader of my choice, rather than being forced to go to websites full of adverts and cookie notices, or forced into apps that also are full of apps, despite being paid for - looking at you Apple News - So here is a code snippet that can take any markdown file, render the content into an item in an RSS feed. The front matter ensures Jekyll builds it and processes the variables.

The will produce a daily feed (as the pub date has no timestamp, and will be triggered by other builds or activity on the repo.

```markdown

—
—
{% assign contents_of_page = site.pages | where: “name”, “index.md” | first %}
{% assign pub_date = site.time | date: “%Y-%m-%d” %}

<?xml version=“1.0” encoding=“UTF-8” ?>
<rss version=“2.0”>
<channel>
<title>Title</title>
<link>page link</link>
<description>Description</description>
<item>
<title>Title {{ pub_date }}</title>
<link>[url]</link>
<guid isPermaLink=“false”>Daily Rundown for {{ pub_date }}</guid>
<description>
<![CDATA[ {{ contents_of_page.content | markdownify }} ]]>
</description>
<pubDate>{{ pub_date }}</pubDate>
</item>
</channel>
</rss>

```