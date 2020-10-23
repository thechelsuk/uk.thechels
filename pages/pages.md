---
layout : default
title : Menu
---

<h4>Pages</h4>
<ul>
  {% for page in site.pages %}
    {% if page.layout == 'default' %}
      {% if page.category == 'pages' %}
          <li><a href="{{ page.url }}">{{ page.title }}</a></li>
      {% endif %}
    {% endif %}
  {% endfor %}
</ul>
