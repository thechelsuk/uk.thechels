---

layout: post
syndicate: false
date: 2026-06-12 21:25
title: NPM no longer has auto-run scripts
link: https://www.theregister.com/devops/2026/06/10/github-pulls-pin-on-npms-auto-run-scripts/5253453
cited: The Register
type: linked

---

Sensible

> GitHub will change npm's defaults so the install command no longer runs scripts automatically, disabling a feature commonly exploited by malicious packages such as the notorious Shai-Hulud worm.
> 
> Maintainer Leo Balter said "Install-time lifecycle scripts are the single largest code-execution surface in the npm ecosystem. Every npm install runs scripts from every transitive dependency, so a single compromised package anywhere in your tree can execute arbitrary code on a developer machine or CI (continuous integration) runner."