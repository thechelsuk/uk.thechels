# Website

A blog/website hosted on Github available at TheChels.uk. The site uses Jekyll, a static site generator, on Ruby. SSL by Cloudflare. It also uses GitHub actions extensively running python scripts.

It is called weak notes as play on words of the popular 'week notes' blogging style - due to the likelihood I will be inconsistent.

## Morning

In order for this solution to work you need to enter some secrets for the repo (or hard-code the values in the scripts if you don't care). There are also a bunch of config files (json) that need updating to suit your needs.

1. An open weather API key - you can register for a free account on their website.
2. Latitude and Longitude for the weather API.
3. Update stocks.json with the ticker ids for the stocks.
4. Update tournaments.json with the list of competition slugs used by the BBC in order to get the relevant football fixtures 
5. Update quotes.json with your favourite quotes.
