---
layout: post
title: How to create a custom GitHub issues template
tag:
 - dev
---

Having recently created and updated the new [ReadMe template homepage](https://github.com/Mat-0) on GitHub, I posed a question on what I should be looking at next.

Then I paused for a moment and thought about how someone might want to communicate with me. Being on GitHub creating a [new issue](https://github.com/Mat-0/Mat-0/issues/new/choose) would make sense, So I created a link to [the issues page](https://github.com/Mat-0/Mat-0/issues/new/choose). However I would want these items kept separate from other issues related to code/bugs i.e. genuine issues.

GitHub allows you to create custom templates and they get stored in `ISSUE_TEMPLATE` folder stored in a `.GitHub` folder in [your repository](https://github.com/Mat-0/Mat-0/tree/main/.github/ISSUE_TEMPLATE).

Creating a new template is as easy as clicking the _add new file_ button and providing some markdown

<script src="https://gist.github.com/Mat-0/2bcfc2a4db0427f802585c047602bc95.js"></script>

You can automatically assign issues to a user, and give it a label `Next` in my example, pretty neat huh.

As the `.GitHub` folder and contents are stored in the repository they benefit from source control, so you can edit them in your IDE of choice, commit, create pull requests and all that good stuff.
