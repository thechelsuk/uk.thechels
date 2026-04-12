---

layout: post
date: 2026-04-12 04:46
title: TIL - Liquid comparisons are case sensitive
type: TIL
class: indie

---

Turns out, a query like the one below would not cater for Blog == blog.

```liquid
{ assign items = site.posts | where_exp: "post", "post.type == page.type" }
``` 

So the liquid syntax way to handle this is to `upcase` or `downcase` such that the query becomes, with downcasing on both sides.

```liquid
{ assign items = site.posts | where_exp: "post", "post.type | downcase == page.type | downcase" }
```

This query then fetches all posts that match have the front matter post.type that matches the one declared in the page front matter. This means I can use one archive template and use the `archive/blog.md` with the blog `page.type`set  and `archive/work.md` with work set as the `page.type`. This is a lot more effective than having n `archive-type.html` files and have to add one each time a new type is added and be sure to handle each post type in the query. The markdown files are quick and easy