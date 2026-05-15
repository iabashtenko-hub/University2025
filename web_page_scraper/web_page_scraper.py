import requests
from bs4 import BeautifulSoup
import string
from pathlib import Path
from requests.exceptions import RequestException


class NatureScraper:
    def __init__(self, max_pages, target_category):
        self.pages_to_crawl = max_pages
        self.category_filter = target_category
        self.endpoint_url = "https://www.nature.com/nature/articles"
        self.web_client = requests.Session()
        # Установка заголовков для имитации браузера
        self.web_client.headers.update({
            "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36",
            "Accept-Language": "en-US,en;q=0.5"
        })

    def _sanitize_filename(self, article_title):
        """Превращает заголовок статьи в валидное имя файла."""
        # Убираем пунктуацию и заменяем пробелы на подчеркивания
        char_strip_table = str.maketrans('', '', string.punctuation.replace('-', '').replace('_', ''))
        cleaned_name = article_title.translate(char_strip_table).replace(' ', '_')
        return f"{cleaned_name[:100]}.txt"

    def _send_request(self, target_url, query_params=None):
        """Обертка для выполнения сетевых запросов с обработкой ошибок."""
        try:
            network_response = self.web_client.get(target_url, params=query_params, timeout=20)
            network_response.raise_for_status()
            return network_response
        except RequestException as network_error:
            print(f"[!] Ошибка соединения с {target_url}: {network_error}")
            return None

    def _parse_article_content(self, article_url):
        """Извлекает текст статьи из найденных HTML-контейнеров."""
        page_data = self._send_request(article_url)
        if not page_data:
            return None

        html_dom = BeautifulSoup(page_data.text, "html.parser")

        # Поиск основного блока текста по известным паттернам Nature
        dom_selectors = [
            "article.c-article-body",
            "div.main-content",
            "div[itemprop='articleBody']"
        ]

        for css_selector in dom_selectors:
            content_node = html_dom.select_one(css_selector)
            if content_node:
                text_nodes = content_node.find_all("p")
                extracted_text = "\n".join(paragraph.get_text(strip=True) for paragraph in text_nodes)
                if extracted_text.strip():
                    return extracted_text

        # Если основной блок не найден, пробуем забрать анонс (teaser)
        teaser_node = html_dom.find("p", class_="article__teaser")
        return teaser_node.get_text(strip=True) if teaser_node else ""

    def _process_single_page(self, current_page_index):
        """Обрабатывает одну страницу списка статей."""
        print(f"[*] Сканирование страницы {current_page_index}...")

        request_payload = {
            "searchType": "journalSearch",
            "sort": "PubDate",
            "year": "2022",  # Можно заменить на актуальный год
            "page": current_page_index
        }

        server_reply = self._send_request(self.endpoint_url, params=request_payload)
        if not server_reply:
            return

        parsed_list_page = BeautifulSoup(server_reply.text, "html.parser")

        # Создаем папку для текущей страницы
        output_directory = Path(f"Page_{current_page_index}")
        output_directory.mkdir(exist_ok=True)

        found_articles = parsed_list_page.find_all("article")
        if not found_articles:
            print(f"[-] На странице {current_page_index} контент отсутствует.")
            return

        for item_node in found_articles:
            # Фильтрация по заданному типу (напр. Research Highlight)
            meta_type_tag = item_node.find("span", {"data-test": "article.type"})
            if not meta_type_tag or meta_type_tag.text.strip() != self.category_filter:
                continue

            link_anchor = item_node.find("a", {"data-track-action": "view article"})
            if not link_anchor:
                continue

            headline = link_anchor.text.strip()
            direct_url = "https://www.nature.com" + link_anchor.get("href")

            print(f"    + Обработка: {headline[:60]}...")

            body_content = self._parse_article_content(direct_url)
            if body_content:
                generated_filename = self._sanitize_filename(headline)
                target_file_path = output_directory / generated_filename
                try:
                    target_file_path.write_text(body_content, encoding="utf-8")
                except IOError as file_io_error:
                    print(f"[!] Не удалось записать файл {generated_filename}: {file_io_error}")

    def run(self):
        """Запуск цикла обхода всех страниц."""
        for page_step in range(1, self.pages_to_crawl + 1):
            self._process_single_page(page_step)
        print("\n[+] Работа завершена. Проверьте созданные директории.")


def main():
    while True:
        try:
            requested_pages = int(input("Сколько страниц нужно просмотреть?\n> "))
            if requested_pages > 0:
                break
        except ValueError:
            pass
        print("Введите корректное число.")

    chosen_category = input("Какую категорию ищем? (напр., Research Highlight):\n> ").strip()

    scraper_instance = NatureScraper(requested_pages, chosen_category)
    scraper_instance.run()


if __name__ == "__main__":
    main()