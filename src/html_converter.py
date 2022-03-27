from functools import reduce
from converter import Converter


class HtmlConverter(Converter):

    escape_chars = {
        '"': '&quot;',
        '\'': '&#39;',
        '&': '&amp;',
        '<': '&lt;',
        '>': '&gt;'
    }

    def file_begin(title: str) -> str:
        tmp = ""
        if title != None:
            tmp = f'<title>{title}</title>\n'

        return f'''<!DOCTYPE html>
<html>
<head>
<link rel="stylesheet"
href="https://cdnjs.cloudflare.com/ajax/libs/highlight.js/11.5.0/styles/default.min.css">
<script src="https://cdnjs.cloudflare.com/ajax/libs/highlight.js/11.5.0/highlight.min.js"></script>
<script>hljs.highlightAll();</script>
{tmp}</head>
<body>
'''

    def file_end() -> str:
        return '</body>\n</html>\n'

    def section_begin(n: int) -> str:
        return f'<div>\n<h{n}>'

    def section_end() -> str:
        return f'</div>\n'

    def section_title_end(n: int) -> str:
        return f'</h{n}>\n'

    def bold_begin() -> str:
        return '<b>'

    def bold_end() -> str:
        return '</b>'

    def italic_begin() -> str:
        return '<i>'

    def italic_end() -> str:
        return '</i>'

    def underline_begin() -> str:
        return '<c>'

    def underline_end() -> str:
        return '</c>'

    def code_inline_begin() -> str:
        return '<code>'

    def code_inline_end() -> str:
        return '</code>'

    def subscript_begin() -> str:
        return '<sub>'

    def subscript_end() -> str:
        return '</sub>'

    def superscript_begin() -> str:
        return '<sup>'

    def superscript_end() -> str:
        return '</sup>'

    def strikeout_begin() -> str:
        return '<del>'

    def strikeout_end() -> str:
        return '</del>'

    def special(spc: str) -> str:
        return f'&{spc};'

    def href_begin(link: str) -> str:
        return f'<a href=\"{link}\">'

    def href_end() -> str:
        return '</a>'

    def image_begin(src: str) -> str:
        return f'<img src="{src}"'

    def image_end() -> str:
        return '>'

    def image_name_begin() -> str:
        return ' alt="'

    def image_name_end() -> str:
        return '"'

    def image_height(height: str) -> str:
        return f' height={height}'

    def image_width(width: str) -> str:
        return f' width={width}'

    def code_block_begin(lang: str) -> str:
        if lang:
            return f'<pre><code class="language-{lang}">\n'
        else:
            return '<pre><code>\n'

    def code_block_end() -> str:
        return '</code></pre>\n'

    def table_begin(n: int) -> str:
        return '<table>\n'

    def table_end() -> str:
        return '</table>\n'

    def btable_begin(n: int) -> str:
        return '<table border="1" style="border-collapse:collapse">\n'

    def btable_end() -> str:
        return '</table>\n'

    def table_row_begin() -> str:
        return '<tr>\n'

    def table_row_end() -> str:
        return '</tr>\n'

    def table_row_header_begin() -> str:
        return '<th>\n'

    def table_row_header_end(table_curr_column: int, table_num_columns: int) -> str:
        return '</th>\n'

    def table_row_element_begin() -> str:
        return '<td>\n'

    def table_row_element_end(table_curr_column: int, table_num_columns: int) -> str:
        return '</td>\n'

    def list_begin() -> str:
        return '<ul>\n'

    def list_end() -> str:
        return '</ul>\n'

    def ordered_list_begin(type: str) -> str:
        if type != '\n':
            return f'<ol type={type}>\n'
        else:
            return '<ol>\n'

    def ordered_list_end() -> str:
        return '</ol>\n'

    def list_item_begin() -> str:
        return '<li>\n'

    def list_item_end() -> str:
        return '</li>\n'

    def description_list_begin() -> str:
        return '<dl>\n'

    def description_list_end() -> str:
        return '</dl>\n'

    def description_list_item_begin() -> str:
        return '<dt>\n'

    def description_list_item_end() -> str:
        return '</dt>\n'

    def description_list_item_description_begin() -> str:
        return '<dd>\n'

    def description_list_item_description_end() -> str:
        return '</dd>\n'

    def raw(lang: str, line: str) -> str:
        if lang == 'html':
            return line
        return ''

    def newline() -> str:
        return '<br>\n'

    def word(word: str) -> str:
        return reduce(
            lambda x, y: x + y,
            map(lambda c: HtmlConverter.escape_chars[c] if c in HtmlConverter.escape_chars else c, word)
        )
