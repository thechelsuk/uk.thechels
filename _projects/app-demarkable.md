---
layout: projects
title: Demarkable - DMARC and SMTP-TLS Viewer for MacOS
permalink: /projects/demarkable
class: applications
seo: "Demarkable MacOS App - A viewer of DMARC and SMTP-TLS Reports"
i_name: Purchase on Gumroad
i_url: "https://thechelsuk.gumroad.com/l/dmarc"
i_image: "/images/apps/demarkable-banner.png"
i_icon: "/images/apps/demarcable-icon.png"
summary: "Drop in a DMARC or SMTP TLS report and get a clear, human-readable breakdown of what passed, what failed, and why."
type: mobile
---

Every domain sending email gets DMARC aggregate reports and SMTP TLS reports back from Google, Microsoft, Yahoo, and every other major mailbox provider — dense XML and JSON files nobody actually enjoys reading. Demarkable turns them into something you can actually understand at a glance.

Drag a report in any of xml, zipped, or gzipped files, it doesn't matter and Demarkable shows you exactly what happened: which servers sent mail as your domain, whether SPF and DKIM passed and aligned, and in plain English, why a message failed if it did. SMTP TLS reports: which connections were encrypted under MTA-STS or DANE, which failed, and what actually went wrong (expired certificate, no STARTTLS support, a broken policy all spelled out for you.

## Highlights

- Drag-and-drop (or ⌘O) import of DMARC aggregate reports and SMTP TLS reports
- Accepts `.xml`, `.json`, `.zip`, and `.gz` — auto-detects which report type it's looking at
- Per-source breakdown: sending IP, message volume, disposition, SPF/DKIM pass or fail
- Plain-English explanations for every failure — no more decoding raw result codes
- TLS report failure types explained: expired certs, missing STARTTLS, MTA-STS/DANE policy problems
- Local history of every report you've imported, with pass-rate at a glance — clear it anytime
- Native SwiftUI app built for the Mac — fast, no browser, no account, no subscription
