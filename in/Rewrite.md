---
title: "Rewrite"
date: 1/1/2021
topic: changes

---

I have completely rewritten my tiny digital garden generator. 

Rather than LOTS of functions, it now uses objects, adopts the frontmatter page object more, and uses YAML settings to inject information. 

Settings are loaded into the main object with:

    with open("config.yml", "r", encoding='utf-8') as f:
        config = yaml.load(f, Loader=yaml.SafeLoader)

    for key in config: setattr(self, key, config[key])


Additionally, I have stuck to using the Python-Markdown package, and have moved some functions to extensions. Third-party extensions include the FigureCaption extension and UrlizeExtension. The goal is to include enough features to allow for the conversion of markdown notes without worry.

Features I need now:

* renable rss feed generation
* a image processor to scrub metadata and resize/compress