# Roji.py 0.4.5 WIP digital garden generator
# Used these as a starting point / basis for the generator backends:
# https://blog.thea.codes/a-small-static-site-generator/
# https://github.com/theacodes/blog.thea.codes/
# 14/11/2020
# encoding: utf8
import frontmatter
import cmarkgfm
import pathlib
import jinja2
import shutil
import re
import os
import yaml
from datetime import datetime

file = open('config.yml', 'r')
config = yaml.load(file, Loader=yaml.FullLoader)


jinja_env = jinja2.Environment(
    loader=jinja2.FileSystemLoader(config['templates']),
)

site_name = config['site_name']
author = config['author']
out_folder = pathlib.Path (config['out_folder'])

#uk date
date = datetime.today().strftime('%d/%m/%Y')


def htmlify(content):
    #using cmarkgfm, but could be swapped out for another flavour of markdown.
    content = cmarkgfm.github_flavored_markdown_to_html(content)
    return content


def files():
    p = pathlib.Path(config["markdown_folder"])
    return p.glob('*.md')


def parse(source):
    # Using nifty Frontmatter!
    post = frontmatter.load(str(source), encoding='utf-8')
    return post


def write_page(page, content):
    # Paths:
    p = out_folder.joinpath("{}".format(page['name'].replace(" ", "-").lower()))
    path = p.joinpath("index.html".format(page['name'].replace(" ", "-").lower()))

    # Make folder if it does not exist:
    if p.exists() == False:
        p.mkdir(parents=False, exist_ok=True)

    
    # Jinja and pathlib write:
    template = jinja_env.get_template('page.html')
    rendered = template.render(page=page, content=content)
    path.write_text(rendered, encoding='utf8')
    
# adds extras for tufte.css    
def tuftify(content):
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

    #trying to add sections for tufte.css
    #and not succeeding
    #content = re.sub(r'<p>','<section><p>',content)    
    #content = re.sub(r'</p>','</p></section>',content)
    
    # content = re.sub(r'<\/h2>','</h2><section>',content) 
    #content = re.sub(r'<h2>','</section><h2>',content)   
    return content

def write_index(topics, new):
    # Paths:
    page = parse("index.md")
    path = out_folder.joinpath("index.html")
    # Extras:
    page['site_name'] = site_name
    page['index_url'] = "../"
    #page['script'] = './scripts/sakura.js'
    page['date'] = date
    page['new'] = new
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
    links = (re.findall(r'\[\[(.*?)\]\]', m))
    # remove duplicates
    links = list(dict.fromkeys(links))

    # Sort list
    for link in links:
        link = ''.join(link)
        old = "[[" + link + "]]"
        if "index" in file:
            linkurl = "[" + md_linkify(link, "", "/") + "]"
        else:
            linkurl = "[" + md_linkify(link, "../", "/") + "]"

        x = m.count(link)
        m = m.replace(old, linkurl, x)

    ## {topic} links 
    links = (re.findall(r'{(.*?)}', m))
    # remove duplicates
    links = list(dict.fromkeys(links))
    for link in links:
        old = "{" + link + "}"
        if "index" in file:
            linkurl = "[" + md_linkify(link, "./topics/", "/") + "]"
        else:
            linkurl = "[" + md_linkify(link, "../topics/", "/") + "]"

        x = m.count(link)
        m = m.replace(old, linkurl, x)


    return m


def cloudify_topics(topics):
    #for index page display
    string = ""
    topics.sort(reverse=False)
    for topic in topics:
        string += md_linkify(topic, "./topics/", "/") + ", "

    return htmlify(string)

