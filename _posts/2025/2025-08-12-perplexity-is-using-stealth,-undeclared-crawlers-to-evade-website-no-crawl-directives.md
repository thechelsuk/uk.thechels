---

layout: post
date: 2025-08-12
link: https://blog.cloudflare.com/perplexity-is-using-stealth-undeclared-crawlers-to-evade-website-no-crawl-directives/
title: Perplexity is using stealth, undeclared crawlers to evade website no-crawl directives
cited: Cloudflare

---

> We are observing stealth crawling behavior from Perplexity, an AI-powered answer engine. Although Perplexity initially crawls from their declared user agent, when they are presented with a network block, they appear to obscure their crawling identity in an attempt to circumvent the website's preferences. We see continued evidence that Perplexity is repeatedly modifying their user agent and changing their source [_ASNs_](https://www.cloudflare.com/learning/network-layer/what-is-an-autonomous-system/) to hide their crawling activity, as well as ignoring -- or sometimes failing to even fetch -- _[robots.txt_ ](https://www.cloudflare.com/learning/bots/what-is-robots-txt/)files.

> The Internet as we have known it for the past three decades is [_rapidly changing_](https://blog.cloudflare.com/content-independence-day-no-ai-crawl-without-compensation/), but one thing remains constant: it is built on trust. There are clear preferences that crawlers should be transparent, serve a clear purpose, perform a specific activity, and, most importantly, follow website directives and preferences. Based on Perplexity's observed behavior, which is incompatible with those preferences, we have de-listed them as a verified bot and added heuristics to our managed rules that block this stealth crawling.