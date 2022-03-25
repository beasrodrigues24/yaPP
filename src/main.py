import sys
import ply.lex as lex

tokens = ["BOLD", 
          "ITALIC",
          "UNDERLINE",
          "CINLINE",
          "SUBSCRIPT",
          "SUPERSCRIPT",
          "STRIKEOUT",
          "HREF",
          "CODE",
          "SECTION",
          "SPACE",
          "WORD",
          "ESCAPEDWORD",
          "COMMENT",
          "TABLE",
          "ROW",
          "TABLEHEADER",
          "TABLEELEMENT",
          "IMAGE",
          "SPECIAL",
          "NAME",
          "LINE",
          "TITLE",
          "ITEM",
          "LIST",
          "RAW",
          "RINLINE"
          "ORDLIST",
          "ENUMTYPE",
          "DSCLIST",
          "OBJECT",
          "DESCRIPTION",
          "NEWLINE",
          "END"
]

states = [
    ('bold', 'inclusive'),
    ('italic', 'inclusive'),
    ('underline', 'inclusive'),
    ('codeinline', 'inclusive'),
    ('subscript', 'inclusive'),
    ('superscript', 'inclusive'),
    ('strikeout', 'inclusive'),
    ('href', 'inclusive'),
    ('linktitle', 'inclusive'),
    ('imagetitle', 'inclusive'),
    ('code', 'exclusive'),
    ('section', 'inclusive'),
    ('sectiontitle', 'inclusive'),
    ('table', 'exclusive'),
    ('title', 'exclusive'),
    ('row', 'exclusive'),
    ('tableheader', 'inclusive'),
    ('tableelement', 'inclusive'),
    ('image', 'inclusive'),
    ('list', 'exclusive'),
    ('item', 'inclusive'),
    ('ordlist', 'exclusive'),
    ('enumtype', 'exclusive'),
    ('dsclist', 'exclusive'),
    ('dlobject', 'inclusive'),
    ('dldescription', 'inclusive'),
    ('width', 'exclusive'),
    ('height', 'exclusive'),
    ('special', 'exclusive'),
    ('raw', 'exclusive'),
    ('rawinline', 'inclusive')
]

def t_ANY_eof(t):
    if(len(t.lexer.lexstatestack) != 0):
        t.lexer.correctly_finished = False;
    else:
        t.lexer.correctly_finished = True;
        
def t_TITLE(t):
    r'\[t\ '
    t.lexer.with_title = True
    t.value = "<title>"
    t.lexer.push_state('title')
    return t

def t_title_WORD(t):
    r'[^[\]\s]+'
    return t

def t_title_SPACE(t):
    r'\s+'
    t.value = ' '
    return t
    
def t_title_END(t):
    r'\s*\]\s*'
    t.value = "</title>\n</head>\n<body>\n"
    t.lexer.pop_state()
    return t

def t_BOLD(t):
    r'\[b\ '
    t.value = "<b>"
    t.lexer.push_state('bold')
    return t
    
def t_bold_END(t):
    r'\s*\]'
    t.value = "</b>"
    t.lexer.pop_state()
    return t

def t_ITALIC(t):
    r'\[i\ '
    t.value = "<i>"
    t.lexer.push_state('italic')
    return t

def t_italic_END(t):
    r'\s*\]'
    t.value = "</i>"
    t.lexer.pop_state()
    return t

def t_UNDERLINE(t):
    r'\[u\ '
    t.value = "<u>"
    t.lexer.push_state('underline')
    return t
    
def t_underline_END(t):
    r'\s*\]'
    t.value = "</u>"
    t.lexer.pop_state()
    return t
    
def t_CINLINE(t):
    r'\[c\ '
    t.value = "<code>"
    t.lexer.push_state('codeinline')
    return t
    
def t_codeinline_END(t):
    r'\s*\]'
    t.value = "</code>"
    t.lexer.pop_state()
    return t

def t_SUBSCRIPT(t):
    r'\[sub\ '
    t.value = "<sub>"
    t.lexer.push_state('subscript')
    return t
    
def t_subscript_END(t):
    r'\s*\]'
    t.value = "</sub>"
    t.lexer.pop_state()
    return t
    
def t_SUPERSCRIPT(t):
    r'\[sup\ '
    t.value = "<sup>"
    t.lexer.push_state('superscript')
    return t
    
def t_superscript_END(t):
    r'\s*\]'
    t.value = "</sup>"
    t.lexer.pop_state()
    return t

def t_STRIKEOUT(t):
    r'\[stk\ '
    t.value = "<del>"
    t.lexer.push_state('strikeout')
    return t

def t_strikeout_END(t):
    r'\s*\]'
    t.value = "</del>"
    t.lexer.pop_state()
    return t

