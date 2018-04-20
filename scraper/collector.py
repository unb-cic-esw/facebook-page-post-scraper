import csv
from post_scraper import Scraper
from token_manager import retrieve_token


def collect_all_pages():
    pages = []
    with open('entidades.csv', 'r') as entidades:
        reader = csv.reader(entidades)
        for row in reader:
            pages.append(row[0])
    scraper = Scraper(retrieve_token())
    if scraper.check_valid_token():
        for page in pages:
            scraper.set_page(page)
            print(scraper.page)
            scraper.get_page_name_and_like()
            scraper.write_file()
            scraper.convert_to_csv()
    else:
        print('Please renew token')


if __name__ == '__main__':
    collect_all_pages()