---
title: Offers page

---

### Offers
Selection of offers and referrals mostly offering free money
      
      {% for item in site.data.offers %}
        - {{item.title}}  &rarr; [{{item.link}}]({{item.link}})
      {% endfor %}
