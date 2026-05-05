---
layout: jokes
title: Jokes
permalink: /jokes
seo: collection of jokes written by thechelsuk
---

This page is a collection of jokes that I have written over the years. They are all original as far as I can tell.

{% for item in site.data.jokes %}

> {{item}}

{% endfor %}