def t_SPECIAL(t):
    r'\[sp\s*'
    t.lexer.push_state('special')
    
def t_special_WORD(t):
    r'[a-zA-Z]+'
    t.value = f"&{t.value};"
    return t

def t_HREF(t):
    r'\[href\ [^ ]+\ ?'
    t.value = f"<a href=\"{t.value[6:-1]}\">"
    t.lexer.push_state('href')
    return t

def t_href_END(t):
    r'\]\n?'
    t.value = "</a>\n"
    t.lexer.pop_state()
    return t

def t_href_NAME(t):
    r'\[name\ '
    t.lexer.push_state('linktitle')
    
def t_IMAGE(t):
    r'\[img\s+[^ ]+\ ?'
    t.value = f"<img src=\"{t.value[5:-1].strip()}\""
    t.lexer.push_state('image')
    return t

def t_image_END(t):
    r'\]'
    t.value = ">"
    t.lexer.pop_state()
    return t

def t_image_NAME(t):
    r'\[name\ '
    t.value = " alt=\""
    t.lexer.push_state('imagetitle')
    return t

def t_imagetitle_END(t):
    r'\]'
    t.value = "\""
    t.lexer.pop_state()
    return t

def t_image_WIDTH(t):
    r'\s*\[w\ '
    t.lexer.push_state("width")
    
def t_width_WORD(t):
    r'\d+(\.\d+)?'
    t.value = f" width={t.value}"
    return t

def t_image_HEIGHT(t):
    r'\s*\[h\ '
    t.lexer.push_state("height")
    
def t_height_WORD(t):
    r'\d+(\.\d+)?'
    t.value = f" height={t.value}"
    return t

def t_CODE(t):
    r'\[code\ ?(\w*)\n'
    lang = t.value[6:-1]
    if lang:
        t.value = f"<pre><code class=\"language-{lang}\">\n"
    else:
        t.value = "<pre><code>\n"
    t.lexer.push_state('code')
    return t
    
def t_code_END(t):
    r'\s*code\]\n?'
    t.value = "</code></pre>\n"
    t.lexer.code_ident = None
    t.lexer.pop_state()
    return t
    
def t_code_LINE(t):
    r'.+\n'
    if t.lexer.code_ident == None:
        t.lexer.code_ident = len(t.value) - len(t.value.lstrip())
    t.value = t.value[t.lexer.code_ident:]
    return t
    
def t_SECTION(t):
    r'\[sec\ '
    t.lexer.header_num += 1
    t.value = f"<div>\n<h{t.lexer.header_num}>"
    t.lexer.push_state('section')
    t.lexer.push_state('sectiontitle')
    return t

def t_sectiontitle_END(t):
    r'\n\s*'
    t.value = f"</h{t.lexer.header_num}>\n"
    t.lexer.pop_state()
    return t
    
def t_section_END(t):
    r'\s*sec\]\n?'
    t.value = "</div>\n"
    t.lexer.pop_state()
    t.lexer.header_num -= 1
    return t

def t_COMMENT(t):
    r'%%.*\n?'

def t_TABLE(t):
    r'\[table\n'
    t.value = "<table>\n"
    t.lexer.push_state('table')
    return t
    
def t_table_END(t):
    r'\s*table\]'
    t.value = "</table>\n"
    t.lexer.pop_state()
    return t
    
def t_table_ROW(t):
    r'\s*\[row\ '
    t.value = "<tr>\n"
    t.lexer.push_state('row')
    return t
    
def t_row_END(t):
    r'\s*\]'
    t.value = "</tr>\n"
    t.lexer.pop_state()
    return t
    
def t_row_TABLEHEADER(t):
    r'\s*\[h\ '
    t.value = "<th>"
    t.lexer.push_state('tableheader')
    return t
    
def t_tableheader_END(t):
    r'\s*\]'
    t.value = "</th>\n"
    t.lexer.pop_state()
    return t

def t_row_TABLEELEMENT(t):
    r'\s*\[e\ '
    t.value = "<td>"
    t.lexer.push_state('tableelement')
    return t
    
def t_tableelement_END(t):
    r'\s*\]'
    t.value = "</td>"
    t.lexer.pop_state()
    return t
    
def t_LIST(t):
    r'\[list\n'
    t.value = "<ul>\n"
    t.lexer.push_state('list')
    return t

def t_list_END(t): 
    r'\s*list\]'
    t.value = "</ul>\n"
    t.lexer.pop_state()
    return t

def t_DSCLIST(t):
    r'\s*\[dsclist\n'
    t.value = "<dl>\n"
    t.lexer.push_state("dsclist")
    return t

