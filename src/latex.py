import sys
import re
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
          "COMMENT",
          "TABLE",
          "ROW",
          "TABLEHEADER",
          "TABLENCOLS",
          "TABLEELEMENT",
          "IMAGE",
          "SPECIAL",
          "NAME",
          "LINE",
          "TITLE",
          "ITEM",
          "LIST",
          "ORDLIST",
          "ENUMTYPE",
          "DSCLIST",
          "OBJECT",
          "DESCRIPTION",
          "NEWLINE",
          "RAW",
          "RINLINE",
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
    t.value = "\\title{"
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
    t.value = "}\n\\maketitle"
    t.lexer.pop_state()
    return t

def t_BOLD(t):
    r'\[b\ '
    t.value = "\\textbf{"
    t.lexer.push_state('bold')
    return t
    
def t_bold_END(t):
    r'\s*\]'
    t.value = "}"
    t.lexer.pop_state()
    return t

def t_ITALIC(t):
    r'\[i\ '
    t.value = "\\textit{"
    t.lexer.push_state('italic')
    return t

def t_italic_END(t):
    r'\s*\]'
    t.value = "}"
    t.lexer.pop_state()
    return t

def t_UNDERLINE(t):
    r'\[u\ '
    t.value = "\\underline{"
    t.lexer.push_state('underline')
    return t
    
def t_underline_END(t):
    r'\s*\]'
    t.value = "}"
    t.lexer.pop_state()
    return t
    
def t_CINLINE(t):
    r'\[c\ '
    t.value = "\\texttt{"
    t.lexer.push_state('codeinline')
    return t
    
def t_codeinline_END(t):
    r'\s*\]'
    t.value = "}"
    t.lexer.pop_state()
    return t

def t_SUBSCRIPT(t):
    r'\[sub\ '
    t.value = "$_{"
    t.lexer.push_state('subscript')
    return t
    
def t_subscript_END(t):
    r'\s*\]'
    t.value = "}$"
    t.lexer.pop_state()
    return t
    
def t_SUPERSCRIPT(t):
    r'\[sup\ '
    t.value = "$^{"
    t.lexer.push_state('superscript')
    return t
    
def t_superscript_END(t):
    r'\s*\]'
    t.value = "}$"
    t.lexer.pop_state()
    return t

def t_STRIKEOUT(t):
    r'\[stk\ '
    t.value = "\\cancel{"
    t.lexer.push_state('strikeout')
    return t

def t_strikeout_END(t):
    r'\s*\]'
    t.value = "}"
    t.lexer.pop_state()
    return t

def t_SPECIAL(t):
    r'\[sp\s*'
    t.lexer.push_state('special')
    
def t_special_WORD(t):
    r'[a-zA-Z]+'
    t.value = f"\\text{t.value}\\space"
    return t

def t_HREF(t):
    r'\[href\ [^ ]+\ ?'
    t.value = f"\\href{{{t.value[6:-1]}}}{{"
    t.lexer.push_state('href')
    return t

def t_href_END(t):
    r'\]\n?'
    t.value = "}\n"
    t.lexer.pop_state()
    return t

def t_href_NAME(t):
    r'\[name\ '
    t.lexer.push_state('linktitle')
    
def t_IMAGE(t):
    r'\[img\s+[^ ]+\ ?'
    tmp = t.value[5:-1]
    t.value = "\\begin{figure}[h]\n\\centering\n\\includegraphics[width=\\textwidth]\n"
    t.value += f"{{{tmp.strip()}}}\n"
    t.lexer.push_state('image')
    return t

def t_image_END(t):
    r'\]'
    t.value = "\\end{figure}\n"
    t.lexer.pop_state()
    return t

def t_image_NAME(t):
    r'\[name\ '
    t.value = "\\label{fig:"
    t.lexer.push_state('imagetitle')
    return t

def t_imagetitle_END(t):
    r'\]'
    t.value = "\}\n"
    t.lexer.pop_state()
    return t

def t_CODE(t):
    r'\[code\ ?(\w*)\n'
    lang = t.value[6:-1]
    if(lang):
        t.value = f"\\begin{{minted}}{{{lang}}}\n"
        lexer.with_lang = True
    else:
        t.value = "\\begin{verbatim}\n"
    t.lexer.push_state('code')
    return t
    
def t_code_END(t):
    r'\s*code\]\n?'
    if(lexer.with_lang):
        t.value = "\\end{minted}\n"
        lexer.with_lang = False
    else:
        t.value = "\\end{verbatim}"
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
    t.value = "\n\\"
    for x in range(1, t.lexer.header_num):
        t.value += "sub"
    t.value += "section{"

    t.lexer.push_state('section')
    t.lexer.push_state('sectiontitle')
    return t

def t_sectiontitle_END(t):
    r'\n\s*'
    t.value = "}\n"
    t.lexer.pop_state()
    return t
    
def t_section_END(t):
    r'\s*sec\]\n?'
    t.lexer.pop_state()
    t.lexer.header_num -= 1

def t_COMMENT(t):
    r'%%.*\n?'

def t_TABLE(t):
    r'\[table\ '
    t.value = "\n\\begin{tabular}"
    t.lexer.push_state('table')
    return t

def t_table_TABLENCOLS(t):
    r'\d+\n'
    t.lexer.ncols = int(t.value[:-1])
    t.value = "{"
    for x in range(t.lexer.ncols):
        t.value += "c "
    t.value += "}\n"
    return t
    
def t_table_END(t):
    r'\s*table\]'
    t.value = "\\end{tabular}\n"
    t.lexer.pop_state()
    return t
    
