---

layout: post
date: 2026-04-12 02:11
title: Pompidou section 3 - Refactor post types
type: rss

---

After setting up collections on my Jekyll blog for various post types I've refactored to use `post.type` in the post front matter instead of collections.

The main reason is to pump all the content into the `_posts` folder. The idea here is that by default everything will be loaded into the post loop - simplifying the code use for the homepage, which is effectively the archive, and simplifying the code for the main rss feed.

It is trivial to exclude any post type using liquid syntax, for example where the type is RSS where one could choose to publish secretly just to the feed.  This enables the generation of the post html file, it is just excluded from the archives (for collections you can toggle output to false in the config to stop page generation). Taking onboard Dave Rupert's note that content should have a url. I opted for the change. I had found even if a page url was not provided several RSS reader apps default to the site url, so on clicking it would confuse users with the homepage, or worse a 404 page. Also there is an accessibility angle here where the web version might be better than the rss reader (zoom, tabbing, text to speech etc).

So my blog now has post types for mixtapes, today I learned (TIL), ways (how to) as well as regular and linked quote posts and finally those secret posts. 

I've also added a feed for each post type too as again the loop is trivial inside an xml file. I've also added a firehose which adds in the rss from YouTube, mastodon and Bluesky - although the latter two require a hashtag in my post to show up, just in case I don't want it in my feed and on the socials page. Again several loops all being added to a single array ordered by date.

Updating data pages has become easier as `site.posts | size` works well to show the total count. Looping over the `post.frontmatter = value` allows me to do clever things not just `post.type` - quote posts for example can use the `post.cited` as the author and `post.link` as the direct link to the source. I manipulate the post title link on feed readers to link to my blog as the permalink. This is different to how John Gruber handles it at Daring Fireball whereby he includes an under star as the link back to his site in relevant posts.

I think my implementation is better as the author field shows 'quoting x' too to make it super clear it's a linked quote post. The reader can choose to go directly to source by clicking the author or to my website by clicking the title. Check out the [feeds](/feeds) to see it for yourself. This visually works well in NetNewsWire my goto RSS app, but also in a bunch of others I have tested.

Links to archive pages filtered by type are on the [pages](/slages) page and given the variety of my posts, readers can choose to view a filtered list and a dedicated RSS feed.