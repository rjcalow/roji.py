#<p>*.*\[\[something\]\]*.*<\/p>
#<.>*.*\[\[something\]\]*.*<\/.>
#<.>*.*\[\[something]]*.*<\/.>

import re


class WikiLink:
    def __init__(self, name, originnote, notes):
        self.name = name
        self.originnote = originnote
        self.notes = notes


def search_notes(notes, term, source):
    #print("seaching for " + term)
    results = []
    #term = term.lower()
    for n in notes:

        if str(n.filename) != str(source.filename):

            text = n.fmatter.content + " " + n.fmatter['title']
            text = text.lower()
            if term.lower() in text:
                if text.find(term.lower()) != -1:
                    #print("found '" + term + "' in " + n.fmatter['title'])
                    results.append(n)
                    continue
                else:
                    r = re.findall(term.lower(), text)
                    if r:
                        results.append(n)
    return results

def wikilinkGenerator(notes):
    for n in notes:
        r = re.compile(r'\[\[(.*?)\]\]')
        links = r.findall(n.HTML)
        if links is None: continue

        links = [l.lower() for l in links]

        links = list( dict.fromkeys(links) ) 
        for l in links:
            results = search_notes(notes, l, n)
            if results is None or len(results) == 0: continue
            n.wikilinks.append(WikiLink(l, n, results))


    

# def GenerateList(name, links, siteurl):
#     html = ''
#     for n in links:
#         html += f'\n<li><a href="{siteurl}/{n.fullurl}">{n.title}</a></li>'
    
    
#     return html


                        
# def wikilinkGenerator(siteurl, notes):
#     #wiki links
    
#     for n in notes:
#         #find <p>[[links]]</p>
#         #r = re.compile(r'<.*>*.*\[\[*.*\]\]*.*<\/.*>')
#         tags = re.compile(r'<.>*.*\[\[*.*\]\]*.*<\/.>')
#         lists = re.compile(r'<ul>(?:\n.*)*<\/ul>')

#         htmlblocks = tags.findall(n.HTML)
#         htmlblocks += lists.findall(n.HTML)

#         if htmlblocks:
            
#             LorR = "right"
            
#             for block in htmlblocks:
#                 reg = re.compile(r'\[\[(.*?)\]\]')
#                 links = reg.findall(block)

#                 replacement = f'\n<aside class={LorR}>'
#                 if links:
#                     for l in links:
                        
#                         results = search_notes(notes, l, n)
#                         if len(results) != 0: replacement += f'\n <ul id="{l}Notes"><p>{l} mentioned in</p>\n' + GenerateList(l, results, siteurl) + "\n</ul>"

#                     if replacement.count('\n') < 4: continue

#                     replacement = block + replacement + "</aside>\n"
#                     n.HTML = n.HTML.replace(block, replacement)
                    
#                     #add anchor links
#                     for l in links:
#                         replacement = f'<a href="#{l}Notes">[[{l}]]</a>'
#                         n.HTML = n.HTML.replace(f'[[{l}]]', replacement)


#                     if LorR == "right": LorR = "left"
#                     else: LorR = "right"


        # r = re.compile(r'\[\[(.*?)\]\]')
        # links = r.findall(n.HTML)

        # if links:
        #     for l in links:
        #         #gen url
        #         t = f'<a href="#{n.url}Notes">{l}</a>'
        #         n.HTML = n.HTML.replace("[["+l+"]]", "[["+t+"]]")
                
        #         #find notes to link to
        #         results = search_notes(notes, l, n)

        #         #if any results
        #         if results:
        #             #find html block i.e <p>
        #             reg = re.compile(r'<.>*.*\[\[' +l+'\]\]*.*<\/.>')
        #             htmlblock = reg.findall(n.HTML)

        #             print(htmlblock)
        #             if htmlblock:
        #                 replacement = htmlblock + "\n" + GenerateSidenote(results, n.html)
        #                 n.HTML = n.HTML.replace(htmlblock,replacement)
                
                  
