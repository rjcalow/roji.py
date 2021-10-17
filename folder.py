import urllib
import pathlib
import yaml
from datetime import datetime
from note import Note

class Folder:
    def __init__(self, source, basepath, parent):
        '''
        #####################################
        • Deal w/ paths
            ↳ folder level
            ↳ find children in path
            ↳ urlize path

        • Scrape notes within folder path
            ↳ use note and img class
            ↳ sort by date
        #####################################
        '''
        self.source = source
        self.rpath = source.relative_to(basepath)
        self.mdfiles = basepath
        self.folderlevel = len(self.rpath.parts) -1
        self.name = str(source.stem)
        #self.title = self.name.title()
        self.title = self.name


        self.url = urllib.parse.quote_plus(str(source.stem))
        self.fullurl = ""
        for p in self.rpath.parts:
            self.fullurl += urllib.parse.quote_plus(str(p)) + "/"

        self.writepath = pathlib.Path(self.fullurl)


        self.parent = parent    
        self.children = []


        for child in self.source.iterdir():
            if child.is_dir():
                self.children.append(Folder(child, self.mdfiles, self))

            if child.name == "about.yml":
                with open(child, "r", encoding='utf-8') as f:
                    config = yaml.load(f, Loader=yaml.SafeLoader)

                for key in config:
                    setattr(self, key, config[key])                    
                        



        self.parents = self.retrieve_parents(self)
        for p in self.parents:
            print (p.title)

        self.notes = []
        for f in self.source.glob("*.md"):
            self.notes.append(Note(f, self))

        self.notesbydate = []
        self.notesbydate = sorted(self.notes, key=lambda note: datetime.strptime(
            note.fmatter['date'], "%d/%m/%Y"), reverse=True)


    def retrieve_parent(self, child):
        if child.parent != None:
            return child.parent
        else:
            return None

    def retrieve_parents(self, child):
        folders = []
        parent = self.retrieve_parent(child)
        if parent == None: return folders
        else: folders.append(parent)
        for i in range (child.folderlevel):
            parent = self.retrieve_parent(parent)
            if parent != None: folders.append(parent)
            else: 
                folders = sorted(folders, key=lambda folder: folder.folderlevel, reverse=False)
                return folders
    
    def allchildren(self):
        if len(self.children) == 0 or None: return None

        children = []
        children += self.children
        
        for c in children:
                
            if len(c.children) != 0:
                children.append(c.children)
                   
            #if len(children)==0:
                #break
        
        return children