def prettify_topics(topics):
    # preparing topics to display on pages
    
    text = ""
    if "," in topics:
        strings = str(topics).split(",")
        for string in strings:
             text += md_linkify(string.lstrip().rstrip(), "../topics/", "/") + ", "  
    else:
        text = md_linkify(topics, "../topics/", "/")
    
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
    #pages_by_date = sorted(pages, key=lambda page: page['date'], reverse=False)
    # Using datetime strptime instead of above
    pages_by_date = sorted(pages,key=lambda page: datetime.strptime(page['date'], "%d/%m/%Y"), reverse=True)
    
    topic_folder = out_folder.joinpath("topics")
    
    for topic in topics:
        #content = "## " + topic.replace("-", " ").title() + " \n"
        content = ""
        for page in pages_by_date:
            if 'topic' in page:

                if "," in page['topic']:
                    strings = str(page['topic']).split(",")
                    for string in strings:
                        if string.lower().lstrip().rstrip()  == topic.lower().lstrip().rstrip() :
                            content = content + md_linkify(page['name'].replace("-", " "), '../../', '/') + " <small>" + page['date'] + "</small></br> \n"
                            break


                if topic.lower() == page['topic'].lower(): content = content + md_linkify(page['name'].replace("-", " "), '../../', '/') + " <small>" + page['date'] + "</small></br> \n"


        content = htmlify(content)
        page = {
            'content': content,
            'site_name': site_name,
            'index_url': "../../",
            'title': topic,
            'date': date

        }

        topicpath = str(topic.replace(" ", "-").lower())
        p = topic_folder.joinpath(topicpath)
        path = p.joinpath("index.html" )
        
        if p.exists() == False:
            p.mkdir(parents=True, exist_ok=True)
        
        # the following finds if a page with the topic name already exists
        # prefering to use the page
        already_a_page = False
        for f in files():
            if topic.replace(" ", "-") == f.stem:
                already_a_page = True
        
        if already_a_page == False:        
            template = jinja_env.get_template('topic.html')
            rendered = template.render(page=page, content=content)
            path.write_text(rendered, encoding='utf8')


def find_refences(name):
    found = []
    
    for f in files():
        text = f.read_text(encoding='utf8')
        lines = text.splitlines()
        temp=[]
        for line in lines:
            # need to use re or str.lower() for case
            #line = line.lower()
            x = line.lower().count("[[" + name.replace("-", " ").lower() + "]]")
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
    text = "["+text.replace("-", " " )+"](" + base + text.replace(" ", "-").lower() + end + ")"
    return text


def new_articles(pages):
    pages_by_date = sorted(pages,key=lambda page: datetime.strptime(page['date'], "%d/%m/%Y"), reverse=True)

    new = ""

    for page in pages_by_date[0:5]:
        new += " - " + md_linkify(page['name'], "./", "/") + " *" + page['date'] + "* \n"

    return htmlify(new)


def housekeeping():
    #extras go here
    ##copy images
    imgs_in = pathlib.Path(config['img_folder'])
    imgs_out = out_folder.joinpath(imgs_in.name)
    #print (imgs_out)
    imgs = imgs_in.glob('*')
    

    #if imgs outfolder doesnt exist make it
    if imgs_out.exists() == False:
            imgs_out.mkdir(parents=False, exist_ok=True)

    for i in imgs:
        path = imgs_out.joinpath(i.name)
        shutil.copy(str(i), str(path))

    assets_folder = pathlib.Path("assets")
    assets_folder_out = out_folder.joinpath("assets")

    if assets_folder_out.exists() == False:
        assets_folder_out.mkdir(parents=False, exist_ok=True)

    assets_ = assets_folder.glob('*')
    for a in assets_:
        path = assets_folder_out.joinpath(a.name)
        
        shutil.copy(str(a), str(path))

def main():
    count = 0
    pages = []
    sources = files()
    
    for source in sources:
        page = parse(source)
        
        content = wikilinkify(page.content, str(source))
        
        content = htmlify(content)
        content = tuftify(content)
        page['author'] = config['author']
        page['site_name'] = config['site_name']
        page['index_url'] = "../"    
        page['name'] = source.stem
        page['backlinks'] = backlinks(source.stem)
        # keep topics (pretty html) and topic (yaml data) apart
        if "topic" in page: page['topics'] = prettify_topics(str(page['topic']))
        write_page(page, content)

        pages.append(page)
        count += 1

    topics = get_topics(pages)
    write_topic_pages(topics, pages)
    new = new_articles(pages)
    write_index(topics, new)
    housekeeping()

    print("Processed " + str(count) + " files to " + str(out_folder))

if __name__ == "__main__":
    main()
