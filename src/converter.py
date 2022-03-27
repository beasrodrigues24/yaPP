from abc import (ABC, abstractmethod)


class Converter(ABC):

    @abstractmethod
    def file_begin(title: str) -> str:
        pass

    @abstractmethod
    def file_end() -> str:
        pass

    @abstractmethod
    def section_begin() -> str:
        pass

    @abstractmethod
    def section_end() -> str:
        pass

    @abstractmethod
    def section_title_end(n: int) -> str:
        pass

    @abstractmethod
    def bold_begin() -> str:
        pass

    @abstractmethod
    def bold_end() -> str:
        pass

    @abstractmethod
    def italic_begin() -> str:
        pass

    @abstractmethod
    def italic_end() -> str:
        pass

    @abstractmethod
    def underline_begin() -> str:
        pass

    @abstractmethod
    def underline_end() -> str:
        pass

    @abstractmethod
    def code_inline_begin() -> str:
        pass

    @abstractmethod
    def code_inline_end() -> str:
        pass

    @abstractmethod
    def subscript_begin() -> str:
        pass

    @abstractmethod
    def subscript_end() -> str:
        pass

    @abstractmethod
    def superscript_begin() -> str:
        pass

    @abstractmethod
    def superscript_end() -> str:
        pass

    @abstractmethod
    def strikeout_begin() -> str:
        pass

    @abstractmethod
    def strikeout_end() -> str:
        pass

    @abstractmethod
    def special(spc: str) -> str:
        pass

    @abstractmethod
    def href_begin(link: str) -> str:
        pass

    @abstractmethod
    def href_end() -> str:
        pass

    @abstractmethod
    def image_begin(src: str) -> str:
        pass

    @abstractmethod
    def image_end() -> str:
        pass

    @abstractmethod
    def image_name_begin() -> str:
        pass

    @abstractmethod
    def image_name_end() -> str:
        pass

    @abstractmethod
    def image_height(height: str) -> str:
        pass

    @abstractmethod
    def image_width(width: str) -> str:
        pass

    @abstractmethod
    def code_block_begin(lang: str) -> str:
        pass

    @abstractmethod
    def code_block_end() -> str:
        pass

    @abstractmethod
    def table_begin(n: int) -> str:
        pass

    @abstractmethod
    def table_end() -> str:
        pass

    @abstractmethod
    def btable_begin(n: int) -> str:
        pass

    @abstractmethod
    def btable_end() -> str:
        pass

    @abstractmethod
    def table_row_begin() -> str:
        pass

    @abstractmethod
    def table_row_end() -> str:
        pass

    @abstractmethod
    def table_row_header_begin() -> str:
        pass

    @abstractmethod
    def table_row_header_end(table_curr_column: int, table_num_columns: int) -> str:
        pass

    @abstractmethod
    def table_row_element_begin() -> str:
        pass

    @abstractmethod
    def table_row_element_end(table_curr_column: int, table_num_columns: int) -> str:
        pass

    @abstractmethod
    def list_begin() -> str:
        pass

    @abstractmethod
    def list_end() -> str:
        pass

    @abstractmethod
    def ordered_list_begin(type: str) -> str:
        pass

    @abstractmethod
    def ordered_list_end() -> str:
        pass

    @abstractmethod
    def list_item_begin() -> str:
        pass

    @abstractmethod
    def list_item_end() -> str:
        pass

    @abstractmethod
    def description_list_begin() -> str:
        pass

    @abstractmethod
    def description_list_end() -> str:
        pass

    @abstractmethod
    def description_list_item_begin() -> str:
        pass

    @abstractmethod
    def description_list_item_end() -> str:
        pass

    @abstractmethod
    def description_list_item_description_begin() -> str:
        pass

    @abstractmethod
    def description_list_item_description_end() -> str:
        pass

    @abstractmethod
    def raw(lang: str, line: str) -> str:
        pass

    @abstractmethod
    def newline() -> str:
        pass

    @abstractmethod
    def word(word: str) -> str:
        pass
