import yaml
from datetime import datetime
import pathlib
import jinja2
from img_process import IMG_process
from wikilinks import wikilinkGenerator
from folder import Folder
from md_to_html import mdtohtml
import shutil

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
        self.jinja = jinja2.Environment(
            loader=jinja2.FileSystemLoader(self.templates))
        self.template_page = self.jinja.get_template(self.template_page)
        self.assets = pathlib.Path(self.template_assets)

        print (self.out_folder.iterdir())
        for x in self.out_folder.iterdir():
            print(x)
        ''' 
        #################
         folders > notes
        #################
        '''
        self.folders = []
        for f in self.md_files.iterdir():

            #if f.is_dir: print(f)
            if f.is_dir:
                if str(self.img_folder) not in str(f):
                    folder = Folder(f, self.md_files, None)
                    self.folders.append(folder)

    def cultivate(self):
        ''' 
        #################
         get all folders
        #################
        '''
        self.allfolders = []
        self.allfolders += self.folders
        for f in self.folders:
            if f.allchildren() != None:
                self.allfolders += f.allchildren()

        ''' 
        #################
          gen wiki links
        #################
        '''
        wikilinkGenerator(self.notes_by_date())

        ''' 
        #################
          write notes
        #################
        '''
        for f in self.allfolders:
            self.sow(f)

        ''' 
        ########
         images
        ########
        '''
        img_out_folder = self.out_folder / "imgs"
        if img_out_folder.exists() == False:
            img_out_folder.mkdir(parents=False, exist_ok=True)

        for f in self.allfolders:
            for n in f.notes:
                for i in n.imgs:
                    for img in self.img_folder.glob('*'):
                        if i.filename == img.name:
                            IMG_process(480, img, img_out_folder / img.name)
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

    def sow(self, f):
        ''' 
        #################
           write files
        #################
        '''
        render = self.template_page.render(
            folder=f, folders=self.folders, garden=self)

        dir = self.out_folder / f.writepath

        if dir.exists() == False:
            dir.mkdir(parents=True, exist_ok=True)

        fullpath = dir / "index.html"

        fullpath.write_text(render, encoding='utf8')

    def notes_by_date(self):
        ''' called by jinja2 for a list of ALL notes by date for log'''
        notes_ = []
        for f in self.allfolders:
            for n in f.notes:
                notes_.append(n)

        notesbydate = sorted(notes_, key=lambda note: datetime.strptime(
            note.fmatter['date'], "%d/%m/%Y"), reverse=True)
        return notesbydate

    def notes_by_month(self):
        '''
        generates a list of lists by month/year
        '''
        notes_ = self.notes_by_date()
        dates = []
        notesbymonth = []

        for n in notes_:
            month = []
            if str(n.date.month) + "/" + str(n.date.year) in dates:
                continue
            for n2 in notes_:
                if n.date.month == n2.date.month:
                    if n.date.year == n2.date.year:
                        month.append(n2)

            dates.append(str(n.date.month)+"/" + str(n.date.year))
            notesbymonth.append(month)

        return notesbymonth

    def size(self):
        ''' misc function for index page '''
        #return self.out_folder.stat().st_size
        
        return (sum(file.stat().st_size for file in self.out_folder.rglob('*')))

    def pages(self):
        '''
        builds meta pages, search and index ect.
        '''
        self.sow_page("search.html", self.out_folder / "search", None)

        self.sow_page("log.html", self.out_folder, None)

        f = open(self.homepage_md, 'r')
        homepage = mdtohtml(f.read())

        self.sow_page("index.html", self.out_folder, homepage)

    def sow_page(self, template, path, content):
        template = self.jinja.get_template(template)
        render = template.render(folders=self.folders,
                                 garden=self, content=content)

        if path.exists() == False:
            path.mkdir(parents=True, exist_ok=True)

        fullpath = path / "index.html"
        fullpath.write_text(render, encoding='utf8')
