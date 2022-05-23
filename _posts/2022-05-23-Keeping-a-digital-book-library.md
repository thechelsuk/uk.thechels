---
title: Keeping a digital book library
layout: post
date: 2022-05-23

---
I wanted to keep a digital library of all the books I own, some physical, some digital (mostly on my Kindle). Thanks to [Katy Decorah](https://katydecorah.com/code/read/) much of the work had been done for me. Including a Shortcut for my phone. I embellished Katy's version with a `scan QR Barcode` action. So I can easily scan the ISBN of any book, append a timestamp `ISO` format of course. and then trigger an issue to be raised on GitHub using their API and a Token.

The issue has a label, and this triggers and Action which includes commiting the change to my repo without me needing to do anything else

![Screenshot 2022-05-23 at 21 19 27](https://user-images.githubusercontent.com/1188107/169899627-593c8354-5517-4bc5-a3f4-13e48e4a7120.png)

All the data is in in YML so can be exported or used as needed.

