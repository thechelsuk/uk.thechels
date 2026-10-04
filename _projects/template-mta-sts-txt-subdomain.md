---
layout: projects
title: "Create mta-sts.txt and subdomain on GitHub Pages - Template Repo"
seo_title: "MTA-STS on GitHub Pages - Template Repo for mta-sts.txt"
seo_description: "A GitHub template repo to host an mta-sts.txt policy on an mta-sts subdomain with GitHub Pages: copy it, set CNAME and MX records, then add DNS."
permalink: /projects/create-mta-sts-txt-subdomain-on-github-pages-template
class: templates
i_name: View
i_url: "https://github.com/thechelsuk/template-mta-sts-sub-domain"
summary: "A Repo template for creating an mta-sts.txt record and subdomain hosted on GitHub Pages using their branch deployment."
type: template
---

A GitHub template repository setup to quickly deploy an `mta-sts.txt` file into a `.well-known/mta-sts.txt` path on a `mta-sts.domain.tld` subdomain.

- Simply copy the template repo.
- Change the CNAME.txt file contents to mta-sts.yourdomain.tld
- Rename CNAME.txt to just CNAME1
- Change the .well-known/mta-sts.txt file to match your email MX records and version2
- Set up the DNS records to point to GitHub's IP ranges.
  - 185.199.108.153
  - 185.199.109.153
  - 185.199.110.153
  - 185.199.111.153
- Publish to GitHub Pages - using the deploy from branch fine, no actions needed.

Default mta-sts config is for Apple's MX records - change these to your provider.
