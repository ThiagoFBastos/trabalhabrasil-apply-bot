from bs4 import BeautifulSoup
import logging
from utils.selenium import get_by_xpath, get_by_xpath_to_click

class TrabalhaBrasilScraper:

    def __init__(self, driver):
        self._driver = driver

    def get_jobs_links_from_page_source(self):
        try:
            page_source = self._driver.page_source
            soup = BeautifulSoup(page_source, 'html.parser')
            nav = soup.find('nav', attrs = {'id': 'jobs-wrapper'})
            aCollection = nav.find_all('a')
            links = [a['href'] for a in aCollection]
            return links
        except Exception as ex:
            logging.error(f'error when extract links of jobs: {ex}')
        return []

    def get_last_page_from_page_source(self):
        try:
            page_source = self._driver.page_source
            soup = BeautifulSoup(page_source, 'html.parser')
            a = soup.find('a', attrs = {'title': 'Última página'})
            onclick = a['onclick']
            return int(onclick.replace(')', '(').split('(')[-2])
        except Exception as ex:
            logging.error(f'error when extract last page of search page: {ex}')
        return 0

    def get_login_cpf_input(self):
        CPF_XPATH = "//*[@id = 'txtLoginCPF']"
        return get_by_xpath(self._driver, CPF_XPATH, 5)

    def get_login_birthday_input(self):
        BIRTHDAY_XPATH = "//*[@id = 'txtLoginNascimento']"
        return get_by_xpath(self._driver, BIRTHDAY_XPATH, 5)

    def get_login_name_input(self):
        NAME_XPATH = "//*[@id = 'txtLoginName']"
        return get_by_xpath(self._driver, NAME_XPATH, 5)

    def get_apply_button(self):
        BOX_ACTION_XPATH = "//div[@class = 'boxAction']"
        APPLY_BUTTON_XPATH = "./button"
        box_action = get_by_xpath(self._driver, BOX_ACTION_XPATH, 5)
        return get_by_xpath_to_click(box_action, APPLY_BUTTON_XPATH, 5)
    
