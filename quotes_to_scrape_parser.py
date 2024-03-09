import requests
import json
from parsel import Selector, SelectorList
from requests import Response

from utils import WorkWithFiles


class QuotesToScrapeParser(WorkWithFiles):
    def __init__(self, url: str, filename: str = 'quotes') -> None:
        self.url = url
        self.headers = self.get_headers()
        self.response = self.make_request()
        self.save_to_html(response=self.response, filename=filename)

    def get_headers(self) -> dict:
        return {
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36',
        }

    def make_request(self) -> Response:
        return requests.get(url=self.url, headers=self.headers)

    def parse(self) -> list[dict]:
        data: list[dict] = []

        while True:
            selector: Selector = Selector(text=self.response.text)
            quotes: SelectorList = selector.css('.quote')
            for quote in quotes:
                text: str = quote.css('.text::text').get().strip()[1:-1]
                author: str = quote.css('[itemprop="author"]::text').get().strip()
                link: str = self.url + quote.css('span a::attr(href)').get()[1:]
                tags: list[dict] = [
                    {
                        'name': tag.css('::text').get().strip(),
                        'link': self.url + tag.css('::attr(href)').get()[1:]
                    }
                    for tag in quote.css('.tags .tag')
                ]

                data.append({
                    'text': text,
                    'author': author,
                    'link': link,
                    'tags': tags
                })

            next_button: str = selector.css('.pager .next a::attr(href)').get()
            if next_button:
                url: str = self.url + next_button
                self.response = requests.get(url=url, headers=self.headers)
            else:
                break

        return data

    def print(self, data: list[dict]) -> None:
        print(json.dumps(data, indent=2, ensure_ascii=False))