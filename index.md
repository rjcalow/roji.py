---
title: "roji.py"
date: 13/9/2020
---

## Roji.py

My hobbyist attempt at a static digital garden generator for my notes.

It *aims* to be small and simple.

A folder of markdown files are processed into pages and topics.

Pages are linked through wikilink style &#91;&#91;brackets &#93;&#93;.

Topics are listed with the YAML of the markdown files, each topic has its own page, and can be linked to with &#123;topic&#125;.


## Why?

Most static site generators concentrate on the blog format. Frustrated, I made my own, inspired by this [article](https://medium.com/swlh/a-static-site-generator-in-python-part-2-d7071da25904), so that I could transform academic and personal notes into a simple website. 

## some example pages

- [[a page]] - internal links are made by brackets
- [[gardens]]
- [[image example]]



## Change log
### 11/11/2020

Improved layouts to match tufte.css better.

#### Changes

- Article tag now embeded in pages.
- Footer class now also used.


### 30/9/2020

I dropped sakura.css for [tufte-css](https://github.com/edwardtufte/tufte-css). Reason, purely simple: I like it for my personal website. In the future it would be neat to select, or make it easier to choose, a classless css. 

Paths/Addresses are all in lower now to avoid problems on my host. 

Topics can be linked with brackets &#123;  &#125;

I could do with a function to deal with different date types. At the moment the script needs d/m/yyyy. 


### 23/9/2020

Constantly playing with ideas, toying with code, the project got a little out of hand. I stumbled on this amazing clean code and became inspired.

- https://blog.thea.codes/a-small-static-site-generator/
- https://github.com/theacodes/blog.thea.codes/

#### Changes:

- Using the fast cmarkgfm package for markdown.
- Rewrote everything.
- Started using pathlib like I should have done in the first place.
- Added a tag system in the form of topics. This still needs to be streamlinned. 
- Neatened the Jinja2 rendering.
- Decided against a directory. It didn't fit the digital garden ethos. 

#### Thinking about:

- I have spent too much time on this, but have learnt a lot.
- Drop in classless css framworks ( https://github.com/dohliam/dropin-minimal-css ) are great.
- I need to build my notes up rather than constantly playing with this.

### 13/9/2020

Changed backend from YAML and pystache to frontend and jinja2 modules. This made processing faster and gives better options. There is now a index and page template, and I'm trying to build a simple menu or categories but I'm stumped on how to organize the posts data by a topic adopted from yaml.

There are also changes to layout/template, keeping it even more simple by removing extra css and using pure html tables for header.

#### Some influences:

* [Making a Static Site Generator with Python ](https://dev.to/nqcm/making-a-static-site-generator-with-python-part-2-4al)

* [Building a Simple Static Site Generator in Python](https://youtu.be/Ph7oJDR71Jc)
