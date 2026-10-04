---
layout: post
date: 2025-03-26
title: Check Your Public IP Address
seo_title: "Check Your Public IP Address With curl and AWS"
seo_description: "A quick way to check your public IP address: visit checkip.amazonaws.com for a plain text answer, or curl the endpoint from the command line."

type: blog
---

If you visit [https://checkip.amazonaws.com/](https://checkip.amazonaws.com/), a plain text page will render that displays your current public IP address.

Alternatively, you can `cURL` this endpoint from the command line:

    curl https://checkip.amazonaws.com/

Either way, you'll get your IP address.
