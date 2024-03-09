from requests import Response


class WorkWithFiles:
    def save_to_html(self, response: Response, filename: str) -> None:
        with open(f'{filename}.html', 'w', encoding='utf-8') as file:
            file.write(response.text)

    def read_from_html(self, filename: str = 'quotes') -> str:
        with open(f'{filename}.html', 'r') as file:
            html: str = file.read()

        return html
