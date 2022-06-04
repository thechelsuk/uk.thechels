---
title: Using a label to trigger automation with GitHub Actions
layout: post
date: 2022-06-04

---
I have been evolving my website over the last few weeks - football season is over - and I am using GitHub Actions to automate my processes and essentially use GitHub's Issues as a content management system (CMS).

CMSs typically have a database backend see WordPress and MySql, there are headless CMSs like Strapi that offer up an API from datasources, but being a cheapskate and hosting my website on GitHub pages I don't have the option of a database. So using the tools at hand I am able to create an issue in GitHub using issue templates (these help structure the content and automatically applies labels).

From these I can then trigger an action that either converts an issue to a markdown file as a post or by adding some data to a yaml file - Jekyll my static site generator uses yaml files (along with CSV and JSON) as data sources.

the below action shows a check against the `labelname` to make sure the right action runs by passing the variable into another action called `runner`. 

Data in yaml files can be looped over at build time to create tables, lists. Using the liquid templating language one can sort and group data too. Such that i now record podcasts, books, websites, films, football teams and a to do list all in yaml files ans all managed by GitHub's issues.  

<script src="https://gist.github.com/MatBenfield/e6d5982d24d35530bebfef157d76aff1.js"></script>
