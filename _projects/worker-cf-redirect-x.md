---
layout: projects
title: CF Worker X Redirect
permalink: /projects/cf-worker-x--redirect
class: workers
seo: "X.app redirect cloudflare worker"
i_name: GitHub Source
i_url: "https://github.com/thechelsuk/cf-worker-x-redirect"
summary: "A Cloudflare worker to solve a niche problem of redirecting urls to an `x-callback-url` on iOS when an app doesn't support them natively."

---

A Cloudflare Worker project that handles URL redirection. Providing a simple and efficient way to manage redirects at the edge. This project solves a small niche problem for managing videos in NetNewsWire that does not seem to support `x-callback-url` schemes. My themes rewrite URLs to to a subdomain passing the video url as a query parameter and the URL is then handled by this worker, redirecting to an iOS video playing app that supports PIP player via it’s own url scheme. 

The project is open source and available on GitHub under an MIT licence. 

Expected customer base of one.