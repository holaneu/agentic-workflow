---
layout: default
title: "Tags"
permalink: /tags/
---

# Tags

{% for tag in site.tags %}
- [{{ tag[0] }}](/tag/{{ tag[0] }}/) ({{ tag[1].size }})
{% endfor %}