def t_table_ROW(t):
    r'\s*\[row\ '
    t.value = "\t"
    t.lexer.push_state('row')
    return t
    
def t_row_END(t):
    r'\s*\]'
    t.value = "\n"
    t.lexer.currentcol = 1
    t.lexer.pop_state()
    return t
    
def t_row_TABLEHEADER(t):
    r'\s*\[h\ '
    t.value = "\\textbf{"
    t.lexer.push_state('tableheader')
    return t
    
def t_tableheader_END(t):
    r'\s*\]'
    t.value = "}"
    if (t.lexer.currentcol == t.lexer.ncols):
        t.value += " \\\ "
    else:
        t.value += " & "
    t.lexer.currentcol += 1
    t.lexer.pop_state()
    return t

def t_row_TABLEELEMENT(t):
    r'\s*\[e\ '
    t.lexer.push_state('tableelement')
    
def t_tableelement_END(t):
    r'\s*\]'
    if (t.lexer.currentcol == t.lexer.ncols):
        t.value = " \\\ "
    else:
        t.value = " & "
    t.lexer.currentcol += 1
    t.lexer.pop_state()
    return t
    
def t_LIST(t):
    r'\[list\n'
    t.value = "\\begin{itemize}\n"
    t.lexer.push_state('list')
    return t

def t_list_END(t): 
    r'\s*list\]'
    t.value = "\\end{itemize}\n"
    t.lexer.pop_state()
    return t

def t_DSCLIST(t):
    r'\s*\[dsclist'
    t.value = "\\begin{description}"
    t.lexer.push_state("dsclist")
    return t

def t_dsclist_OBJECT(t):
    r'\s*\[obj\ '
    t.value = "\n\\item["
    t.lexer.push_state("dlobject")
    return t 

def t_dlobject_END(t):
    r'\s*\]'
    t.value = "] "
    t.lexer.pop_state()
    return t 

def t_dsclist_DESCRIPTION(t):
    r'\s*\[dsc\ '
    t.value = "\\\\\n"
    t.lexer.push_state("dldescription")
    return t

def t_dldescription_END(t):
    r'\s*\]'
    t.lexer.pop_state()

def t_dsclist_END(t):
    r'\s*dsclist]'
    t.value = "\n\\end{description}\n"
    t.lexer.pop_state()
    return t

def t_ORDLIST(t):
    r'\[ordlist\ ?'
    t.lexer.push_state("ordlist")
    t.lexer.push_state("enumtype")

def t_enumtype_ENUMTYPE(t):
    r'[a-zA-Z]{0,1}.*\n'
    match = re.match(r'[a-zA-Z]', t.value[0])
    if match:
        t.value = "\\begin{enumerate}[label=(\\alph*)]\n"
    else:
        t.value = "\\begin{enumerate}\n"
    t.lexer.pop_state()
    return t
    
def t_ordlist_list_ITEM(t):
    r'\s*\[item\ '
    t.value = "\\item "
    t.lexer.push_state('item')
    return t

def t_item_END(t):
    r'\s*\]'
    t.value = "\n"
    t.lexer.pop_state()
    return t
    
def t_ordlist_END(t):
    r'\s*ordlist\]'
    t.value = "\\end{enumerate}\n"
    t.lexer.pop_state()
    return t

def t_special_linktitle_width_height_END(t):
    r'\s*\]'
    t.lexer.pop_state()
    
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

def t_NEWLINE(t):
    r'\n{2,}'
    t.value = "\\\\\n"
    return t

def t_SPACE(t):
    r'\s+'
    t.value = ' '
    return t

def t_WORD(t):
    r'[^[\]\s]+'
    return t

def t_ANY_error(t):
    r'.*|\n'
    print(f"Illegal character: {t.value}")

args = sys.argv
sys.tracebacklimit = 0 # hides traceback

if(args[1] == "-help"):
    print("""
        yaPP allows you to convert an .ya file with the defined syntax to an .html file.
        
        Usage: [input_file] [output_file]
        - The input file should have the .ya extension.
        - The output file should have the .html extension.
        
        To check the "yet another PreProccessor" syntax, please check our manual.
    """)
    exit() # better way to do this???

if(len(args) != 3):
    raise Exception("Wrong number of arguments. Use \"-help\" for more information.")

input_name = args[1]

if(input_name[-2:] != 'ya'):
    raise Exception("Unknown file extension. Use \"-help\" for more information.")

f = open(args[1], "r")
file_content = f.read()
f.close()

output_name = args[2]
if(output_name[-3:] != 'tex'):
    raise Exception("Unknown file extension. Use \"-help\" for more information.")

lexer = lex.lex()
lexer.header_num = 0
lexer.code_ident = None
lexer.correctly_finished = True
lexer.with_lang = False
lexer.input(file_content)
tmp_str = ""
lexer.ncols = 0
lexer.currentcol = 1

for tok in lexer:
    tmp_str += tok.value
    
if(lexer.correctly_finished):
    out_str = '''
\\documentclass{article}
\\usepackage[utf8]{inputenc}
\\usepackage[margin=1.1in]{geometry}
\\usepackage{graphicx}
\\usepackage{tikz}
\\usepackage{caption}
\\usepackage{textgreek}
\\usepackage{minted}
\\usepackage{enumitem}
\\usepackage{hyperref}
\\begin{document}
'''
    output = open(output_name, "w")
    output.write(out_str + tmp_str)
    output.write("\\end{document}")
    output.close()
else:
    print("Syntax error")

