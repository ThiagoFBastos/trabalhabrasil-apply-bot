from bs4 import BeautifulSoup
from utils.selenium import get_by_xpath, get_by_xpath_to_click
from fake_useragent import UserAgent
import requests
import re

class TrabalhaBrasilScraper:

    def __init__(self, driver):
        self._driver = driver

    def get_jobs_links_from_page_source(self, url):
        ua = UserAgent()
        page_source = requests.get(url, headers = {'User-Agent': ua.firefox}).text
        soup = BeautifulSoup(page_source, 'html.parser')
        nav = soup.find('nav', attrs = {'id': 'jobs-wrapper'})
        if nav is None:
            raise RuntimeError('Tag não encontrada no método get_jobs_links_from_page_source')
        aCollection = nav.find_all('a')
        links = [a['href'] for a in aCollection if 'href' in a.attrs]
        return links
        
    def get_last_page_from_page_source(self, url):
        ua = UserAgent()
        page_source = requests.get(url, headers = {'User-Agent': ua.firefox}).text
        soup = BeautifulSoup(page_source, 'html.parser')
        a = soup.find('a', attrs = {'title': 'Última página'})
        if a is None:
            raise RuntimeError('Tag não encontrada no método get_last_page_from_page_source')
        elif 'onclick' not in a.attrs:
            if 'class' in a.attrs and a['class'] == ['pagination__link', 'disabled']:
                return 1
            raise RuntimeError('Tag não possui atributo em get_last_page_from_page_source')
        onclick = a['onclick']
        if not re.match(r'^[a-zA-z_]+\(\d+\)$', onclick):
            raise RuntimeError('Atributo com formato incorreto no método get_last_page_from_page_source')
        return int(re.search(r'\d+', onclick).group(0))

    def get_login_cpf_input(self):
        CPF_XPATH = "//*[@id = 'txtLoginCPF']"
        try:
            return get_by_xpath(self._driver, CPF_XPATH, 5)
        except:
            raise RuntimeError('Tag não encontrada no método get_login_cpf_input')

    def get_login_birthday_input(self):
        BIRTHDAY_XPATH = "//*[@id = 'txtLoginNascimento']"
        try:
            return get_by_xpath(self._driver, BIRTHDAY_XPATH, 5)
        except:
            raise RuntimeError('Tag não encontrada no método get_login_birthday_input')

    def get_login_name_input(self):
        NAME_XPATH = "//*[@id = 'txtLoginName']"
        try:
            return get_by_xpath(self._driver, NAME_XPATH, 5)
        except:
            raise RuntimeError('Tag não encontrada no método get_login_name_input')

    def get_apply_button(self):
        BOX_ACTION_XPATH = "//div[@class = 'boxAction']"
        APPLY_BUTTON_XPATH = "./button"
        try:
            box_action = get_by_xpath(self._driver, BOX_ACTION_XPATH, 5)
            return get_by_xpath_to_click(box_action, APPLY_BUTTON_XPATH, 5)
        except:
            raise RuntimeError('Tag não encontrada no método get_apply_button')
    
