
# encoding: utf8
"""
roji.py converts a folder of markdown files into a static digital garden with Sakura.css 
https://github.com/rjcalow/roji.py
version 0.2 13/9/2020
"""
import frontmatter
import markdown
from jinja2 import Environment, FileSystemLoader
import os
import platform
import shutil
import re
import time
import http.server
import socketserver
import sys  # for arguments

from markdown.extensions.wikilinks import WikiLinkExtension
# site name
site_name = "Roji.py digital garden 🌱"

# attempt at making the script work on linux or darwin, should have used pathlib
p = ""
if platform.system() == "Windows":
    p = "\\"
if platform.system() == "Linux" or platform.system() == "Darwin":
    p = "/"

# paths
path = os.getcwd()
# where .md files are:
in_folder = path + p + "in" + p
# where the html, imgs and scripts will go:
out_folder = path + p + "docs" + p
# where the images are
image_folder = path + p + "imgs" + p
# where any scripts are
script_folder = path + p + "scripts" + p

pages_=[]


def pages(t):
    files = os.listdir(in_folder)
    if t != 'all':
        files.remove("index.md")
    return files


def process_markdown_files():
    for f in pages(''):
        if ".md" in str(f) and f != "index.md":
            fpath = in_folder + str(f)
            # read md file
            metadata, content = read_md(fpath)
            content = content + add_refences(str(f))
            # convert md to html
            metadata["file"] = "/" + str(f.replace(".md", "/"))
            
            pages_.append(metadata)
            output = out_folder + str(f.replace(".md", p)) + "index.html"
            render_page(output, content, metadata)


def process_index():
    f = in_folder + "index.md"
    metadata, content = read_md(f)
    content = content + add_refences(str(f))
    output = out_folder + "index.html"
    render_index(output, content, metadata)


def read_md(file):
    page = frontmatter.load(file)
    metadata = page.metadata

    # convert [[links]] and data into markdown
    content = markdown.markdown(
        convert_brackets_to_md_links(page.content, file))

    if "topic" in metadata:
        if "subtopic" != metadata:
            metadata["subtopic"] = ""
        categorize(metadata["topic"], metadata["subtopic"], file, metadata["date"])

    return metadata, content


def find_refences(name):
    found = []
    for f in pages('all'):
        if ".md" in str(f):
            with open(in_folder + f, encoding="utf8", errors='ignore') as infile:
                for s in infile:
                    if "[[" in s:
                        try:
                            linkname = re.search(r'\[\[(.*?)\]\]', s).group(1)
                            if (name.replace(".md", "")) == (linkname.replace(" ", "-")):

                                f = str(f.replace(" ", "-").replace(".md", ""))
                                if "index" in f:
                                    linkurl = "../" + f + ".html"
                                else:
                                    linkurl = "../" + f + "/"

                                mdlink = "[" + f + "]("+linkurl+") : "

                                found.append(mdlink + "\n >" + s)
                        except:
                            pass
    return found


def add_refences(name):
    list_ = []
    list_ = find_refences(name)
    if len(list_) == 0:
        return ""
    string = "### Backlinks \n"
    for l in list_:
        string = string + str(l) + "\n"
    string = markdown.markdown(string)
    return string


def convert_brackets_to_md_links(m, file):
    # could also use markdown ext called wikilinks
    for line in m.splitlines():
        try:
            linkname = re.search(r'\[\[(.*?)\]\]', line).group(1)
            old = "[[" + linkname + "]]"
            if "index" in file:
                linkurl = "" + linkname.replace(" ", "-") + "/"
            else:
                linkurl = "../" + str(linkname.replace(" ", "-")) + "/"
            mdlink = "[[["+str(linkname)+"]]]("+linkurl+")"
            m = m.replace(old, mdlink)

        except:
            continue

    return m


def categorize(cat, sub, file, date):
    filename = str(file.split(os.path.sep)[-1].replace(".md", ".html"))
    # listt = [''.join(cat), ''.join(sub), filename, ''.join(date)]
    # topics.append(listt)


def create_menu():
    # need a method for creating a basic menu
 
    return()


def render_page(filename, content, metadata):
    template_env = Environment(loader=FileSystemLoader(searchpath='./'))
    template = template_env.get_template('page_template.html')

    foldername = str(filename.split(os.path.sep)[-2])

    # check and create paths
    # the and stops the output folder being created by the root index.html
    if os.path.exists(out_folder + foldername) == False and foldername not in out_folder:
        os.makedirs(out_folder + foldername)

    with open(filename, 'w', encoding='utf8') as _file:
        _file.write(
            template.render(
                site_name=site_name,
                title=metadata['title'],
                date=metadata['date'],
                script="../scripts/sakura.js",
                index_url="../",
                content=content,
            )
        )


def render_index(filename, content, metadata):
    template_env = Environment(loader=FileSystemLoader(searchpath='./'))
    template = template_env.get_template('index_template.html')

    with open(filename, 'w', encoding='utf8') as _file:
        _file.write(
            template.render(
                site_name=site_name,
                title=metadata['title'],
                date=metadata['date'],
                script="scripts/sakura.js",
                index_url="#",
                content=content,
                #menu=create_menu()
            )
        )


def house_keeping():
    folders = [(image_folder), (script_folder)]

    for folder in folders:
        # if source folder doesn't exist do not panic
        if os.path.exists(folder) == False:
            continue
        else:

            foldername = str(folder.split(os.path.sep)[-2])

            # make folder in out_folder
            if os.path.exists(out_folder + foldername) == False:
                os.makedirs(out_folder + foldername)

            files_ = os.listdir(folder)
            for f in files_:
                shutil.copy(str(folder + f),
                            str(out_folder + foldername + p + f))


def serve():
    # need rewriting so that the out_folder is served
    PORT = 8000

    handler = http.server.SimpleHTTPRequestHandler

    with socketserver.TCPServer(("", PORT), handler) as httpd:
        print("Server started at http://localhost:" + str(PORT) +
              "/" + str(out_folder.split(os.path.sep)[-2]))
        httpd.serve_forever()


def main(args):
    start = time.time()

    process_markdown_files()
    process_index()
    house_keeping()

    end = time.time()
    converted = len(os.listdir(out_folder))
    print("Generated " + str(converted) +
          " pages in ", str(end - start) + " seconds.")
    # method to option server
    if "serve" in args:
        serve()


if __name__ == "__main__":
    if not hasattr(sys, 'argv'):
        sys.argv = ['']
    #print (sys.argv)
    main(sys.argv)
