from selenium import webdriver
from selenium.webdriver.firefox.service import Service as FirefoxService
from webdriver_manager.firefox import GeckoDriverManager
from selenium.webdriver.firefox.options import Options as FirefoxOptions
from time import sleep
import scraper
from utils.selenium import get_by_xpath, get_by_xpath_to_click
import logging

class TrabalhaBrasil:

    def __init__(self, cpf, data_nascimento):
        self._BASE_URL = 'https://www.trabalhabrasil.com.br'
        self._LOGIN_URL = f'{self._BASE_URL}/Login?tipoPerfil=Candidato'
        self._SEARCH_URL = f'{self._BASE_URL}/vagas-empregos' + '{}{}/{}'

        self._cpf = cpf
        self._data_nascimento = data_nascimento

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

    def login(self):
        CPF_XPATH = "//*[@id = 'txtLoginCPF']"
        DATA_NASCIMENTO_XPATH = "//*[@id = 'txtLoginNascimento']"
        NOME_XPATH = "//*[@id = 'txtLoginName']"

        while True:
            try:
                if self._driver.current_url != self._LOGIN_URL:
                    self._driver.get(self._LOGIN_URL)

                cpf = get_by_xpath(self._driver, CPF_XPATH, 5)                
                cpf.send_keys(self._cpf)

                data_nascimento = get_by_xpath(self._driver, DATA_NASCIMENTO_XPATH, 5)
                data_nascimento.send_keys(self._data_nascimento)

                nome = get_by_xpath_to_click(self._driver, NOME_XPATH, 5)
                nome.click()

                sleep(5)
                break
            except Exception as ex:
                logging.error(f'error when trying to login: {ex}')

    def quit(self):
        self._driver.quit()

    def countSearchPages(self, keywords, location = None):
        try:
            self.search(keywords, 1, location)
            page_source = self._driver.page_source
            return scraper.get_last_page_from_page_source(page_source)
        except Exception as ex:
            logging.error(f'error when search for jobs: {ex}')

    def search(self, keywords, page, location = None):
        try:
            url = self._SEARCH_URL.format('', '', keywords) if location is None else self._SEARCH_URL.format('-em-', location.replace(' ', '-'), keywords)
            url += f'?pagina={page}' 

            self._driver.get(url)

            page_source = self._driver.page_source
            links = scraper.get_jobs_links_from_page_source(page_source)
            links = list(map(lambda href: f'{self._BASE_URL}{href}', links))

            return links
        except Exception as ex:
            logging.error(f'error when search for jobs: {ex}')

        return []

    def apply(self, url):
        try:
            print(f'trying aplly for {url}')

            BOX_ACTION_XPATH = "//div[@class = 'boxAction']"
            APPLY_BUTTON_XPATH = "./button"

            self._driver.get(url)

            boxAction = get_by_xpath(self._driver, BOX_ACTION_XPATH, 5)
            button = get_by_xpath_to_click(boxAction, APPLY_BUTTON_XPATH, 5)

            if button is not None:
                buttonClass = button.get_attribute('class')
                if 'disabled' not in buttonClass:
                    button.click()
                    return True
                else:
                    return False
        except Exception as ex:
            logging.error(f'error when apply for job: {ex}')
