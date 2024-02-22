from selenium import webdriver
from selenium.webdriver.firefox.service import Service as FirefoxService
from webdriver_manager.firefox import GeckoDriverManager
from selenium.webdriver.firefox.options import Options as FirefoxOptions
from time import sleep
from scraper import TrabalhaBrasilScraper
import logging
import os
import os.path
import pickle

class TrabalhaBrasilBOT:

    def __init__(self, cpf, data_nascimento):
        self._BASE_URL = 'https://www.trabalhabrasil.com.br'
        self._LOGIN_URL = f'{self._BASE_URL}/Login?tipoPerfil=Candidato'
        self._SEARCH_URL = f'{self._BASE_URL}/vagas-empregos' + '{}{}/{}'

        self._cpf = cpf
        self._data_nascimento = data_nascimento

        self._is_logged = False

        self.removeCookies()

        self.restart()

    def removeCookies(self):
        cookie_filename = f'cookies/{self._cpf}.pkl'

        if not os.path.isdir('cookies'):
            os.mkdir('cookies')

        if os.path.isfile(cookie_filename):
            os.remove(cookie_filename)

    @property
    def is_logged(self):
        return self._is_logged

    def restart(self):
        if self.is_logged:
            self.quit()

        options = FirefoxOptions()
        options.add_argument("--start-maximized")
        options.add_argument("--disable-infobars")
        options.add_argument("--disable-extensions")
        options.add_argument('--no-sandbox')
        options.add_argument('--disable-application-cache')
        options.add_argument('--disable-gpu')
        options.add_argument("--disable-dev-shm-usage")
        options.add_argument("--headless")

        self._driver = webdriver.Firefox(service = FirefoxService(GeckoDriverManager().install()), options = options)
    
        self._scraper = TrabalhaBrasilScraper(self._driver)

        self.login()

    def login(self):
        cookie_filename = f'cookies/{self._cpf}.pkl'

        if os.path.isfile(cookie_filename):
            self._driver.get(self._BASE_URL)
            with open(cookie_filename, 'rb') as f:
                cookies = pickle.load(f)
                for cookie in cookies:
                    self._driver.add_cookie(cookie)
        else:
            while True:
                try:
                    if self._driver.current_url != self._LOGIN_URL:
                        self._driver.get(self._LOGIN_URL)

                    cpf = self._scraper.get_login_cpf_input()
                    cpf.send_keys(self._cpf)

                    birthday = self._scraper.get_login_birthday_input()
                    birthday.send_keys(self._data_nascimento)

                    name = self._scraper.get_login_name_input()
                    name.click()

                    sleep(5)

                    break
                except Exception as ex:
                    logging.error(f'error when trying to login: {ex}')

            cookies = self._driver.get_cookies()

            with open(cookie_filename, 'wb') as f:
                pickle.dump(cookies, f)

        self._is_logged = True

    def quit(self):
        self._driver.quit()
        self._is_logged = False

    def countSearchPages(self, keywords, location = None):
        try:
            self.search(keywords, 1, location)
            return self._scraper.get_last_page_from_page_source()
        except Exception as ex:
            logging.error(f'error when search for jobs: {ex}')

    def search(self, keywords, page, location = None):
        try:
            print(f'searching on page {page}')

            url = self._SEARCH_URL.format('', '', keywords) if location is None else self._SEARCH_URL.format('-em-', location.replace(' ', '-'), keywords)
            url += f'?pagina={page}'

            self._driver.get(url)

            links = self._scraper.get_jobs_links_from_page_source()
            links = list(map(lambda href: f'{self._BASE_URL}{href}', links))

            return links
        except Exception as ex:
            logging.error(f'error when search for jobs: {ex}')

        return []

    def apply(self, url):
        try:
            print(f'trying apply for {url}')

            self._driver.get(url)

            apply_button = self._scraper.get_apply_button()

            if apply_button is not None:
                button_class = apply_button.get_attribute('class')
                if 'disabled' not in button_class:
                    apply_button.click()
                    return True
        except Exception as ex:
            logging.error(f'error when apply for job: {ex}')

        return False
