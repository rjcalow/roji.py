import yaml
from datetime import datetime
import urllib
import frontmatter
import pathlib
import markdown 
import re 
import jinja2

from img_process import *
from mdx_extensions.figureAltCaption import FigureCaptionExtension
from mdx_extensions.mdx_urlize import UrlizeExtension

class DigitalGarden:
    def __init__(self, configfile):
        self.gen_date = datetime.today().strftime('%d/%m/%Y')
        
        # open w/ utf8 so emojis can be stored in yaml tags
        with open(configfile, "r", encoding='utf-8') as f:
            config = yaml.load(f, Loader=yaml.SafeLoader)

        for key in config:
            setattr(self, key, config[key])
        
        self.md_files = pathlib.Path(self.markdown_folder)  # markdown files
        self.img_folder = pathlib.Path(self.img_folder)
        self.out_folder = pathlib.Path(self.out_folder)
        self.homepage_md = pathlib.Path(self.homepage_md)
        self.jinja = jinja2.Environment(loader=jinja2.FileSystemLoader(self.templates))
        self.template_page = self.jinja.get_template(self.template_page)
        self.template_home = self.jinja.get_template(self.template_homepage)
        self.assets = pathlib.Path(self.template_assets)

        self.folders = []
        for f in self.md_files.glob('*'):
            if f.is_dir and self.img_folder != f:
                self.folders.append(self.Folder(f))

    def cultivate(self):
        ''' 
        #################
         markdown > HTML
        #################
        '''
        for f in self.folders:
            render = self.template_page.render(folder=f, folders=self.folders, garden=self)
            
            dir = self.out_folder / f.url  
            

            if dir.exists() == False:
                dir.mkdir(parents=True, exist_ok=True)
            
            fullpath = dir / "index.html"
            
            fullpath.write_text(render, encoding='utf8')

        ''' 
        ##########
         homepage
        ##########
        '''
        homepage = frontmatter.load(str(self.homepage_md), encoding='utf-8')
        homepageHTML= markdown.markdown(homepage.content, extensions=[
                    'tables', 'fenced_code', UrlizeExtension()])
        render = self.template_home.render(homepage=homepageHTML, garden=self)
        fullpath = self.out_folder / "index.html"
        fullpath.write_text(render, encoding='utf8')

        ''' 
        ########
         images
        ########
        '''
        img_out_folder = self.out_folder / "imgs"
        if img_out_folder.exists() == False:
            img_out_folder.mkdir(parents=False, exist_ok=True)

        for img in self.img_folder.glob('*'):
            #print(img_out_folder / img.name)
            # loop to check if file used in md files
            # not great but my note image folder is a mess
            for f in self.folders:
                for n in f.notes:
                    for i in n.imgs:
                        if img.name == i.filename:             
                            IMG_process(1000, img, img_out_folder / img.name )
                            break
        ''' 
        #################
         template assets
        #################
        '''
        asset_out_folder = self.out_folder / "assets"
        if asset_out_folder.exists() == False:
            asset_out_folder.mkdir(parents=False, exist_ok=True)
        
        for f in self.assets.glob('*'):
            outpath = asset_out_folder / f.name
            shutil.copy(str(f), str(outpath))


    def notes_by_date(self):
        ''' called by jinja2 for a list of ALL notes by date for index'''
        notes_ = []
        for f in self.folders:
            for n in f.notes:
                notes_.append(n)
        
        notesbydate = sorted(notes_, key=lambda note: datetime.strptime(
            note.fmatter['date'], "%d/%m/%Y"), reverse=True)
        return notesbydate

    def search_notes(self, term, source):
        #print (term)
        results = []
        term = term.lower()
        for n in self.notes_by_date():
            if n.fmatter['title'] != source.fmatter['title']:
                r = re.findall(term.lower(), n.fmatter.content.lower() + " " + n.fmatter['title'].lower())
                
                if r and n not in results:
                    results.append(n)


        return results
    


    class Folder:
            def __init__(self, path):
                self.path = path
                self.name = str(path.stem)
                self.title = self.name.title()
                self.url = urllib.parse.quote_plus(str(path.stem))
                self.writepath = self.name 
                self.notes = []

                for f in self.path.glob("*.md"):
                    self.notes.append(self.Note(f, self.url))
                
                self.notesbydate = []
                self.notesbydate = sorted(self.notes, key=lambda note: datetime.strptime(
                    note.fmatter['date'], "%d/%m/%Y"), reverse=True)

    
            class Note:
                def __init__(self, path, folderrul):
                    #parse
                    self.fmatter = frontmatter.load(str(path), encoding='utf-8')
                    self.date = datetime.strptime(self.fmatter['date'], "%d/%m/%Y")
                    self.filename = path.name
                    self.folderurl = folderrul
                    self.url = urllib.parse.quote_plus(str(path.stem))
                    self.HTML = markdown.markdown(self.fmatter.content, extensions=[
                    'tables', 'fenced_code',  FigureCaptionExtension(), UrlizeExtension()])
                    
                    
                    #imgs
                    self.imgs = []
                    for i in re.findall(r'src="(.*?)"', self.HTML ):
                        ext =(".jpg", ".jpeg", ".png",".gif")
                        if i.endswith(ext) == True:
                            self.imgs.append(self.Img(i))
                    
                    #wiki links
                    self.wikilinks = []
                    reg = re.compile(r'\[\[(.*?)\]\]')
                    links = reg.findall(self.HTML)
                    if links:
                        for l in links:
                            t = f'<a href="#{self.url}Notes">{l}</a>'
                            self.HTML = self.HTML.replace(f"[[{l}]]", t)
                            #print(l)
                            
                            if l.lower() not in self.wikilinks: 
                                self.wikilinks.append(l.lower())
                                

                    else:
                        self.wikilinks = None


                class Img:
                    def __init__(self, src):
                        self.src = src
                        if "/" in src:
                            self.filename = src.split("/")[-1] 
                        else:
                            self.filename = src

                    

                       

g = DigitalGarden('config.yml')
g.cultivate()