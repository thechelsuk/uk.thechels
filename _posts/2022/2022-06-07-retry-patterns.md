---
layout: post
date: 2022-06-07
link: https://blog.bytebytego.com/p/retry-patterns-episode-9
title: Retry Patterns - Software Resilience and Error Handling
seo_title: "Retry Patterns - Exponential Backoff With Jitter"
seo_description: "Linking ByteByteGo on retry patterns for resilient software, including exponential backoff with jitter to spread retries and avoid overload."
type: linked
cited: Alex Xu
---

> Exponential backoff with jitter. If all the failed calls back off at the same time, they cause contention or overload again when they retry. Jitter adds some amount of randomness to the backoff to spread the retries.
