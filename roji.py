import yaml
import re
import pathlib
import frontmatter
import jinja2
import urllib.parse
from datetime import datetime
import shutil
import markdown
from mdx_extensions.mdx_urlize import UrlizeExtension
from mdx_extensions.figureAltCaption import FigureCaptionExtension
from mdx_extensions.mdx_truly_sane_lists import TrulySaneListExtension
import PIL
from PIL import Image


class Garden:

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
        self.images = []  # images in docs
        self.docs = []  # global store of docs for homepage

    def parse(self, path):
        try:
            page = frontmatter.load(str(path), encoding='utf-8')
            page.filename = path.name
            page.name = path.stem
            page.url = urllib.parse.quote_plus(str(path.stem))
            page.RAW = page.content  # unconverted markdown
            page.content = markdown.markdown(page.content, extensions=[
                                             UrlizeExtension(), TrulySaneListExtension(), FigureCaptionExtension(), 'tables'])
            page.images = self.find_images(page.content)
            for i in page.images:
                self.images.append(i.split("/")[-1])
            page.title = str(page['title']).title()

            for html in self.html_changes:
                page.content = page.content.replace(
                    html['replace'], html['apply'])

            return page

        except Exception as e:
            print(e)

    def process_image_folder(self):
        images = self.img_folder.glob('*')

        imagefolder = self.out_folder / "imgs"

        if imagefolder.exists() == False:
            imagefolder.mkdir(parents=False, exist_ok=True)

        for f in images:
            process_path = imagefolder / f.name

            if process_path.exists == True:
                continue
            if f.name in self.images:  # and process_path.exists == False:
                # https://gist.github.com/tomvon/ae288482869b495201a0
                mywidth = 1000

                img = Image.open(f)
                if img.width > mywidth and f.suffix != ".gif":
                    wpercent = (mywidth/float(img.size[0]))
                    hsize = int((float(img.size[1])*float(wpercent)))
                    img = img.resize((mywidth, hsize), PIL.Image.ANTIALIAS)
                    img.save(str(process_path))
                else:
                    shutil.copy(str(f), str(process_path))

    def build(self):
        # parse folders
        self.folders = []

        #self.docs = []

        #folder loop
        for f in self.md_files.glob('*'):
            if f.is_dir and self.img_folder != f:
                F = self.Folder(f)  # folder class

                #folder file loop
                for doc in f.glob('*.md'):
                    p = self.parse(doc)
                    p.folder = str(f.name)
                    p.fullurl = self.siteurl + "/" + \
                        urllib.parse.quote_plus(
                            f.name) + "#" + urllib.parse.quote_plus(p.name)

                    F.docs.append(p)
                    self.docs.append(p)

                F.docs_by_date = sorted(F.docs, key=lambda doc: datetime.strptime(
                    doc['date'], "%d/%m/%Y"), reverse=True)
                F.path = self.out_folder / F.url
                F.template = self.template_page
                self.folders.append(F)

        #all docs for homepage
        self.docs = sorted(self.docs, key=lambda doc: datetime.strptime(
            doc['date'], "%d/%m/%Y"), reverse=True)

        # wiki links
        reg = re.compile(r'\[\[(.*?)\]\]')
        for d in self.docs:
            d.modals = []
            m = reg.findall(d.content)
            if m:
                #print(m)
                for match in m:
                    w = self.WikilinkModal(''.join(match), self.docs, d)
                    d.modals.append(w)
                    if len(w.docs) != 0:
                        apply = '''<a onclick="document.getElementById('{0}').style.display='block'"">{1}</a>'''.format(
                            w.id, w.name)
                        d.content = d.content.replace(
                            "[[" + w.name + "]]", "[[" + apply + "]]")

        # build home page
        self.homepage = self.parse(self.homepage_md)
        self.homepage.template = self.template_homepage
        self.homepage.path = self.out_folder

    def write(self):
        #write pages
        for f in self.folders:
            self.writePage(f)

        #write homepage
        self.writePage(self.homepage)
        self.process_image_folder()

    def writePage(self, page):
        if page.path.exists() == False:
            page.path.mkdir(parents=True, exist_ok=True)
        page.path = page.path / "index.html"
        jinja_env = jinja2.Environment(
            loader=jinja2.FileSystemLoader(self.templates))
        template = jinja_env.get_template(page.template)
        rendered = template.render(page=page, garden=self)
        page.path.write_text(rendered, encoding='utf8')

    def find_images(self, lines):
        lines = str(lines)
        found = []

        found = re.findall(r'src="(.*?)"', lines)
        return found

    class Folder:
        def __init__(self, path):
            self.name = path.stem
            self.title = self.name.title()
            self.url = urllib.parse.quote_plus(str(path.stem))
            self.docs = []
            #self.template = Garden.template_topic

    class WikilinkModal:
        def __init__(self, name, docs, source):
            self.name = name
            self.docs = []
            self.id = "modal" + name.replace(" ", "").lower()

            for d in docs:
                #print(name)
                if d.title != source.title:
                    if " " + name + "s" in d.RAW and d not in self.docs:
                        #print(d.name)
                        self.docs.append(d)
                    if " " + name + " " in d.RAW and d not in self.docs:
                        #print(d.name)
                        self.docs.append(d)
                    if "[[" + name + "]]" in d.RAW and d not in self.docs:
                        #print(d.name)
                        self.docs.append(d)
                    if name.lower() in d.title.lower() and d not in self.docs:
                        self.docs.append(d)


if __name__ == "__main__":
    g = Garden('config.yml')
    g.build()

    g.write()
