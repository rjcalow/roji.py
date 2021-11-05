## Roji.py

My hobbyist attempt at a static digital garden generator for my notes.

It *aims* to be small and simple.

It has [[wiki style links]], backlinks and a tag system for hyperlinking. 

## Why?

Most static site generators concentrate on the blog format. Frustrated, I made my own, inspired by this [article](https://medium.com/swlh/a-static-site-generator-in-python-part-2-d7071da25904), so that I could transform academic and personal notes into a simple website. 


## Update

Engine-wise, this is probably my final update for a while at least. I have rewritten this engine/generator so many times. In the process, I have learnt a lot. But I would preferably use it for my notes as is, rather than keep tinkering with it. I have given it a module-component design to allow for future edits. The image processor and markdown to HTML components can be swapped out and replaced. 

The folder design is embedded and not for everyone. I adopted it as an organizational feature. Digital gardens should not be so structured. It would be neat in the future to rewrite the wikilink engine into an automated connection generator and have all the notes at the root level. Currently, for dynamic connections, there is a search page using lunr.js. Following minimalist/low resource design, I did not want to rely on javascript, but it works well.  
