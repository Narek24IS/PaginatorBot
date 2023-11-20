import os
import sys

class Book:
    def __init__(self, path, page_size=1050):
        self.path = os.path.join(sys.path[0], os.path.normpath(path))
        self.page_size = page_size

        self.book: dict[int, str] = {}

        self._prepare_book(path)

    @staticmethod
    def _get_part_text(text: str, start: int, size: int) -> tuple[str, int]:
        end = min(start+size, len(text))
        current:int
        if end == len(text):
            page = text[start:end]
            return page, len(page)

        for current in range(end-1, start, -1):
            if text[current] in '.,:;!?':
                if text[current + 1] != '.':
                    a = text[current]
                    break
        else:
            current = end

        page = text[start:current+1]
        return page, len(page)


    def _prepare_book(self, path: str) -> None:
        with open(path, 'r', encoding='utf-8') as f:
            text = f.read()
            current = 0
            page_num = 1
            while current < len(text)-1:
                page, size = self._get_part_text(text, current, PAGE_SIZE)
                self.book[page_num] = page.lstrip()
                current += size
                page_num += 1

    def __len__(self):
        return len(self.book)

    def __getitem__(self, key:int|str):
        if isinstance(key, str):
            if key.isdigit():
                key = int(key)
        return self.book[key]

    def __setitem__(self, key:int|str, value:str):
        if isinstance(key, str):
            if key.isdigit():
                key = int(key)
        self.book[key] = value

    def __delitem__(self, key):
        del self.book[key]

    def __iter__(self):
        return iter(self.book.values())


# bok = Book('../books/book.txt')
# print([page for page in bok])