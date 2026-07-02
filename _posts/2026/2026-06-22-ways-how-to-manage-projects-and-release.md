---
layout: post
title: How to manage website projects and releases
seo: Ways - how to manage website projects and releases
date: 2026-06-22 23:00
syndicate: true
type: ways
---

## Releases Yaml

Update the releases.yml file in the `_data` folder with the new release feed url. This will allow the website to display the latest releases as new blog posts, A GitHub action polls for feed changes and creates new posts automatically.

```yaml
- id: text label (as shown as blog post title)
  url: url/to/releases.atom
```

## Projects Page

Add a new post to the `_projects` collection folder with the following front matter:

```yaml
---
layout: projects
title: some-title
permalink: /projects/some-title
seo: "Some Title"
class: scripts
i_name: View
i_url: "repo-url"
summary: "A short description of the project."
type: wrench
---
Description of the project, as post content
```

the type is the icon used on the projects page, the class is the category of the project and these are grouped on the projects page.
The i_name and i_url are the icon name and url for the project link at the bottom of the post page.
