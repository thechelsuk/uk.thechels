---
layout: pages
title: Architecture - Website Technology Stack and Build
permalink: /architecture
seo: Architecture page for thechels.uk
---

Hosted on [GitHub Pages](https://pages.github.com), the site uses [Jekyll](https://jekyllrb.com), a static site generator, on [Ruby](https://www.ruby-lang.org/en/) using the [liquid templating language](https://shopify.github.io/liquid/). It also uses GitHub Actions and [Python](https://www.python.org) for automation and additional compute at build time. Content is written in GitHub flavoured [Markdown](https://daringfireball.net/projects/markdown/). Data is stored in [Yaml](https://yaml.org) files. DNS and SSL by [Cloudflare](https://www.cloudflare.com). [VSCode for Mac](https://code.visualstudio.com/) as the IDE, supported by various plugins. [Working Copy](https://workingcopy.app/) on iOS as the Git client of choice. [Drafts](https://getdrafts.com/) App as the starting point for content creation.

The site is a [progressive web app](https://developer.mozilla.org/en-US/docs/Web/Progressive_web_apps) (PWA) and can be installed on devices from modern browsers. There is no cookies or tracking other than some of the CloudFlare protection and RUA. The site builds as static html and css, uses browser and Cloudflare caching and scores highly in performance scanning tools and in Lighthouse scores with 100% across the board. At the time of checking the site has [valid HTML](https://validator.w3.org/nu/?doc=https%3A%2F%2Fthechels.uk%2F) and [valid CSS](https://jigsaw.w3.org/css-validator/validator?uri=https%3A%2F%2Fthechels.uk&profile=css3svg).

The site is structured as follows:

- **`_pages`**: Contains all the markdown files for individual pages, such as `architecture.md` and `daily.md`. These files define the content and metadata for each page.
- **`_data`**: Stores YAML files that provide structured data for the site, such as configuration settings, lists, or other reusable data.
- **`_includes`**: Contains reusable HTML snippets, such as headers, footers, or other components that can be included in multiple layouts or pages.
- **`_layouts`**: Defines the templates for different types of pages, such as `default`, `post`, or `page` layouts. These templates determine the overall structure of the site.
- **`_posts`**: Holds blog posts or time-sensitive content, organized by date in the filename (e.g., `2025-04-06-example-post.md`).
- **`_site`**: The output directory where the generated static site is built. This folder is created during the build process and should not be edited directly.
- **`_config.yml`**: The main configuration file for the Jekyll site, where global settings like site title, description, and plugins are defined. This includes the menus as key value pairs of title and link.

This structure allows for modular and maintainable development, with clear separation of content, data, and presentation.

![architecture](/images/architecture.png)

This diagram illustrates the following:

1. **GitHub Repository**: Contains the source code for the Jekyll site, including configuration, content, and assets.
2. **Jekyll Build Process**: Converts the source code into a static site.
3. **Static Site (_site folder)**: The output of the Jekyll build process, containing HTML, CSS, and other static files.
4. **GitHub Pages Server**: Hosts and serves the static site.
5. **Browser**: Users access the site through their web browsers.
