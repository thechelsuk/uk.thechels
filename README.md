# Site

A blog hosted on GitHub is available at TheChels.uk. The site uses Jekyll, a static site generator, on Ruby. DNS and SSL by Cloudflare. It also uses GitHub actions, GitHub issues, and Python for extensive automation.

It is called "weak notes" as a play on words of the popular "week notes" [blogging style](https://weeknot.es/) - 
due to the likelihood, I will have an inconsistent and irregular cadebce for posting.

## Badges

<details><summary><code>Quality Control</code></summary>

  [![Run tests](https://github.com/Mat-0/TheChels.uk/actions/workflows/python-ci.yml/badge.svg)](https://github.com/Mat-0/TheChels.uk/actions/workflows/python-ci.yml)
  [![CodeQL](https://github.com/Mat-0/TheChels.uk/actions/workflows/codeql.yml/badge.svg)](https://github.com/Mat-0/TheChels.uk/actions/workflows/codeql.yml) 
  [![Lighthouse](https://github.com/Mat-0/TheChels.uk/actions/workflows/lighthouse.yml/badge.svg)](https://github.com/Mat-0/TheChels.uk/actions/workflows/lighthouse.yml) 
  [![Link Checker](https://github.com/Mat-0/TheChels.uk/actions/workflows/link-checker.yml/badge.svg)](https://github.com/Mat-0/TheChels.uk/actions/workflows/link-checker.yml) 
  [![Linter](https://github.com/Mat-0/TheChels.uk/actions/workflows/linter.yml/badge.svg)](https://github.com/Mat-0/TheChels.uk/actions/workflows/linter.yml) 
  [![Clear Cache](https://github.com/Mat-0/TheChels.uk/actions/workflows/clear-cache.yml/badge.svg)](https://github.com/Mat-0/TheChels.uk/actions/workflows/clear-cache.yml) 
  [![Pages](https://github.com/Mat-0/TheChels.uk/actions/workflows/pages/pages-build-deployment/badge.svg)](https://github.com/Mat-0/TheChels.uk/actions/workflows/pages/pages-build-deployment) 
</details>

<details><summary><code>Content Management</code></summary>

  [![Add Book](https://github.com/Mat-0/TheChels.uk/actions/workflows/add-book.yml/badge.svg)](https://github.com/Mat-0/TheChels.uk/actions/workflows/add-book.yml) 
  [![Add Now and Next](https://github.com/Mat-0/TheChels.uk/actions/workflows/add-next.yml/badge.svg)](https://github.com/Mat-0/TheChels.uk/actions/workflows/add-next.yml) 
  [![Add Offers](https://github.com/Mat-0/TheChels.uk/actions/workflows/add-offers.yml/badge.svg)](https://github.com/Mat-0/TheChels.uk/actions/workflows/add-offers.yml) 
  [![Add Post](https://github.com/Mat-0/TheChels.uk/actions/workflows/add-post.yml/badge.svg?event=issues)](https://github.com/Mat-0/TheChels.uk/actions/workflows/add-post.yml) 
  [![Add Podcast](https://github.com/Mat-0/TheChels.uk/actions/workflows/add-podcast.yml/badge.svg)](https://github.com/Mat-0/TheChels.uk/actions/workflows/add-podcast.yml) 
  [![Add Quotes](https://github.com/Mat-0/TheChels.uk/actions/workflows/add-quotes.yml/badge.svg)](https://github.com/Mat-0/TheChels.uk/actions/workflows/add-quotes.yml) 
  [![Add Stock](https://github.com/Mat-0/TheChels.uk/actions/workflows/add-stock.yml/badge.svg)](https://github.com/Mat-0/TheChels.uk/actions/workflows/add-stock.yml) 
</details>

## Configuration
There are several optional settings for you to configure. Use the example `_config.yml` file in the repo and use the documentation below to configure your site:

<details><summary><code>Config</code></summary>

  ### Using includes
  There are 2 main includes: one for the header and one for the footer, largely to minimise repetition.

  ### Using layouts

  Layouts are almost one-to-one with pages, handling any page specifics. `post.html` is the layout used for every blog post. There are also default templates and an empty template used for `scss` and other special pages such as `humans.txt`

 ### Using Data

  Data files power many aspects of the site and these are updated via issues and GitHub Actions.

  ### Site navigation

  Using configuration yml, navigation is provided by three collections for `header`, `footer`, and `around_the_web` (on the about page) and are fairly self-explanatory.
</details>
