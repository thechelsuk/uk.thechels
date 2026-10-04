---
layout: post
date: 2022-05-02
link: https://blog.ploeh.dk/2021/12/27/label-persistent-test-data-with-deletion-dates/
title: Label persistent test data with deletion dates
seo_title: "Label Persistent Test Data With Deletion Dates"
seo_description: "Linking Mark Seemann's tip for shared staging environments: label the test data your tests leave behind with a deletion date so it can be cleaned up."
type: linked
cited: Ploeh.dk
---

> I run my tests against a staging environment. The entire purpose of the library is to create resources, so all successful tests leave behind new 'things' in that staging environment.
> I'm not the only person who's testing against that environment, so all sorts of test entries accumulate.
