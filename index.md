---
layout: default
title: Home
---

## The Principle of Scannability

Good web design allows users to scan a page quickly to find what they're looking for. Long blocks of text can be intimidating. Marginalia, or sidenotes, help break up the text and provide quick summaries for the reader.
{% include sidenote.html text="Scannability & Sidenotes" %}

This system works by using a Jekyll include. The include tag inserts a small piece of HTML into the final page. Our CSS then sees this new HTML element and uses a Grid layout to position it in the left-hand column, next to the paragraph it's associated with.
{% include sidenote.html text="Jekyll, CSS Grid, Layout" %}

On mobile devices, a two-column layout doesn't work well. Our CSS includes a special rule called a media query. If the screen is too narrow, it automatically switches to a single-column layout and styles the sidenote as a simple, indented quote above the paragraph.
{% include sidenote.html text="Responsive & Mobile" %}

## Book Notes

Here you can find summaries and notes on various books.
{% include sidenote.html text="Reading List" %}

<ul>
  <li><a href="books/lieberman_2013/lieberman.html">Lieberman, D. E. (2013). *The story of the human body: Evolution, health, and disease.* Pantheon Books.</a></li>
</ul>
