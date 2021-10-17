import frontmatter
from datetime import datetime
import urllib
import re 
from md_to_html import mdtohtml

class Note:
    def __init__(self, path, folder):
        #parse
        self.fmatter = frontmatter.load(str(path), encoding='utf-8')
        self.date = datetime.strptime(self.fmatter['date'], "%d/%m/%Y")
        self.title = self.fmatter['title']
        self.month = self.date.month
        self.filename = path.name
        self.folder = folder
        self.folderurl = folder.fullurl
        self.url = urllib.parse.quote_plus(str(path.stem))
        self.fullurl = str(self.folderurl) + "#" +self.url
        self.absoluteurl = ""
        self.HTML = mdtohtml(self.fmatter.content)
        self.text = re.sub('<[^<]+?>', '',self.HTML) 
        
        #imgs
        self.imgs = []
        for i in re.findall(r'src="(.*?)"', self.HTML ):
            ext =(".jpg", ".jpeg", ".png",".gif")
            if i.endswith(ext) == True:
                self.imgs.append(self.Img(i))
        
        self.wikilinks = []
        

    class Img:
        def __init__(self, src):
            self.src = src
            if "/" in src:
                self.filename = src.split("/")[-1] 
            else:
                self.filename = src