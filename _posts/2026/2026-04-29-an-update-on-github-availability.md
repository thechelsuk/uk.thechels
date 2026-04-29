---

layout: post
date: 2026-04-29 15:07
title: An update on GitHub availability
link: https://github.blog/news-insights/company-news/an-update-on-github-availability/#h-recent-incidents
cited: GitHub
type: linked

---

Yikes, it's been a pretty terrible week or so for GitHub.

Worth noting that:

1. Pull requests are bad, don't use them for non-open source projects, and only for open source projects where contributions become a problem.
2. GitHub has had a huge spike in usage this year given the near ubiquitous accessibility of AI coding tools.

> Pull requests merged through merge queue using the squash merge method produced incorrect merge commits when a merge group contained more than one pull request. In affected cases, changes from previously merged pull requests and prior commits were inadvertently reverted by subsequent merges.
> 
> During the impact window, 658 repositories and 2,092 pull requests were affected. We initially shared slightly higher numbers because our first assessment was intentionally conservative. The issue did not affect pull requests merged outside merge queue, nor did it affect merge queue groups using merge or rebase methods