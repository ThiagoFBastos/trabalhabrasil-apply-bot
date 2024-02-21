from bs4 import BeautifulSoup
import logging
from time import sleep

def get_jobs_links_from_page_source(page_source):
    try:
        soup = BeautifulSoup(page_source, 'html.parser')
        nav = soup.find('nav', attrs = {'id': 'jobs-wrapper'})
        aCollection = nav.find_all('a')
        links = [a['href'] for a in aCollection]
        return links
    except Exception as ex:
        logging.error(f'error when extract links of jobs: {ex}')
    return []

def get_last_page_from_page_source(page_source):
    try:
        soup = BeautifulSoup(page_source, 'html.parser')
        a = soup.find('a', attrs = {'title': 'Última página'})
        onclick = a['onclick']
        return int(onclick.replace(')', '(').split('(')[-2])
    except Exception as ex:
        logging.error(f'error when extract last page of search page: {ex}')
    return 0
