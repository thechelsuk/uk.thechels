---

layout: post
title: Saving json file using GiHhub actions and curl
date: 2020-11-12
tag:
 - dev

---

Previously I had been using a python script and import the requests package to access a public json file and saving it to my repo, however there is a simpler way using curl built right in to the github action.

I have found this to be more reliable overall - the previous method would some times leave malformed json and break future activities.

As you can see below, this can be triggered manually in the actions tab on github `workflow_dispatch` does that, plus also its scheduled as a cron task every 15 minutes.

The job runs on ubuntu, uses curl and saves it out to the output_file.json

``` yaml
name: Scheduled Build
on:
  workflow_dispatch:
  schedule:
    - cron:  '*/15 * * * *'

jobs:
  build:
    runs-on: ubuntu-latest
    steps:
    - name: Check out repo
      uses: actions/checkout@v2
      with:
        fetch-depth: 0
    - name: Download Feed
      run: |-
        curl "[url]" | jq . > output_file.json
    - name: Commit and push changes
      run: |-
        git diff
        git config user.name "Automated"
        git config user.email "actions [at] users.noreply [dot] github.com"
        git diff --quiet || (git add -A && git commit -m "Updated with latest")
        git push
```

At the moment, on public repos, there appears to be no cost involved in doing this, but do be mindful of GitHub's costs and respect the source's API restrictions - for example the environment agency's open beta API suggests requests at every 15 minutes would suffice as that is how frequent the underlying data is update, running this every  minute would just be wasteful and offer little value.

The last part of the yaml file does a git diff and sets some user config (this basically can be anything) and then does a commit.

This is ideal for those that want to do some git-scraping and monitor and track public APIs for changes.
