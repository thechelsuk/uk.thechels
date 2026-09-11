---
layout: post
date: 2026-09-12 10:00
title: Shortkeys Version 1.3.0
type: release
cited: GitHub
link: https://thechels.uk/projects/shortkeys
release_version: 1.3.0
---

## About

ShortKeys is a text-expander multi-line replacement productivity app for people who live in text. Build multi-line snippets, drop them behind memorable keyboard ShortKeys, and fly through forms, support replies, or daily journaling.

## What's Changed

- New icon
- Big refactor and tidy up
- Fix keyboard crash + review blockers, tighten cross-process sync
- Dedupe replacement search/filter; add unit test target
- Keyboard: reliable triggers, safer backspace repeat, lighter redraws
- Polish: cancelled-tip alert, NavigationStack, home card, debug logging
- Consolidate shared code between the app and keyboard targets
- Auto-assign a newly created tag to the ShortKey being edited
- Data safety: stop tests touching real data; heal lost/orphaned tags
- Make SharedConstants non-isolated

[Read more about my projects](/projects)
