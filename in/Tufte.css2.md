---
title: "Tufte.css 2"
date: 14/11/2020
topic: changes

---

I have been looking at parsers with plugins and options for blocks to use tufte.css section tag. My markdown files do not have inbuilt tags and nor do I want to go through each one adding tags. So I need a python solution to add section tags under headings and close at the next heading.  This is probably a different project altogether as it's about tufte.css than the digital garden.

I have already wrote some basic code to move alt text to the margins

~~~
    count = 1
    imgs = re.findall(r'<img(.*?)>' ,content)

    for img in imgs:
        img = str(img)
        
        try:
            alt = re.search(r'alt=".(.*?)"', img).group(0)
            alt_text = re.search(r'".(.*?)"', alt).group(0)
            alt_text = alt_text.replace('"', "")
            if alt_text != None:
                # the following is messy BUT readable
                newline = '<figure>'
                newline += ' '
                newline += "\n <img" + str(img) + '>'
                newline += '<label for="' + alt_text.replace(" ", "-")[0:4] + str(count) + '" class="margin-toggle">' + str(count)+'</label><input type="checkbox" id="' + alt_text.replace(" ", "-")[0:4] + str(count) + '" class="margin-toggle">'
                newline += '\n<span class="marginnote">' + str(alt_text) + '</span>'
                newline += "</figure>"
                content = content.replace("<img" + str(img)+">", newline)
                count += 1
        except:
            pass
~~~