---

layout: post
date: 2026-04-04 12:00
link: https://stuartbreckenridge.net/2026-04-03-the-bbcs-rss-feed/
title: The BBC RSS Feeds are garbage
cited: Stuart Breckenridge

---

This must be due to the unique way the Beeb is funded. 

I stopped subscribing to all BBC feeds because of this very reason, many, many moons ago.

I love RSS and more so given my accessibility needs so to see and be reminded of how it is abused this way is frustrating 

> Due to the _incorrect_ way the BBC's [RSS 2.0 feed](http://feeds.bbci.co.uk/news/uk/rss.xml) handles `guid`s, RSS readers are repeatedly left displaying [duplicate articles](https://discourse.netnewswire.com/t/duplicates-of-the-articles/202).

> Let's have a look at why this happens with a sample article from their feed

***

> Gobbler has fetched this article three times. The **article hasn't changed** at all: same title, same content, and same published date1, all validated by the `content_hash`. This is simply not justifiable. There is no reason to change the `guid` if the article hasn't changed.