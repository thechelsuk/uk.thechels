---
layout: post
date: 2022-09-17
link: https://jvns.ca/blog/2022/09/12/why-do-domain-names-end-with-a-dot-/
title: Why do domain names sometimes end with a dot?
seo_title: "Why Do Domain Names Sometimes End With a Dot?"
seo_description: "Linking Julia Evans on why domain names in DNS zone files and dig output end with a trailing dot, marking them as fully qualified, not relative."
type: linked
cited: Julia Evans
---

> This also explains why there’s a . at the end of example.com. – zone files require a trailing dot at the end of a domain name (because otherwise they’re interpreted as being relative to the zone). So dig does too.
>
> I really wish dig had a +human flag that printed out all of this information in a more human readable way, but for now I’m too lazy to put in the work to actually contribute code to do that (and I’m a pretty bad C programmer) so I’ll just complain about it on my blog instead :)
