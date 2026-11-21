---
layout: post
date: 2026-11-20 23:06
title: SecOpsNews - SBOM script (python) Version v1.1.0
seo_title: SecOpsNews - SBOM script (python) Version v1.1.0 Release
seo_description:
  "Release notes for SecOpsNews - SBOM script (python) version v1.1.0:
  Add osv check.py , which checks an SBOM against OSV.dev and lists known vulnerabilities..."
type: release
cited: GitHub
link: https://github.com/SecOpsNews/script_sbom.py/releases/tag/v1.1.0
release_id: tag:github.com,2008:Repository/1465939704/v1.1.0
release_repo: script_sbom.py
release_project: secopsnews-sbom-script-python
release_version: v1.1.0
---

## About

A Python script that scans a folder's dependency manifests and lock files and writes a CycloneDX 1.6 `sbom.json`, then checks it for known vulnerabilities with OSV.dev. Python standard library only.

## What's Changed

- Add `osv_check.py`, which checks an SBOM against OSV.dev and lists known vulnerabilities by severity, with each CVE and the versions that fix it
- Bump softprops/action-gh-release from 2 to 3
- Bump actions/checkout from 4 to 7

[Read more about my projects](/projects)
