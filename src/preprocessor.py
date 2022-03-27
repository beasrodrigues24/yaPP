import ply.lex as lex
from converter import Converter
import io


class Preprocessor:

    def __init__(self, converter: Converter, input: str):
        self.lexer = lex.lex(module=self, debug=False)
        self.lexer.input(input)
        self.c: Converter = converter

        self.title_text: str = None
        self.header_num: int = 0
        self.code_ident: int = None
        self.raw_lang: str = None
        self.table_num_columns: int = 0
        self.table_curr_column: int = 1
        self.correctly_finished: bool = True
        self.processed_file: str = ""

    def process(self):
        for tok in self.lexer:
            self.processed_file += tok.value

        if not self.correctly_finished:
            raise SystemExit('error: unbalanced brackets at the end of file.')

    def write(self, out: io.TextIOWrapper):
        out.write(self.c.file_begin(self.title_text))
        out.write(self.processed_file)
        out.write(self.c.file_end())


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
              "BTABLE",
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
              "ORDLIST",
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
        ('btable', 'exclusive'),
        ('row', 'exclusive'),
        ('tableheader', 'inclusive'),
        ('tableelement', 'inclusive'),
        ('image', 'inclusive'),
        ('list', 'exclusive'),
        ('item', 'inclusive'),
        ('ordlist', 'exclusive'),
        ('dsclist', 'exclusive'),
        ('dlobject', 'inclusive'),
        ('dldescription', 'inclusive'),
        ('width', 'exclusive'),
        ('height', 'exclusive'),
        ('special', 'exclusive'),
        ('raw', 'exclusive'),
    ]

    def t_TITLE(self, t):
        r'\[t\s+[^\]]+\s*\]\s*'
        self.title_text = t.value[2:].strip()[:-1].rstrip()

    def t_SECTION(self, t):
        r'\[sec\s+'
        self.header_num += 1
        t.value = self.c.section_begin(self.header_num)
        t.lexer.push_state('section')
        t.lexer.push_state('sectiontitle')
        return t

    def t_sectiontitle_END(self, t):
        r'\n\s*'
        t.value = self.c.section_title_end(self.header_num)
        t.lexer.pop_state()
        return t

    def t_section_END(self, t):
        r'\s*sec\]\n?'
        t.value = self.c.section_end()
        t.lexer.pop_state()
        self.header_num -= 1
        return t

    def t_BOLD(self, t):
        r'\[b\s+'
        t.value = self.c.bold_begin()
        t.lexer.push_state('bold')
        return t

    def t_bold_END(self, t):
        r'\s*\]'
        t.value = self.c.bold_end()
        t.lexer.pop_state()
        return t

    def t_ITALIC(self, t):
        r'\[i\s+'
        t.value = self.c.italic_begin()
        t.lexer.push_state('italic')
        return t

    def t_italic_END(self, t):
        r'\s*\]'
        t.value = self.c.italic_end()
        t.lexer.pop_state()
        return t

    def t_UNDERLINE(self, t):
        r'\[u\s+'
        t.value = self.c.underline_begin()
        t.lexer.push_state('underline')
        return t

    def t_underline_END(self, t):
        r'\s*\]'
        t.value = self.c.underline_end()
        t.lexer.pop_state()
        return t

    def t_CINLINE(self, t):
        r'\[c\s+'
        t.value = self.c.code_inline_begin()
        t.lexer.push_state('codeinline')
        return t

    def t_codeinline_END(self, t):
        r'\s*\]'
        t.value = self.c.code_inline_end()
        t.lexer.pop_state()
        return t

    def t_SUBSCRIPT(self, t):
        r'\[sub\s+'
        t.value = self.c.subscript_begin()
        t.lexer.push_state('subscript')
        return t

    def t_subscript_END(self, t):
        r'\s*\]'
        t.value = self.c.subscript_end()
        t.lexer.pop_state()
        return t

    def t_SUPERSCRIPT(self, t):
        r'\[sup\s+'
        t.value = self.c.superscript_begin()
        t.lexer.push_state('superscript')
        return t

    def t_superscript_END(self, t):
        r'\s*\]'
        t.value = self.c.superscript_end()
        t.lexer.pop_state()
        return t

    def t_STRIKEOUT(self, t):
        r'\[stk\s+'
        t.value = self.c.strikeout_begin()
        t.lexer.push_state('strikeout')
        return t

    def t_strikeout_END(self, t):
        r'\s*\]'
        t.value = self.c.strikeout_end()
        t.lexer.pop_state()
        return t

    def t_SPECIAL(self, t):
        r'\[sp\s+'
        t.lexer.push_state('special')

    def t_special_WORD(self, t):
        r'[a-zA-Z]+'
        t.value = self.c.special(t.value)
        return t

    def t_HREF(self, t):
        r'\[href\s+[^ ]+\s*'
        t.value = self.c.href_begin(t.value[6:].strip())
        t.lexer.push_state('href')
        return t

    def t_href_END(self, t):
        r'\]\n?'
        t.value = self.c.href_end()
        t.lexer.pop_state()
        return t

    def t_href_NAME(self, t):
        r'\[name\s+'
        t.lexer.push_state('linktitle')

    def t_IMAGE(self, t):
        r'\[img\s+[^ ]+\s*'
        t.value = self.c.image_begin(t.value[5:].strip())
        t.lexer.push_state('image')
        return t

    def t_image_END(self, t):
        r'\]'
        t.value = self.c.image_end()
        t.lexer.pop_state()
        return t

    def t_image_NAME(self, t):
        r'\[name\s+'
        t.value = self.c.image_name_begin()
        t.lexer.push_state('imagetitle')
        return t

    def t_imagetitle_END(self, t):
        r'\]'
        t.value = self.c.image_name_end()
        t.lexer.pop_state()
        return t

    def t_image_WIDTH(self, t):
        r'\s*\[w\s+'
        t.lexer.push_state("width")

    def t_width_WORD(self, t):
        r'\d+(\.\d+)?'
        t.value = self.c.image_width(t.value)
        return t

    def t_image_HEIGHT(self, t):
        r'\s*\[h\s+'
        t.lexer.push_state("height")

    def t_height_WORD(self, t):
        r'\d+(\.\d+)?'
        t.value = self.c.image_height(t.value)
        return t

    def t_CODE(self, t):
        r'\[code\s+(\w*)\n'
        t.value = self.c.code_block_begin(t.value[6:].strip())
        t.lexer.push_state('code')
        return t

    def t_code_END(self, t):
        r'\s*code\]\n?'
        t.value = self.c.code_block_end()
        self.code_ident = None
        t.lexer.pop_state()
        return t

    def t_code_LINE(self, t):
        r'.+\n'
        if self.code_ident == None:
            self.code_ident = len(t.value) - len(t.value.lstrip())
        t.value = t.value[self.code_ident:]
        return t

    def t_TABLE(self, t):
        r'\[table[^\n\S]+\d+\n'
        self.table_num_columns = int(t.value[7:])
        t.value = self.c.table_begin(self.table_num_columns)
        t.lexer.push_state('table')
        return t

    def t_table_END(self, t):
        r'\s*table\]'
        t.value = self.c.table_end()
        t.lexer.pop_state()
        return t

    def t_BTABLE(self, t):
        r'\[btable[^\n\S]+\d+\n'
        self.table_num_columns = int(t.value[8:])
        t.value = self.c.btable_begin(self.table_num_columns)
        t.lexer.push_state('btable')
        return t

    def t_btable_END(self, t):
        r'\s*btable\]'
        t.value = self.c.btable_end()
        t.lexer.pop_state()
        return t

    def t_table_btable_ROW(self, t):
        r'\s*\[row\s+'
        t.value = self.c.table_row_begin()
        t.lexer.push_state('row')
        return t

    def t_row_END(self, t):
        r'\s*\]'
        t.value = self.c.table_row_end()
        self.table_curr_column = 1
        t.lexer.pop_state()
        return t

    def t_row_TABLEHEADER(self, t):
        r'\s*\[h\s+'
        t.value = self.c.table_row_header_begin()
        t.lexer.push_state('tableheader')
        return t

    def t_tableheader_END(self, t):
        r'\s*\]'
        t.value = self.c.table_row_header_end(self.table_curr_column, self.table_num_columns)
        self.table_curr_column += 1
        t.lexer.pop_state()
        return t

    def t_row_TABLEELEMENT(self, t):
        r'\s*\[e\s+'
        t.value = self.c.table_row_element_begin()
        t.lexer.push_state('tableelement')
        return t

    def t_tableelement_END(self, t):
        r'\s*\]'
        t.value = self.c.table_row_element_end(self.table_curr_column, self.table_num_columns)
        self.table_curr_column += 1
        t.lexer.pop_state()
        return t

    def t_LIST(self, t):
        r'\[list\n'
        t.value = self.c.list_begin()
        t.lexer.push_state('list')
        return t

    def t_list_END(self, t):
        r'\s*list\]'
        t.value = self.c.list_end()
        t.lexer.pop_state()
        return t

    def t_DSCLIST(self, t):
        r'\s*\[dsclist\n'
        t.value = self.c.description_list_begin()
        t.lexer.push_state("dsclist")
        return t

    def t_dsclist_END(self, t):
        r'\s*dsclist]'
        t.value = self.c.description_list_end()
        t.lexer.pop_state()
        return t

    def t_dsclist_OBJECT(self, t):
        r'\s*\[obj\ '
        t.value = self.c.description_list_item_begin()
        t.lexer.push_state("dlobject")
        return t

    def t_dlobject_END(self, t):
        r'\s*\]'
        t.value = self.c.description_list_item_end()
        t.lexer.pop_state()
        return t

    def t_dsclist_DESCRIPTION(self, t):
        r'\s*\[dsc\ '
        t.value = self.c.description_list_item_description_begin()
        t.lexer.push_state("dldescription")
        return t

    def t_dldescription_END(self, t):
        r'\s*\]'
        t.value = self.c.description_list_item_description_end()
        t.lexer.pop_state()
        return t

    def t_ORDLIST(self, t):
        r'\[ordlist[^\n\S]+[a-zA-Z]{0,1}.*\n'
        t.value = self.c.ordered_list_begin(t.value[8:].strip()[0])
        t.lexer.push_state("ordlist")
        return t

    def t_ordlist_list_ITEM(self, t):
        r'\s*\[item\s+'
        t.value = self.c.list_item_begin()
        t.lexer.push_state('item')
        return t

    def t_item_END(self, t):
        r'\s*\]'
        t.value = self.c.list_item_end()
        t.lexer.pop_state()
        return t

    def t_ordlist_END(self, t):
        r'\s*ordlist\]'
        t.value = self.c.ordered_list_end()
        t.lexer.pop_state()
        return t

    def t_RAW(self, t):
        r'\[raw[^\n\S]+\w+\n'
        self.raw_lang = t.value[5:-1].strip()
        t.lexer.push_state('raw')

    def t_raw_END(self, t):
        r'\s*raw\]\n?'
        self.code_ident = None
        t.lexer.pop_state()

    def t_raw_LINE(self, t):
        r'.+\n'
        if self.code_ident == None:
            self.code_ident = len(t.value) - len(t.value.lstrip())
        t.value = self.c.raw(self.raw_lang, t.value[self.code_ident:])
        return t

    def t_special_linktitle_width_height_END(self, t):
        r'\s*\]'
        t.lexer.pop_state()

    def t_ANY_COMMENT(self, t):
        r'//.*\n?'

    def t_NEWLINE(self, t):
        r'\n{2,}'
        t.value = self.c.newline()
        return t

    def t_SPACE(self, t):
        r'\s+'
        t.value = ' '
        return t

    def t_ESCAPEDWORD(self, t):
        r'\\.'
        if t.value[1] == '\\':
            t.value = '\\'
        else:
            t.value = t.value.replace("\\", "")

        t.value = self.c.word(t.value)
        return t

    def t_WORD(self, t):
        r'[^[\]\s\\]+'
        t.value = self.c.word(t.value)
        return t

    def t_ANY_error(self, t):
        r'.*|\n'
        print(f"Illegal character: {t.value} at {t.lexpos}:{t.lineno}")

    def t_ANY_eof(self, t):
        if(len(t.lexer.lexstatestack) != 0):
            self.correctly_finished = False
        else:
            self.correctly_finished = True
