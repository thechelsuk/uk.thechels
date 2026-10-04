---
layout: jokes
title: Jokes
seo_title: "Jokes - Original One-Liners and Puns by thechelsuk"
seo_description: "A collection of original jokes, one-liners and puns written by thechelsuk over the years. As far as I can tell, every one of them is my own creation."
permalink: /jokes
---

This page is a collection of jokes that I have written over the years. They are all original as far as I can tell.

{% for item in site.data.jokes %}

> {{item}}

{% endfor %}
