from src import scraper
from src import logging_manager as log


def main():
    try:
        scraper.get_links()
        scraper.get_product_info()
        scraper.save_info()
    except Exception as e:
        print(e)
        log.o_info(e)


if __name__ == '__main__':
    main()

