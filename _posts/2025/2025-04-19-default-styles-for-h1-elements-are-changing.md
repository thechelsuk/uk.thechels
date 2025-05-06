---

layout: post
date: 2025-04-19
link: https://developer.mozilla.org/en-US/blog/h1-element-styles/
title: Default styles for h1 elements are changing
cited: MDN

---

> Browsers are starting to roll out changes in default UA styles for nested section headings. Developers should check that their sites don't rely on UA styles for certain cases to avoid unexpected results and failing Lighthouse checks. In this post, we'll have a look at what the incoming changes are, how to identify if it's an issue on your pages, and some hints for conformant and better-structured websites.

> What's changing
> The HTML spec used to define an outline algorithm that gave <h1> elements an implicit semantic heading level based on how many sectioning elements (<section>, <aside>, <nav>, and <article>) it was nested inside.
