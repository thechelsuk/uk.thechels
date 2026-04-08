---
layout: post
title: How to create various data types for thechelsuk
seo: Ways - create data types for thechelsuk
tag: ways
date: 2026-03-01
type: ways

---

This site has various data types, each with their own format and process for creation. Below are the steps to create each type of data.

## Add a Film

- In Drafts;
  - create a new draft with the film template add a film title on the first line
  - Run action to search film to get the correct IMDB ID it'll be added to the draft automatically
  - Add the rating in the placeholder
  - Run the  `Add Film` action which will trigger the GitHub Action workflow.

- Or;
  - On Mac; Run the python script typing in a Film IMDB code and a Rating.
  - In the browser; Run a workflow dispatch - entering the inputs film IMDB and Rating

## Add a Book

- Run a workflow dispatch - entering the ISBN
- Download the cover image
- Resize to a height of 183px
- Save the cover image into the `images/books` folder ensuring the name matches the format `book-[isbn].png`
- Push a commit to Prod

## Other types

- Add a row to the yaml file as needed.
- Push a commit to Prod in working copy or VS Code.
