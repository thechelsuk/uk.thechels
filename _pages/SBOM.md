---

title : Software Bill of Materials (SBOM)
layout: page
date: 2026-04-27
robots: noindex, nofollow
permalink: /SBOM
seo: Software Bill of Materials (SBOM) for thechelsuk website
---

## Overview

This document lists all software dependencies used on this website, including both Ruby gems for Jekyll and Python packages for utility scripts.

Last updated: 2026-04-27

## Ruby Gems (Jekyll Dependencies)

The following Ruby gems are used for the Jekyll static site generator:

| Gem Name | Version | Description |
| ---------- | ---------: | ------------- |
| activesupport | 7.2.3.1 | Ruby gem |
| addressable | 2.9.0 | Ruby gem |
| base64 | 0.3.0 | Ruby gem |
| benchmark | 0.5.0 | Ruby gem |
| bigdecimal | 4.1.2 | Ruby gem |
| colorator | 1.1.0 | Ruby gem |
| concurrent-ruby | 1.3.6 | Ruby gem |
| connection_pool | 3.0.2 | Ruby gem |
| csv | 3.3.5 | Ruby gem |
| date | 3.5.1 | Ruby gem |
| domain_name | 0.6.20240107 | Ruby gem |
| drb | 2.2.3 | Ruby gem |
| em-websocket | 0.5.3 | Ruby gem |
| eventmachine | 1.2.7 | Ruby gem |
| execjs | 2.10.1 | Ruby gem |
| faraday | 2.14.1 | Ruby gem |
| faraday-net_http | 3.4.2 | Ruby gem |
| faraday-retry | 2.4.0 | Ruby gem |
| ffi | 1.17.4-x86_64-linux-musl | Ruby gem |
| ffi-compiler | 1.3.2 | Ruby gem |
| forwardable-extended | 2.6.0 | Ruby gem |
| google-protobuf | 4.34.1-x86_64-linux-musl | Ruby gem |
| htmlbeautifier | 1.4.3 | Ruby gem |
| http | 5.3.1 | Ruby gem |
| http-cookie | 1.1.6 | Ruby gem |
| http-form_data | 2.3.0 | Ruby gem |
| i18n | 1.14.8 | Ruby gem |
| indieweb-endpoints | 8.0.0 | Ruby gem |
| jekyll | 4.4.1 | Ruby gem |
| jekyll-avatar | 0.8.0 | Ruby gem |
| jekyll-github-metadata | 2.16.1 | Ruby gem |
| jekyll-sass-converter | 3.1.0 | Ruby gem |
| jekyll-sitemap | 1.4.0 | Ruby gem |
| jekyll-watch | 2.2.1 | Ruby gem |
| jekyll-webmention_io | 4.1.0 | Ruby gem |
| json | 2.19.4 | Ruby gem |
| jsonpath | 1.0.7 | Ruby gem |
| kramdown | 2.5.2 | Ruby gem |
| kramdown-parser-gfm | 1.1.0 | Ruby gem |
| link-header-parser | 5.1.1 | Ruby gem |
| liquid | 4.0.4 | Ruby gem |
| listen | 3.10.0 | Ruby gem |
| llhttp-ffi | 0.5.1 | Ruby gem |
| logger | 1.7.0 | Ruby gem |
| mercenary | 0.4.0 | Ruby gem |
| mini_portile2 | 2.8.9 | Ruby gem |
| minitest | 5.27.0 | Ruby gem |
| multi_json | 1.20.1 | Ruby gem |
| net-http | 0.9.1 | Ruby gem |
| nokogiri | 1.19.2-x86_64-linux-musl | Ruby gem |
| octokit | 6.1.1 | Ruby gem |
| openssl | 3.3.2 | Ruby gem |
| pathutil | 0.16.2 | Ruby gem |
| psych | 5.3.1 | Ruby gem |
| public_suffix | 7.0.5 | Ruby gem |
| racc | 1.8.1 | Ruby gem |
| rake | 13.4.2 | Ruby gem |
| rb-fsevent | 0.11.2 | Ruby gem |
| rb-inotify | 0.11.1 | Ruby gem |
| rexml | 3.4.4 | Ruby gem |
| rouge | 4.7.0 | Ruby gem |
| safe_yaml | 1.0.5 | Ruby gem |
| sass-embedded | 1.99.0-x86_64-linux-musl | Ruby gem |
| sawyer | 0.9.3 | Ruby gem |
| securerandom | 0.4.1 | Ruby gem |
| stringio | 3.2.0 | Ruby gem |
| terminal-table | 3.0.2 | Ruby gem |
| tzinfo | 2.0.6 | Ruby gem |
| tzinfo-data | 1.2026.1 | Ruby gem |
| uglifier | 4.2.1 | Ruby gem |
| unicode-display_width | 2.6.0 | Ruby gem |
| uri | 1.1.1 | Ruby gem |
| wdm | 0.2.0 | Ruby gem |
| webmention | 7.0.0 | Ruby gem |
| webrick | 1.9.2 | Ruby gem |

**Total Ruby Gems:** 75

## Python Packages

The following Python packages are used for utility scripts and data processing:

| Package Name | Type | Usage |
| -------------- | ------ | ------- |
| argparse | Python package | Command-line argument parsing |
| datefinder | Python package | Date extraction from text |
| feedparser | Python package | RSS/Atom feed parsing |
| lxml | Python package | Python package |
| lxml_html_clean | Python package | HTML cleaning utilities |
| markdownify | Python package | Python package |
| pandas | Python package | Data manipulation and analysis |
| pathlib | Python package | Object-oriented filesystem paths |
| pillow | Python package | Image processing library |
| pytest | Python package | Testing framework |
| pytest-cov | Python package | Test coverage reporting |
| pytest-emoji | Python package | Emoji support for pytest |
| pytest-md | Python package | Markdown output for pytest |
| pyyaml | Python package | YAML file processing |
| requests | Python package | HTTP library for API calls |
| requests_html | Python package | HTML parsing with JavaScript support |
| ruamel.yaml | Python package | Advanced YAML processing |
| yahoo_fin | Python package | Yahoo Finance data retrieval |
| yapf | Python package | Python code formatter |
| yfinance | Python package | Yahoo Finance data access |

**Total Python Packages:** 20

## Summary

- **Ruby Gems:** 75 packages
- **Python Packages:** 20 packages
- **Total Dependencies:** 95 packages

## Package Managers

- **Ruby:** Bundler (via Gemfile)
- **Python:** pip (via requirements.txt)

## Security Notes

All dependencies are managed through their respective package managers and should be regularly updated to address security vulnerabilities. The project uses:

- `bundle audit` for Ruby gem security checking
- `pip-audit` for Python package security checking (recommended)


