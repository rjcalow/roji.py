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
- N̶e̶s̶t̶ ̶s̶e̶c̶t̶i̶o̶n̶ ̶t̶a̶g̶s̶ ̶u̶n̶d̶e̶r̶ ̶h̶e̶a̶d̶i̶n̶g̶s̶ ̶f̶o̶r̶ ̶t̶u̶f̶t̶e̶.̶c̶s̶s̶  - Changed turfte css varient to [https://github.com/darshandsoni/asciidoctor-skins/blob/71ce8dcd401600985dcce7b78d5b5d8b20a0a52d/css/tufte.css](ascii doctor). It's now much cleaner.

Long term
- Streamline topics
- Add a better system for dates
- Image resizer

## Credits
- [https://github.com/theacodes/blog.thea.codes/](https://github.com/theacodes/blog.thea.codes/) - static site tutorial and much better code than mine.
- [https://github.com/edwardtufte/tufte-css](https://github.com/edwardtufte/tufte-css) - drop-in css
