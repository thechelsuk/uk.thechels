---

layout: post
date: 2023-04-07
link: https://github.blog/2022-09-19-5-tips-for-prioritizing-dependabot-alerts/
title: 5 tips for prioritizing Dependabot alerts
cited: GitHub

---

> By default, Dependabot alerts are sorted with a “Most Important” sort, which not only takes into consideration the potential risk to your project, but also considers factors to infer how relevant the vulnerability may be to your project. For example, this sort calculation takes into consideration whether you’re calling a vulnerable function, as well as dependency scope (like if an alert is a devDependency).

> This calculation also takes into account the actionability of the alert; for example, alerts with available patches (like a version with a fix) are featured higher than alerts without a patch.