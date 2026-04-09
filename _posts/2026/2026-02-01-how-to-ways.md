---
layout: post
title: How to use ways
seo: Ways - A guide to using ways
date: 2026-02-01
type: ways
pinned: true

---

Ways are a slash pages format for documenting processes, workflows, and procedures. They are designed to be easy to read and follow, on how to do things. They happen to include a link to the official manual or service where possible, but there should be enough detail to follow steps without needing to click through.

1. Create a new markdown file in the `_ways` directory. The filename should be descriptive of the process you are documenting, for example `how-to-use-ways.md`.
2. Start the file with the following front matter:

    ```markdown
    ---
    layout: post
    title: How to use ways
    seo: Ways - A guide to using ways
    type: ways
    permalink: /ways/use-ways/
    date: 2026-02-01
    pinned: true/false
    ---
    ```

3. Customize the front matter with the appropriate title, SEO description, type, permalink, and date for your specific way, use pinned as true if you want the way to be featured at the top of the ways archive page, otherwise set it to false or omit it.
4. After the front matter, you can start writing your content. Use headings, lists, and other markdown formatting to make it easy to read and follow.
5. Save the file and commit it to your repository. The new way will be available at the specified permalink, in this case `/ways/use-ways/`.

_I've refrained from using screenshots of apps or tools in ways as apps and designs can change frequently, whereas functionality, hopefully, persists._

I've also updated the Jekyll config to include `_ways` as a collection, so you can use the site data variables to access all the ways in your templates and layouts and metadata like the front matter and count of items etc.

The output in the config is set to 'true' so the files are generated, however they are not included in any RSS feed output as they are not timely in that sense. This differs to the RSS only feed that has generation turned off so the webpages don't exist but the RSS feed is still generated with the content.
