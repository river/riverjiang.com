---
title: Blog
excerpt_separator: ""
---

<div class="posts">
  {% for post in site.posts %}
  <div class="post">
    <h1 class="post-title">
      <a href="{{ post.url | absolute_url }}">
        {{ post.title }}
      </a>
    </h1>

    <span class="post-date">{{ post.date | date_to_string }}</span>

    {{ post.content | strip_html | truncatewords: 50 }}
    <a href="{{ post.url | absolute_url }}">read more &rarr;</a>
  </div>
  {% endfor %}
</div>