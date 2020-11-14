## Roji.py

My hobbyist attempt at a static digital garden generator for my notes.

It *aims* to be small and simple.

It has [[wiki style links]], backlinks and a tag system for hyperlinking. 

## Why?

Most static site generators concentrate on the blog format. Frustrated, I made my own, inspired by this [article](https://medium.com/swlh/a-static-site-generator-in-python-part-2-d7071da25904), so that I could transform academic and personal notes into a simple website. 

## Usage
Clone the repo and install requirements 
```
pip install -r requirements.txt 
```
Add markdown files to the *in* folder and any images into *imgs*, and then run...

```
python3 roji.py
```

This will create a html site in */docs*. Changes can be made in the template.html and roji.py itself. 

## Things to do 🍃
Short term
- Nest section tags under headings for tufte.css

Long term
- Streamline topics
- Add a better system for dates
- Image resizer

## Credits
- [https://github.com/theacodes/blog.thea.codes/](https://github.com/theacodes/blog.thea.codes/) - static site tutorial and much better code than mine.
- [https://github.com/edwardtufte/tufte-css](https://github.com/edwardtufte/tufte-css) - drop-in css
