import yaml
import pathlib
import frontmatter
from markdown import markdown
from mdx_extensions.mdx_ext import findTopics
from mdx_extensions.mdx_ext import WikiBrackets
from mdx_extensions.mdx_urlize import UrlizeExtension
from mdx_extensions.figureAltCaption import FigureCaptionExtension
from mdx_extensions.mdx_truly_sane_lists import TrulySaneListExtension
from markdown.extensions.toc import TocExtension

import jinja2
from datetime import datetime
import shutil

class Garden:
    
    def __init__(self):
        self.gen_date = datetime.today().strftime('%d/%m/%Y')
        #open w/ utf8 so emojis can be stored in yaml tags
        with open("config.yml", "r", encoding='utf-8') as f:
            config = yaml.load(f, Loader=yaml.SafeLoader)

        for key in config: setattr(self, key, config[key])

        self.topicsList = [] #used for unique tags
        self.md_files = pathlib.Path(self.markdown_folder) #markdown files

    def parse(self):
        self.pages = [] #stores page objects
        for m in self.md_files.glob('*.md'):              
            page = frontmatter.load(str(m), encoding='utf-8')
            page.readablename = m.stem.replace("-", " ")
            page.name = page.readablename.replace(" ", "_").replace("-", "_").lower()
            page.template = self.template_page
            page.RAW = page.content #unconverted markdown
            page.content =  markdown(page.content,extensions=[FigureCaptionExtension(), WikiBrackets(), UrlizeExtension(),TocExtension(),TrulySaneListExtension()])
            page.topics = self.topic_helper(page['topic'])
            page.HTML_topics = []
            for t in page.topics:
                if t not in self.topicsList: self.topicsList.append (t) #on the fly tag finding
                page.HTML_topics.append('<a href="{path}">{name}</a>'.format(path="../topics/"+t.replace(" ","_")+"/", name=t.title())) 
            
            page.path = pathlib.Path(self.out_folder) / page.name
            if "http" in self.css: page.css = self.css
            else: page.css = ".." + self.css
            self.pages.append(page)

        for p in self.pages: p.backlinks = self.find_refences(p.readablename)

        self.pages_by_date = sorted(self.pages,key=lambda page: datetime.strptime(page['date'], "%d/%m/%Y"), reverse=True)

    def find_refences(self, name):
        found = []
        find = "[[" + name.lower() + "]]"
        for p in self.pages:
            if find in p.RAW.lower():
                lines = str(p.RAW).splitlines()
                for line in lines: 
                    if find in line.lower():
                        found.append('<a href="{path}">{name}</a> <i>{l}</i>'.format(path="../"+p.name + "/", name=p.readablename, l=markdown(line)))
        if len(found) >= 1: return found
        else: return None


    def build_Topicpages(self):
        for t in self.topicsList:
            topicpage = self.Topicpage(t, self)
            self.writePage(topicpage)


    def topic_helper(self, topics):
        #cleans up lazy yaml writing with "," instead of lists
        cleanTopics=[]
        if isinstance(topics, str) == True:
            lst = topics.split(",")
            for l in lst:
                l = "".join(l.lstrip().rstrip())
                if l != "": cleanTopics.append(l)
            return cleanTopics
        else: return topics

    def build(self):
        #render tag/topic pages
        self.build_Topicpages()

        #render pages
        for p in self.pages:
            self.writePage(p)
        
        #render homepage
        homepage = self.Homepage(self)
        self.writePage(homepage)

        #copy assets to www dir
        for f in self.folders_to_copy: self.copy_assets(f)
        self.copy_assets(self.img_folder)



    def copy_assets(self, folder):
        path_in = pathlib.Path(folder)
        path_out = pathlib.Path(self.out_folder) / path_in.name
        #print (path_in.parent.name)

        if path_out.exists() == False:
            path_out.mkdir(parents=False, exist_ok=True)

        files = path_in.glob('*')

        for f in files:
            path = path_out.joinpath(f.name)
            shutil.copy(str(f), str(path))

    def writePage(self, page):
        if page.path.exists() == False: page.path.mkdir(parents=True, exist_ok=True)
        page.path = page.path / "index.html"
        jinja_env = jinja2.Environment(loader=jinja2.FileSystemLoader(self.templates))
        template = jinja_env.get_template(page.template)
        rendered = template.render(page=page, garden=self)
        page.path.write_text(rendered, encoding='utf8')
    

    class Homepage:
        def __init__(self, Garden):
            self.title = Garden.site_name
            self.template = Garden.template_homepage
            self.path = pathlib.Path(Garden.out_folder)
            if "http" in Garden.css: self.css = Garden.css
            else: self.css = "." + Garden.css
            
            if Garden.displayIndexmd == True:
                with open("index.md", "r", encoding='utf-8') as f:
                    self.content = markdown(f.read(),extensions=[FigureCaptionExtension(), WikiBrackets(), UrlizeExtension()])
                    #messy hack to make extension produced links work on homepage
                    self.content = self.content.replace('<a href="../', '<a href="./')
            
            self.TopicSection = []
            Garden.topicsList.sort(reverse=False)
            for t in Garden.topicsList:
                self.TopicSection.append('<a href="{path}">{name}</a>'.format(path="./topics/"+t.replace(" ","_")+"/", name=t))
            
            self.new = []
            for p in Garden.pages_by_date[0:5]:
                self.new.append('<p><a href="{path}">{name}</a> <i>{date}</i></p>'.format(path="./"+p.name, name=p['title'], date=p['date']))
            

    class Topicpage:
        def __init__(self, name, Garden):
            self.name = name    
            self.title = name.title()   
            self.template = Garden.template_topic                  
            self.path = pathlib.Path(Garden.out_folder) / "topics" / str(self.name).replace(" ", "_") 
            
            if "http" in Garden.css: self.css = Garden.css
            else: self.css = "../.." + Garden.css
            self.content = []
            for p in Garden.pages_by_date :
                if name in p.topics:
                    self.content.append('<p><a href="{path}">{name}</a> <i>{date}</i></p>'.format(path="../../"+p.name, name=p['title'], date=p['date']))
            
            
if __name__ == "__main__":
    g = Garden()
    g.parse()
    g.build()

