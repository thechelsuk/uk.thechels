---

layout: post
date: 2022-07-24
link: https://circleci.com/blog/trunk-vs-feature-based-dev/
title: Trunk-based vs. feature-based development
cited: CircleCI

---

> A developer can directly push changes to the main branch, but if a coding activity requires more extensive time — perhaps a few days — they can check out a branch from main, move the changes into it, then merge it back in when development is complete.
 
> Fellow developers must then perform a code review based on company guidelines before merging the checked-out branch with the main branch. The crucial thing about checked-out branches is that they are short-lived, spanning two to three days at most.

> In a trunk-based workflow, the main branch should always be production-ready. Faulty code can break the entire build and result in a complicated development history. That means that teams should thoroughly test each code change before pushing them to the main branch. Short development cycles and automated testing enable teams to identify defects and recover from failed builds quickly, reducing the risk.