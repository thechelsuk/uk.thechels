---

layout: post
syndicate: true
date: 2026-07-05 16:43
title: A Method For Quoteblogs
link: https://frankmcpherson.blog/2026/07/04/a-method-for-quoteblogs.html
cited: Frank McPherson
type: linked

---

Love reading about how others handle their processes for managing content.

I use [Drafts](https://getdrafts.com) and use their capture tool template set up to capture the title, link, date, plus quoting whatever I have highlighted on the page. Placeholders for author and some commentary allows me to use the up/down arrows in the tool bar to cycle through  them (it highlights and replaces it when i type).

```text
Weak Notes by thechelsuk

<|commentary>

> Hello, hello. Welcome in to my working out loud and in public second brain from your favourite software engineering people leader

Link: https://thechels.uk
Cited: <|cited>
Date: 2026-07-05 22:00

``` 

I have a publish action written in JavaScript which does some rewriting of content into the front matter and markdown structure I need. This script prompts me to choose the post type whether it’s a quote, or just a regular blog - I have some other actions that generate content into Drafts like my music mixtapes. 

The action allows me to choose it it’s going to be sent to indienews, or socials, be shown on my homepage or hidden. 

Drafts has to be one of the most powerful apps on the Apple platform given its versatility for things like this.


> My quoteblog posts originate from the highlights I store in Readwise. Readwise provides the ability to tag articles, or what it calls documents, and tag individual highlights. I give the source article of the quotes a “blog-post” tag and the highlights to share a “quote” tag in Readwise. Claude then wrote the code that reviews the articles that I pinned looking for ones with a “blog-post” document tag and when it finds one, it puts thee article title, author, and source URL in a markdown file. Highlights that have a “quote” tag are then added to the markdown file.