'''
My first attempt at a markdown python extension
based on https://alexwlchan.net/2017/03/extensions-in-python-markdown/

'''

from markdown.preprocessors import Preprocessor
from markdown.extensions import Extension
import re

class findTopics(Extension):
    def extendMarkdown(self, md, md_globals):
        md.preprocessors.add('line_subn', findTopicsProcessor(md), '_begin')

class findTopicsProcessor(Preprocessor):
    def run(self, lines):
        new_lines = []
        #topic = (re.match(r'{(.*?)}'))
        reg = re.compile(r'{(.*?)}')
        for line in lines:
                        
            m= reg.findall(line)
            if m:
                
                for match in m:
                    
                    new = '<a href="../topics/'+ match.replace(" ", "_").replace("-","_") + '">' + match + '</a>'
                    line = line.replace(match, new).replace("{","").replace("}","")
                
                new_lines.append(line) 
                     
            else:
                new_lines.append(line)
        return new_lines


class WikiBrackets(Extension):
    def extendMarkdown(self, md, md_globals):
        md.preprocessors.add('line_subn', findwikiBrackets(md), '_begin')

class findwikiBrackets(Preprocessor):
    def run(self, lines):
        new_lines = []
        
        reg = re.compile(r'\[\[(.*?)\]\]')
        topics = re.compile(r'{(.*?)}')

        for line in lines:
                        
            m= reg.findall(line)
            if m:
                #print(m)
                for match in m:
                    
                    new = '<a href="../'+ match.replace(" ", "_").replace("-","_") + '/">' + match + '</a>'
                    line = line.replace(match, new).replace("[[","").replace("]]","")
          
            m= topics.findall(line)
            if m:
                #print(m)
                for match in m:
                    
                    new = '<a href="../topics/'+ match.replace(" ", "_").replace("-","_") + '">' + match + '</a>'
                    line = line.replace(match, new).replace("{","").replace("}","")
                
                                     
            
            new_lines.append(line)
        
        return new_lines