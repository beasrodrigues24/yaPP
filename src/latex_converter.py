import re
from functools import reduce
from converter import Converter


class LatexConverter(Converter):

    escape_chars = {
        '&': '\\&',
        '%': '\\%',
        '$': '\\$',
        '#': '\\#',
        '_': '\\_',
        '{': '\\{',
        '}': '\\}',
        '~': '\\textasciitilde',
        '^': '\\textasciicircum',
        '\\': '\\textbackslash'
    }

    def file_begin(title: str) -> str:
        tmp = ""
        if title != None:
            tmp = '\\title{' + title + '}\n\\maketitle\n'

        return '''\\documentclass{article}
\\usepackage[utf8]{inputenc}
\\usepackage[margin=1.1in]{geometry}
\\usepackage{graphicx}
\\usepackage{tikz}
\\usepackage{caption}
\\usepackage{textgreek}
\\usepackage{minted}
\\usepackage{enumitem}
\\usepackage{hyperref}
\\usepackage{ulem}
\\begin{document}
''' + tmp

    def file_end() -> str:
        return '\\end{document}'

    def section_begin(n: int) -> str:
        tmp = '\\'
        for x in range(1, n):
            tmp += 'sub'
        tmp += 'section{'

        return tmp

    def section_end() -> str:
        return ''

    def section_title_end(n: int) -> str:
        return '}\n'

    def bold_begin() -> str:
        return '\\textbf{'

    def bold_end() -> str:
        return '}'

    def italic_begin() -> str:
        return '\\textit{'

    def italic_end() -> str:
        return '}'

    def underline_begin() -> str:
        return '\\underline{'

    def underline_end() -> str:
        return '}'

    def code_inline_begin() -> str:
        return '\\texttt{'

    def code_inline_end() -> str:
        return '}'

    def subscript_begin() -> str:
        return '$_{'

    def subscript_end() -> str:
        return '}$'

    def superscript_begin() -> str:
        return '$^{'

    def superscript_end() -> str:
        return '}$'

    def strikeout_begin() -> str:
        return '\\sout{'

    def strikeout_end() -> str:
        return '}'

    def special(spc: str) -> str:
        return f'\\text{spc}\\space'

    def href_begin(link: str) -> str:
        return '\\href{' + link + '}{'

    def href_end() -> str:
        return '}'

    def image_begin(src: str) -> str:
        return f'''
\\begin{{figure}}[!ht]
\\centering
\\includegraphics[width=\\textwidth]{{{src}}}
'''

    def image_end() -> str:
        return '\\end{figure}\n'

    def image_name_begin() -> str:
        return '\\caption{'

    def image_name_end() -> str:
        return '}\n'

    def image_height(height: str) -> str:
        return ''

    def image_width(width: str) -> str:
        return ''

    def code_block_begin(lang: str) -> str:
        if lang:
            return '\\begin{minted}{' + lang + '}\n'
        else:
            return '\\begin{minted}{text}\n'

    def code_block_end() -> str:
        return '\\end{minted}\n'

    def table_begin(n: int) -> str:
        tmp = '\\begin{tabular}{'
        for x in range(n - 1):
            tmp += 'c '
        tmp += 'c}\n'

        return tmp

    def table_end() -> str:
        return '\\end{tabular}\n'

    def btable_begin(n: int) -> str:
        return LatexConverter.table_begin(n)

    def btable_end() -> str:
        return LatexConverter.table_end()

    def table_row_begin() -> str:
        return '\t'

    def table_row_end() -> str:
        return '\n'

    def table_row_header_begin() -> str:
        return '\\textbf{'

    def table_row_header_end(table_curr_column: int, table_num_columns: int) -> str:
        if (table_curr_column == table_num_columns):
            return "} \\\ "
        else:
            return "} & "

    def table_row_element_begin() -> str:
        return ''

    def table_row_element_end(table_curr_column: int, table_num_columns: int) -> str:
        if (table_curr_column == table_num_columns):
            return " \\\ "
        else:
            return " & "

    def list_begin() -> str:
        return '\n\\begin{itemize}\n'

    def list_end() -> str:
        return '\\end{itemize}\n'

    def ordered_list_begin(type: str) -> str:
        match = re.match(r'[a-zA-Z]', type)
        if match:
            return "\n\\begin{enumerate}[label=(\\alph*)]\n"
        else:
            return "\n\\begin{enumerate}\n"

    def ordered_list_end() -> str:
        return '\\end{enumerate}\n'

    def list_item_begin() -> str:
        return '\\item '

    def list_item_end() -> str:
        return '\n'

    def description_list_begin() -> str:
        return '\n\\begin{description}'

    def description_list_end() -> str:
        return '\n\\end{description}\n'

    def description_list_item_begin() -> str:
        return '\n\\item['

    def description_list_item_end() -> str:
        return ']'

    def description_list_item_description_begin() -> str:
        return '\\\\\n'

    def description_list_item_description_end() -> str:
        return ''

    def raw(lang: str, line: str) -> str:
        if lang == 'latex':
            return line
        return ''

    def newline() -> str:
        return '\\\\\n'

    def word(word: str) -> str:
        return reduce(
            lambda x, y: x + y,
            map(lambda c: LatexConverter.escape_chars[c] if c in LatexConverter.escape_chars else c, word)
        )
