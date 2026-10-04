---
layout: projects
title: "Track a RSS/Atom feed on GitHub - Template Repo"
seo_title: "RSS and Atom Feed Archiver - GitHub Template Repo"
seo_description: "A GitHub template repo that archives any RSS or Atom feed into a _data folder on a daily GitHub Actions schedule, committing new items as they appear."
permalink: /projects/create-archive-of-feed-on-github-with-this-template
class: templates
i_name: View
i_url: "https://github.com/thechelsuk/template-feed-archiver"
summary: "A Repo template for monitoring and archiving a feed."
type: template
---

A GitHub template repository setup to copy an rss or atom feed into a `_data` folder in a repo for monitoring and archiving purposes.

- Simply copy the repo.
- Change the `daily.yml` action to include the feed url and the output file name
- GitHub Action runs on a daily schedule and will commit any new updates into the repo.
