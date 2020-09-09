
# encoding: utf8
"""
roji.py converts a folder of markdown files into a static digital garden with Sakura.css 
https://github.com/rjcalow/roji.py
version 0.1 9/9/2020
"""
import yaml
import markdown
import pystache
import os
import platform
import shutil
import re
import time
import http.server
import socketserver

# site name
site_name = "My digital garden 🌱"

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
files = os.listdir(in_folder)


def move_assets():
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


def find_refences(name):
    found = []
    for f in files:
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

                                mdlink = "[[[" + f + "]]]("+linkurl+") : "

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


def read_md(file):
    with open(file, encoding="utf8", errors='ignore') as infile:

        for s in infile:
            if s.startswith('---'):
                break

        yaml_lines = []
        for s in infile:
            if s.startswith('---'):
                break
            else:
                yaml_lines.append(s)

        ym = ''.join(yaml_lines)

        md_data = []
        for s in infile:
            s = convert_brackets_to_md_links(s, file)
            md_data.append(s)
        md = ''.join(md_data)

    # adding extras to the yaml here
    # further changes could be made here for optional content
    ym = ym + 'site_name: "' + site_name + '"\n'
    if "index" in file:
        ym = ym + 'script: "scripts/sakura.js"\n'
        ym = ym + 'index_url: "#"'
    else:
        ym = ym + 'script: "../scripts/sakura.js"\n'
        ym = ym + 'index_url: "../"'

    info = yaml.load(ym, yaml.SafeLoader)
    content = markdown.markdown(md)

    return info, content


def convert_brackets_to_md_links(line, file):
    try:
        linkname = re.search(r'\[\[(.*?)\]\]', line).group(1)

        old = "[[" + linkname + "]]"
        if "index" in file:
            linkurl = "" + linkname.replace(" ", "-") + "/"
        else:
            linkurl = "../" + str(linkname.replace(" ", "-")) + "/"
        mdlink = "[[["+str(linkname)+"]]]("+linkurl+")"
        line = line.replace(old, mdlink)
    except:
        return line

    return line


def template():
    with open('template.html') as infile:
        template = infile.read()
    return template


def render(content, info):
    info['content'] = content
    html = pystache.render(template(), info)
    return html


def save(html, filename):
    foldername = str(filename.split(os.path.sep)[-2])

    # check and create paths
    # the and stops the output folder being created by the root index.html
    if os.path.exists(out_folder + foldername) == False and foldername not in out_folder:
        os.makedirs(out_folder + foldername)

    with open(filename, "w", encoding='utf8') as f:
        f.write(html)
        f.close()


def serve():
    # need rewriting so that the out_folder is served
    PORT = 8000

    handler = http.server.SimpleHTTPRequestHandler

    with socketserver.TCPServer(("", PORT), handler) as httpd:
        print("Server started at http://localhost:" + str(PORT) +
              "/" + str(out_folder.split(os.path.sep)[-2]))
        httpd.serve_forever()


def main():
    start = time.time()
    converted = 0

    for f in files:
        if ".md" in str(f):

            fpath = in_folder + str(f)

            # read md file
            info, content = read_md(fpath)
            # add references
            content = content + add_refences(str(f))

            if "index.md" in f:
                output = out_folder + str(f.replace(".md", ".html"))
            else:
                output = out_folder + \
                    str(f.replace(".md", p)) + "index.html"

            # convert md to html
            html = render(content, info)

            # write html
            save(html, output)
            converted += 1
    # finish up
    move_assets()
    end = time.time()
    print("Generated " + str(converted) +
          " pages in ", str(end - start) + " seconds.")
    # add a method to option server
    serve()


if __name__ == "__main__":
    main()
