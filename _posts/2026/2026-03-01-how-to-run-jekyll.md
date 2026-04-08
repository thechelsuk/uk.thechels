---
layout: post
title: How to run Jekyll locally
seo: Ways - run Jekyll locally
tag: ways
date: 2026-03-01
type: ways

---

- Clone the repository:

   ```bash
   git clone your_repo_url
   ```

- Navigate into the project directory:

   ```bash
   cd repo_name
   ```

- Install the required dependencies:

   ```bash
   bundle install
   ```

- Build the site:

   ```bash
   bundle exec jekyll build
   ```

- Build and serve the site locally:

   ```bash
   bundle exec jekyll serve --watch
   ```

- Open your browser and go to `<http://localhost:4000>` to see your site.

- To stop the server, press `Ctrl + C` in the terminal.

_Make sure you have Ruby and Bundler installed on your machine before running these commands._

- If you don't have a gemfile and bundler, you should just be able to run:

   ```bash
   jekyll serve --watch
   ```

This will start the Jekyll server and watch for changes in your files, allowing you to see updates in real-time as you edit your site.
