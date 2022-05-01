---

layout: post
date: 2022-05-01
link: https://technology.blog.gov.uk/2021/10/08/a-new-standard-of-testing-for-gov-uk/
title: A new standard of testing for Technology in government
cited: Gov.uk

---

> What’s in a test? GOV.UK is an ecosystem of 70 applications and components, which are mostly written in Ruby on Rails. For each app, we have tests to make sure it works in isolation: unit, integration and UI tests - these test the behaviour of the app and rely on simulated communication with other apps and services visual regression tests - these run against rendered HTML to verify it appears as expected (most of our apps use components instead of raw HTML) runtime health checks - many of our apps have a way to give a live report of their internal status, such as connectivity to a database