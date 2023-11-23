import json
import re
import requests
from aiogram.types import Document

from config.config import config

class Book:
    def __init__(self, file:Document, page_size=800):
        # self.title = path.split('/')[-1].split('.')[0]
        # self.path = os.path.join(sys.path[0], os.path.normpath(path))
        self.title = self._get_pretty_name(file.file_name)
        self.file_id = file.file_id
        self.__page_size = page_size

        self.book: dict[int, str] = {}

        self._prepare_book()


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
        text = self._get_file_text_from_server()
        current = 0
        page_num = 1
        while current < len(text)-1:
            page, size = self._get_part_text(text, current, self.__page_size)
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