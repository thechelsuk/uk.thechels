---
layout: projects
title: "Publish a Python script - Template Repo"
seo_title: "Python Script Release - GitHub Template Repo"
seo_description: "A GitHub template repo for publishing a Python script, with a config file kept out of git, Dependabot and releases tagged from the package.json version."
permalink: /projects/publish-a-python-script-template
class: templates
i_name: View
i_url: "https://github.com/thechelsuk/template-script-python"
summary: "A Repo template for publishing a Python script, with releases tagged from its version."
type: template
---

A GitHub template repository for publishing a standalone Python script, the starting point for my Python scripts.

It comes with a `config.py.example` for tokens and settings (the real `config.py` is ignored by git), Dependabot for pip and GitHub Actions, an MIT licence, and a release workflow. Raise the version in `package.json` and it tags a release, with notes from my [shared workflows](https://github.com/thechelsuk/workflows): what the script does, then a list of what's changed.

- Use the template to create a new repo.
- Copy `config.py.example` to `config.py` and add any tokens.
- Write the script in `script.py`, and update the README and `package.json` description.
- Raise the `package.json` version to release a change.
