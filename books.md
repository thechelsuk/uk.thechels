---
layout: default
title: BookShelf

---

{% assign sorted = site.data.read | sort: 'dateFinished' %}

<div class="books">
  {% for book in sorted %}
    <a href="{{book.canonicalVolumeLink}}" class="book"><img src="{{book.imageLinks.thumbnail}}" alt="{{book.title}}"></a>
  {% endfor %}
</div>
