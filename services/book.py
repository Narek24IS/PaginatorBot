import json
import re
import requests
from aiogram.types import Document

from config.config import config


class Book:
    def __init__(self, file: Document | None = None, text:str | None = None, page_size=800):
        self.__page_size = page_size
        if file:
            self.title = self._get_pretty_name(file.file_name)
            self.file_id = file.file_id
            self.text = self._get_file_text_from_server()
        elif text:
            self.text = text
        else:
            raise ValueError

        self.book: dict[int, str] = {}

        self._prepare_book()

    @staticmethod
    def _get_part_text(text: str, start: int, size: int) -> tuple[str, int]:
        chars = '.,:;!?'
        end = min(start+ size, len(text))

        if end == len(text):
            page = text[start:end+1]
            return page, len(page)

        for current in range(end - 1, start, -1):
            if text[current] in chars and text[current+1] not in chars:
                break
        else:
            current = end

        page = text[start:current + 1]
        return page, len(page)

    def _get_pretty_name(self, name: str) -> str:
        name = name.replace('.txt', '')
        pretty = re.sub(r'\W', '_', name.lower())
        pretty = re.sub(r'_+', '_', pretty)
        return pretty[:35]

    def _get_file_text_from_server(self) -> str:
        file_info_url = f'https://api.telegram.org/bot{config.bot.token}/getFile?file_id={self.file_id}'
        response = requests.get(file_info_url)
        file_info = response.json()
        file_path = file_info["result"]["file_path"]
        file_url = f"https://api.telegram.org/file/bot{config.bot.token}/{file_path}"
        response = requests.get(file_url)
        return response.text

    def _prepare_book(self) -> None:
        while '\n\n' in self.text:
            self.text = self.text.replace('\n\n', '\n')
        current = 0
        page_num = 1
        while current < len(self.text) - 1:
            page, size = self._get_part_text(self.text, current, self.__page_size)
            self.book[page_num] = page.lstrip()
            current += size
            page_num += 1

    def __len__(self):
        return len(self.book)

    def __getitem__(self, key: int | str):
        if isinstance(key, str):
            if key.isdigit():
                key = int(key)
        return self.book[key]

    def __setitem__(self, key: int | str, value: str):
        if isinstance(key, str):
            if key.isdigit():
                key = int(key)
        self.book[key] = value

    def __delitem__(self, key):
        del self.book[key]

    def __iter__(self):
        return iter(self.book.values())

    def get_json_text(self) -> str:
        return json.dumps(self.book, indent=1)

# bok = Book('../books/book.txt')
# print([page for page in bok])
#
# import json
#
# with open(r'scripts/storage/Bredberi_Marsianskie_hroniki.json', encoding='utf-8') as f:
#     content = json.load(f)
#     content_str = json.dumps(content)
#
# query = 'INSERT INTO books (name, content) VALUES (%s, %s)'
# values = ('📖 Ray Bradbury `The Martian Chronicles`', content_str)
