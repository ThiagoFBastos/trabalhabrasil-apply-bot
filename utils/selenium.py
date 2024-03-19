from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
import selenium.webdriver.support.expected_conditions as EC
import logging

def get_by_xpath(driver, xpath, wait_time):
    return WebDriverWait(driver, wait_time).until(EC.presence_of_element_located((By.XPATH, xpath)))
    
def get_by_xpath_to_click(driver, xpath, wait_time):
    return WebDriverWait(driver, wait_time).until(EC.element_to_be_clickable((By.XPATH, xpath)))
