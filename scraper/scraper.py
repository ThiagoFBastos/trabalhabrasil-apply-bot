from bs4 import BeautifulSoup
import logging

def get_jobs_links_from_page_source(page_source):
    try:
        soup = BeautifulSoup(page_source, 'html.parser')
        jg__jobs = soup.find_all('div', attrs = {'class': 'jg__job'})
        links = [jg__job.find('a')['href'] for jg__job in jg__jobs]
        return links
    except Exception as ex:
        logging.error(f'error when extract links of jobs: {ex}')

def get_last_page_from_page_source(page_source):
    try:
        soup = BeautifulSoup(page_source, 'html.parser')
        ul = soup.find('ul', attrs = {'class': 'newPagination__controls'})
        li = ul.find_all('li', attrs = {'class': 'newPagination__item newPagination__item--icon'})[-1]
        onclick = li['onclick']
        return int(onclick.replace(')', '(').split('(')[-2])
    except Exception as ex:
        logging.error(f'error when extract last page of search page: {ex}')
