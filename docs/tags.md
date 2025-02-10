---
layout: default
title: "Tags"
permalink: /tags/
---

# Tags

<div class="tag-cloud">
{% assign tags = site.tags | sort %}
{% for tag in tags %}
  {% assign tag_name = tag | first %}
  {% assign posts = tag | last %}
  <a href="{{ site.baseurl }}/tag/{{ tag_name | slugify }}" class="tag-item">
    <span class="tag-name">{{ tag_name }}</span>
    <span class="tag-count">{{ posts.size }}</span>
  </a>
{% endfor %}
</div>

<style>
.tag-cloud {
  display: flex;
  flex-wrap: wrap;
  gap: 10px;
  margin: 2em 0;
}

.tag-item {
  background: var(--bg-secondary);
  padding: 8px 15px;
  border-radius: 20px;
  text-decoration: none;
  display: inline-flex;
  align-items: center;
  transition: transform 0.2s ease, background-color 0.2s ease;
}

.tag-item:hover {
  background: var(--bg-tertiary);
  transform: translateY(-2px);
}

.tag-name {
  color: var(--text-main);
}

.tag-count {
  background: var(--bg-tertiary);
  color: var(--text-secondary);
  padding: 2px 8px;
  border-radius: 12px;
  font-size: 0.8em;
  margin-left: 8px;
}
</style>

## Posts by Tag

{% for tag in tags %}
### {{ tag[0] }}
{% for post in tag[1] %}
- [{{ post.title }}]({{ site.baseurl }}{{ post.url }}) <small class="post-date">{{ post.date | date: "%B %d, %Y" }}</small>
{% endfor %}
{% endfor %}
