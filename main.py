from quotes_to_scrape_parser import QuotesToScrapeParser


def main() -> None:
    qtsp = QuotesToScrapeParser(url='https://quotes.toscrape.com')
    quotes_to_scrape_data: list[dict] = qtsp.parse()
    qtsp.print(quotes_to_scrape_data)


if __name__ == '__main__':
    main()
