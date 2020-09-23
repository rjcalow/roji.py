# Roji.py 0.2 WIP digital garden generator
# Used these as basis for the generator backends:
# https://blog.thea.codes/a-small-static-site-generator/
# https://github.com/theacodes/blog.thea.codes/
# 23/9/2020
# encoding: utf8
import frontmatter
import cmarkgfm
import pathlib
import jinja2
import shutil
import re
import os
from datetime import datetime

jinja_env = jinja2.Environment(
    loader=jinja2.FileSystemLoader('templates'),
)

site_name = "Digital garden 🌾"
date = datetime.today().strftime('%d/%m/%Y')


def htmlify(content):
    #using cmarkgfm, but could be swapped out for another flavour of markdown.
    content = cmarkgfm.github_flavored_markdown_to_html(content)
    return content


def files():
    return pathlib.Path('.').glob('in/*.md')


def parse(source):
    # Using nifty Frontmatter!
    post = frontmatter.load(str(source), encoding='utf-8')
    return post


def write_page(page, content):
    # Paths:
    p = pathlib.Path("./docs/{}/".format(page['name'].replace(" ", "-")))
    path = pathlib.Path(
        "./docs/{}/index.html".format(page['name'].replace(" ", "-")))
    # Make folder if it does not exist:
    if p.exists() == False:
        p.mkdir(parents=False, exist_ok=True)
    # Jinja and pathlib write:
    template = jinja_env.get_template('page.html')
    rendered = template.render(page=page, content=content)
    path.write_text(rendered, encoding='utf8')


def write_index(topics):
    # Paths:
    page = parse("index.md")
    path = pathlib.Path("./docs/index.html")
    # Extras:
    page['site_name'] = site_name
    page['index_url'] = "../"
    page['script'] = './scripts/sakura.js'
    page['date'] = date

    page['topics'] = cloudify_topics(topics)
    content = wikilinkify(page.content, path.stem)
    # Render:
    template = jinja_env.get_template('index.html')
    rendered = template.render(page=page, content=(htmlify(content)))
    path.write_text(rendered, encoding='utf8')


def wikilinkify(m, file):
    # A module might do this better,
    # but trying to keep the number of 
    # dependencies down.
    
    # Using re to find links into list
    linkname = (re.findall(r'\[\[(.*?)\]\]', m))
    # remove duplicates
    linkname = list(dict.fromkeys(linkname))

    # Sort list
    for link in linkname:
        link = ''.join(link)
        old = "[[" + link + "]]"
        if "index" in file:
            linkurl = "[" + md_linkify(link, "", "/") + "]"
        else:
            linkurl = "[" + md_linkify(link, "../", "/") + "]"

        x = m.count(link)
        m = m.replace(old, linkurl, x)
    return m

def cloudify_topics(topics):
    #for index page display
    string = ""
    for topic in topics:
        string += md_linkify(topic, "./", "/") + ", "

    return htmlify(string)

def prettify_topics(topics):
    # preparing topics to display on pages
    
    text = ""
    if "," in topics:
        strings = str(topics).split(",")
        for string in strings:
             text += md_linkify(string, "../", "/") + ", "  
    else:
        text = md_linkify(topics, "../", "/")
    
    return htmlify(text) 

def get_topics(pages):
    topics = []
    for page in pages:
        if 'topic' in page:
            if "," in page['topic']:
                strings = str(page['topic']).split(",")
                for string in strings:
                    string = string.lstrip().rstrip()
                    if string != " " and string not in topics: topics.append(string)
            else:
                string = page['topic'].lstrip().rstrip()
                if string != " " and string not in topics: topics.append(string)
    
    # Further clean up
    topics = set(topics)
    #topics = list(dict.fromkeys(topics))
    
    return list(topics)


def write_topic_pages(topics, pages):

    pages = sorted(pages, key=lambda page: page['date'], reverse=True)

    for topic in topics:
        content = "## " + topic.replace("-", " ").title() + " \n"
        for page in pages:
            if 'topic' in page and topic in page['topic']:
                content = content + md_linkify(page['name'].replace(
                    "-", " "), '../', '/') + " <small>" + page['date'] + "</small> </br>"

        content = htmlify(content)
        page = {
            'content': content,
            'site_name': site_name,
            'script': "../scripts/sakura.js",
            'index_url': "../",
            'title': topic,
            'date': date

        }
        p = pathlib.Path("./docs/{}/".format(topic.replace(" ", "-")))
        path = pathlib.Path(
            "./docs/{}/index.html".format(topic.replace(" ", "-")))
        if p.exists() == False:
            p.mkdir(parents=False, exist_ok=True)
        
        # the following finds if a page with the topic name already exists
        # prefering to use the page
        already_a_page = False
        for f in files():
            if topic.replace(" ", "-") == f.stem:
                already_a_page = True
        
        if already_a_page == False:        
            template = jinja_env.get_template('page.html')
            rendered = template.render(page=page, content=content)
            path.write_text(rendered, encoding='utf8')


def find_refences(name):
    found = []
    for f in files():
        text = f.read_text(encoding='utf8')
        lines = text.splitlines()
        temp=[]
        for line in lines:
            x = line.count("[[" + name.replace("-", " ") + "]]")
            if x >= 1:
                temp=[f.stem, line]
                found.append(temp)
    
    return found


def backlinks(name):    
    list_ = find_refences(name)
    if len(list_) == 0:
        return ""
    string = "### Backlinks \n"
    for l in list_:
        string = string + "##### " + md_linkify(l[0], "../", "/") + " \n >" + l[1] + " \n"
    string = htmlify(string)
    return string



def md_linkify(text, base, end):
    text = "["+text.replace("-", " " )+"](" + base + text.replace(" ", "-") + end + ")"
    return text

def housekeeping():
    #extras go here

    ##copy images
    imgs = pathlib.Path('.').glob('imgs/*.jpg')
    p = pathlib.Path('./docs/imgs/')

    if p.exists() == False:
            p.mkdir(parents=False, exist_ok=True)

    for i in imgs:
        path = pathlib.Path(
            "./docs/{}".format(i))
        shutil.copy(str(i),
                    str(path))

    ## copy scripts
    scripts = pathlib.Path('.').glob('scripts/*')
    p = pathlib.Path('./docs/scripts/')

    if p.exists() == False:
            p.mkdir(parents=False, exist_ok=True)

    for i in scripts:
        path = pathlib.Path(
            "./docs/{}".format(i))
        shutil.copy(str(i),
                    str(path))
def main():
    pages = []
    sources = files()

    for source in sources:
        page = parse(source)
        content = wikilinkify(page.content, str(source))
        content = htmlify(content)
        page['site_name'] = site_name
        page['index_url'] = "../"
        page['script'] = '../scripts/sakura.js'
        page['name'] = source.stem
        page['backlinks'] = backlinks(source.stem)
        # keep topics (pretty html) and topic (yaml data) serpate
        if "topic" in page: page['topics'] = prettify_topics(str(page['topic']))
        write_page(page, content)

        pages.append(page)

    topics = get_topics(pages)
    write_topic_pages(topics, pages)
    write_index(topics)
    housekeeping()


if __name__ == "__main__":
    main()
