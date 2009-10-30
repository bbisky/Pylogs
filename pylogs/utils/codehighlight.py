import re
#from pygments import highlight, lexers, formatters

def highlight_code(text):
    '''highlight the [code lang="xxx"][/code] block.'''
    return text
    #r = re.compile(r'\[code\s+lang="(\w+)"\](.+?)\[/code\]',re.DOTALL|re.I|re.M)
    #r = re.compile(r'<pre\s+class="(\w+)">(.+?)</pre>',re.DOTALL|re.I|re.M)    
    #allmatches = r.findall(text)
   # try:
    #    for i in range(0,len(allmatches)):
    #        text = r.sub('$CODE$',text)
    #        text = text.replace('$CODE$',hl(allmatches[i][0],allmatches[i][1]),1)
    #except:pass
   # return text

#def hl(lang,code):
    #code = code.replace("<br />","\n")    
    #le = lexers.get_lexer_by_name(lang)
    #highlightedStr =  highlight(code,
  #                       le,
  #                       formatters.HtmlFormatter())
   # return highlightedStr