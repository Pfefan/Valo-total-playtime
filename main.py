from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException

class Webscraper():
    def __init__(self) -> None:
        self.url = "https://tracker.gg/valorant/profile/riot/GBC%20Pfefan%23PEPE/performance"
        self.options = Options()
        self.options.add_argument('--headless')
        self.options.binary_location = r"C:\Program Files\Mozilla Firefox\firefox.exe"
    
    def getdata(self):
        browser = webdriver.Firefox(options=self.options, executable_path='geckodriver.exe')
        browser.get(self.url)
        
        try:
            myElem = WebDriverWait(browser, 1).until(EC.presence_of_element_located((By.ID, 'IdOfMyElement')))
        except TimeoutException:
            pass

        html = browser.page_source.encode("utf-8")
        soup = BeautifulSoup(html, features="html.parser")
        mydivs = soup.find_all("div", class_="value")
        value = mydivs[0]
        value = value.get_text(separator=" ").strip()
        browser.quit()

        return value.split(" ")
        
if __name__ == "__main__":
    print(Webscraper().getdata())