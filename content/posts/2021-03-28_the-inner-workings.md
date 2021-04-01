---
title: "The Inner Workings"
date: 2021-03-28T21:00:00+01:00
location: "France"
---

If creating your own personal page has been on your mind for a while, I hope this blog post inspires you to go through with it. This is not intented to be a manual, but an overview of my own process.

As I've [previously mentioned](/posts/hello-world/), it is important to define some guidelines of what we want to archieve (even if later on we need to change them). As such, this webpage is intended to be lightweight and fast. Therefore, I will try to just include just the necessary resources. I will not follow this religiously like some people that won't even include images.

Since the main focus is to share some textual information with you, the website is structured in a way that makes it easy to read. First, the text is centered in middle of the screen. Secondly, the line length follows the [studies on the optimal line length](https://www.humanfactors.com/newsletters/optimal_line_length.asp), meaning they are not too long nor too short.

<!-- ## Domain

The domain name [mmagalha.es](https://mmagalha.es) might have you wondering if I am from Spain. Although I do have spanish ancestry, I am from Portugal. The domain name is the result of the merge between the first letter of my first name (Miguel) and my last name (Magalhães). It just happened that the spanish top-level domain (TLD) fitted my last name like a glove. 

My initial idea was to grab the [magalha.es](https://magalha.es) domain, but it was already owned my *"distant brazilian cousin"* with the same last name as me. Unfortunately, he was not interested in selling it. -->

## Site Generator

There are several static [site generators](https://jamstack.org/generators/) available. The two main criteria I used to choose between them were (1) it had to be popular and well established, measured by GitHub stars, and (2) it could not be JavaScript based. After checking that it provided all the desired functionalities, [Hugo](https://gohugo.io/) ended up being the chosen one. Another viable alternative would be [Jekyll](https://jekyllrb.com/).

As a side note, Víctor (from [Evolutio](https://evolutio.pt/)) and I developed a basic proof-of-concept [static site generator](https://github.com/djangocon/2020.djangocon.eu/blob/master/djangocon_2020/site/templatetags/markdown_extras.py) in Django for the official website of [DjangoCon Europe 2020](https://2020.djangocon.eu/) & [2021](https://2021.djangocon.eu/). However, this was done just for demonstratation & educational purposes. It is somewhat limited, but you need to take into account that it has less than 50 lines of code.

## Design & Structure

The design & structure of this page are made simple on purpose. Since I am not a designer, I needed some inspiration and for that I've got some ideas others: [Tom MacWright](https://macwright.com/), [Andrew Healey](https://healeycodes.com/) and [Tyler Kimothy](https://tyler.kim/).

## Privacy

This blog does not include cookies and will not sell your personal data. In terms of analytics, [counter.dev](https://counter.dev/) is used since it is free, open source, and privacy friendly.