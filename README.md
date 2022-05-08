# Site

[![Code QL](https://github.com/MatBenfield/TheChels.uk/actions/workflows/codeql-analysis.yml/badge.svg)](https://github.com/MatBenfield/TheChels.uk/actions/workflows/codeql-analysis.yml) [![Lighthouse](https://github.com/MatBenfield/TheChels.uk/actions/workflows/lighthouse.yml/badge.svg)](https://github.com/MatBenfield/TheChels.uk/actions/workflows/lighthouse.yml) [![Link Checker](https://github.com/MatBenfield/TheChels.uk/actions/workflows/link-checker.yml/badge.svg)](https://github.com/MatBenfield/TheChels.uk/actions/workflows/link-checker.yml) [![Linter](https://github.com/MatBenfield/TheChels.uk/actions/workflows/linter.yml/badge.svg)](https://github.com/MatBenfield/TheChels.uk/actions/workflows/linter.yml) 

[![Morning Run](https://github.com/MatBenfield/TheChels.uk/actions/workflows/morning-run.yml/badge.svg)](https://github.com/MatBenfield/TheChels.uk/actions/workflows/morning-run.yml) [![Publish Post](https://github.com/MatBenfield/TheChels.uk/actions/workflows/issue-to-post.yml/badge.svg)](https://github.com/MatBenfield/TheChels.uk/actions/workflows/issue-to-post.yml) [![Update Data Files](https://github.com/MatBenfield/TheChels.uk/actions/workflows/update-data.yml/badge.svg)](https://github.com/MatBenfield/TheChels.uk/actions/workflows/update-data.yml) [![pages-build-deployment](https://github.com/MatBenfield/TheChels.uk/actions/workflows/pages/pages-build-deployment/badge.svg)](https://github.com/MatBenfield/TheChels.uk/actions/workflows/pages/pages-build-deployment)

A blog hosted on GitHub available at TheChels.uk. The site uses Jekyll, a static site generator, on Ruby. DNS and SSL by Cloudflare. It also uses GitHub actions, GitHub issues, and Python for extensive automation.

It is called "weak notes" as play on words of the popular "week notes" blogging style - due to the likelihood I will be inconsistent and therefore weak at it.

## Morning

In order for the page to work you need to enter some secrets for the repository. There are also a bunch of config files (json) that need updating to suit your needs.

1. An open weather API key - you can register for a free account on their website.
2. Latitude and Longitude for the weather API.
3. Update stocks.json with the ticker ids for the stocks you want prices for.
4. Update comps.json with the list of competition slugs used by the BBC in order to get the relevant football fixtures 
5. Update quotes.json with your favourite quotes.
