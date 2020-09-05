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

<h4>Data</h4>
<ul>
  {% for page in site.pages %}
    {% if page.layout == 'data' %}
      <li><a href="{{ page.url }}">{{ page.title }}</a></li>
    {% endif %}
  {% endfor %}
</ul>
