---
layout: projects
title: SecOpsNews
seo_title: "SecOpsNews - Security News Dashboard, Feeds and Tools"
seo_description: "A security news, advisory and critical CVE dashboard for engineering leaders, plus open source feeds, a feed to issues template and an SBOM script."
permalink: /projects/secopsnews
class: websites
i_name: Visit
i_url: "https://secops.thechels.uk"
summary: "Security news, advisories, critical CVEs and cloud outages on one dashboard, plus open source security feeds and tools."
type: website
---

SecOpsNews brings security news, government advisories, critical CVEs, data breaches and cloud outages together on one dashboard, for engineering leaders and security professionals. Every item links to its original source. Alongside the dashboard, the [SecOpsNews organisation on GitHub](https://github.com/SecOpsNews) holds the open source feeds and tools behind it, with more to come.

## SecOpsNews dashboard

- More than 30 RSS and Atom feeds, from The Hacker News and BleepingComputer to CISA, the NCSC, Cloudflare Radar and the AWS, Azure and Google Cloud status pages, gathered into headlines, advisories, critical CVEs, blogs and outages.
- Each item becomes a GitHub issue, and the dashboard and a morning and afternoon RSS rundown are built from them. It's quite noisy, but well liked, with more than 70 stars on GitHub.
- Get the rundown in Slack, Microsoft Teams or a feed reader.
- [Visit the dashboard](https://secops.thechels.uk) &rarr; or [view the repo](https://github.com/SecOpsNews/news) &rarr;

## All feeds as OPML

- Every source on the dashboard, grouped by category, to import into a feed reader. It's rebuilt automatically whenever a feed is added.
- [Download the OPML](https://secops.thechels.uk/feeds.opml) &rarr;

## Feed to issues template

- A GitHub template repo for watching your own choice of feeds, such as vendor advisories and status pages, and getting each new item as a GitHub issue. Edit one list of feeds, and old items close themselves.
- [View the template](https://github.com/SecOpsNews/template-feed-to-issues) &rarr;

## SBOM script

- A Python script that scans a folder and writes a software bill of materials, `sbom.json`, in CycloneDX 1.6 format. It reads Python, npm, Ruby, Go, Rust, PHP, Swift and CocoaPods manifests and lock files, using the Python standard library only.
- [View the script](https://github.com/SecOpsNews/script_sbom.py) &rarr;

All are open source, under an MIT licence.