def t_dsclist_OBJECT(t):
    r'\s*\[obj\ '
    t.value = "<dt>"
    t.lexer.push_state("dlobject")
    return t 

def t_dlobject_END(t):
    r'\s*\]'
    t.value = "</dt>\n"
    t.lexer.pop_state()
    return t 

def t_dsclist_DESCRIPTION(t):
    r'\s*\[dsc\ '
    t.value = "<dd>"
    t.lexer.push_state("dldescription")
    return t 

def t_dldescription_END(t):
    r'\s*\]'
    t.value = "</dd>\n"
    t.lexer.pop_state()
    return t

def t_dsclist_END(t):
    r'\s*dsclist]'
    t.value = "</dl>\n"
    t.lexer.pop_state()
    return t

def t_ORDLIST(t):
    r'\[ordlist\ ?'
    t.lexer.push_state("ordlist")
    t.lexer.push_state("enumtype")

def t_enumtype_ENUMTYPE(t):
    r'[a-zA-Z]{0,1}.*\n'
    if t.value[0] != '\n':
        t.value = f"<ol type={t.value[0]}>\n"
    else:
        t.value = "<ol>\n"
    t.lexer.pop_state()
    return t
    
def t_ordlist_list_ITEM(t):
    r'\s*\[item\ '
    t.value = "<li>"
    t.lexer.push_state('item')
    return t

def t_item_END(t):
    r'\s*\]'
    t.value = "</li>\n"
    t.lexer.pop_state()
    return t
    
def t_ordlist_END(t):
    r'\s*ordlist\]'
    t.value = "</ol>"
    t.lexer.pop_state()
    return t

def t_RAW(t):
    r'\[raw\ ?\n'
    t.lexer.push_state('raw')
    
def t_raw_END(t):
    r'\s*raw\]\n?'
    t.lexer.code_ident = None
    t.lexer.pop_state()

def t_raw_LINE(t):
    r'.+\n'
    if t.lexer.code_ident == None:
        t.lexer.code_ident = len(t.value) - len(t.value.lstrip())
    t.value = t.value[t.lexer.code_ident:]
    return t

def t_RINLINE(t):
    r'\s*\[r\ '
    t.lexer.push_state('rawinline')

def t_rawinline_END(t):
    r'\s*\]'
    t.lexer.pop_state()
    return t
    
def t_special_linktitle_width_height_END(t):
    r'\s*\]'
    t.lexer.pop_state()

def t_NEWLINE(t):
    r'\n{2,}'
    t.value = "<br>"
    return t

def t_SPACE(t):
    r'\s+'
    t.value = ' '
    return t

def t_ESCAPEDWORD(t):
    r'\\[^\s]+'
    t.value = t.value.replace("\\", "")
    return t

def t_WORD(t):
    r'[^[\]\s\\]+'
    return t

def t_ANY_error(t):
    r'.*|\n'
    print(f"Illegal character: {t.value} at {t.lexpos}:{t.lineno}")

args = sys.argv
sys.tracebacklimit = 0 # hides traceback

if(args[1] == "-h" or args[1] == "--help"):
    print("""
        yaPP allows you to convert an .ya file with the defined syntax to an .html file.
        
        Usage: [input_file] [output_file]
        - The input file should have the .ya extension.
        - The output file should have the .html extension.
        
        To check the "yet another PreProccessor" syntax, please check our manual.
    """)
    exit() # better way to do this???

if(len(args) != 3):
    raise Exception("Wrong number of arguments. Use \"--help\" for more information.")

input_name = args[1]

if(input_name[-2:] != 'ya'):
    raise Exception("Unknown file extension. Use \"--help\" for more information.")

f = open(args[1], "r")
file_content = f.read()
f.close()

output_name = args[2]
if(output_name[-4:] != 'html'):
    raise Exception("Unknown file extension. Use \"--help\" for more information.")

lexer = lex.lex()
lexer.header_num = 0
lexer.code_ident = None
lexer.correctly_finished = True
lexer.with_title = False
lexer.input(file_content)
tmp_str = ""

for tok in lexer:
    tmp_str += tok.value
    
if(lexer.correctly_finished):
    out_str = '''
<!DOCTYPE html>
<html>
<head>
<link rel="stylesheet"
      href="https://cdnjs.cloudflare.com/ajax/libs/highlight.js/11.5.0/styles/default.min.css">
<script src="https://cdnjs.cloudflare.com/ajax/libs/highlight.js/11.5.0/highlight.min.js"></script>
<script>hljs.highlightAll();</script>
'''
    output = open(output_name, "w")
    if not lexer.with_title:
        out_str += "</head>\n<body>\n"
    output.write(out_str + tmp_str)
    output.write("</body>\n</html>")
    output.close()
else:
    print("Syntax error")

