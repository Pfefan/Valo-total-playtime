"""Main module"""
from threading import Thread
from datetime import datetime
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.firefox.service import Service
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait


class Webscraper():
    """Main class to Webscrape tracker.gg"""
    def __init__(self) -> None:
        self.url = "https://tracker.gg/valorant/profile/riot/"
        self.data = []
        self.options = Options()
        self.options.add_argument('--headless')
        self.options.binary_location = r"C:\Program Files\Mozilla Firefox\firefox.exe"
        self.browser = ""

    def main(self):
        """main class to start threads"""
        while True:
            self.commandhandler(input(">: "))

    def getdata(self, user):
        """gets data from a player"""
        url = self.url + user + "/performance"
        self.browser.get(url)

        try:
            myElem = WebDriverWait(self.browser, 1).until(EC.presence_of_element_located((By.ID, 'IdOfMyElement')))
        except TimeoutException:
            pass
        html = self.browser.page_source.encode("utf-8")
        soup = BeautifulSoup(html, features="html.parser")
        mydivs = soup.find_all("div", class_="value")
        
        if len(mydivs) > 0:
            value = mydivs[0]
            value = value.get_text(separator=" ").strip()
        

            self.data.append(value)
        else:
            print(f"failed to get playtime of {url} user: {user}")

    def commandhandler(self, read):
        """handel command inputs"""
        if len(read.split(" ", maxsplit=1)) > 1:
            cmd, attributes = read.split(" ", maxsplit=1)
            if cmd == "add-user":
                with open("namelist.txt", "a+", encoding="utf8") as wfile:
                    wfile.write(self.nameconvert(attributes) + "\n")
        else:
            if read == "get-total":
                start = datetime.now()
                totaltime = 0
                self.browser = webdriver.Firefox(options=self.options, service=Service("geckodriver.exe"))

                with open("namelist.txt", "r", encoding="utf-8") as rfile:
                    for user in rfile.readlines():
                        Thread(target=self.getdata(user)).start()
                delta = datetime.now() - start
                for value in self.data:
                    totaltime += float(value.split(" ")[0])
                self.browser.quit()
                print(f"Total playtime: {totaltime} hrs, lookuptime: {str(delta)}")
        self.data.clear()
    

    def nameconvert(self, name):
        """converts normal string name into name which can be used on tracker.gg"""
        outletter = ""
        for _, value in enumerate(name):
            if value == " ":
                outletter += "%20"
            elif value == "#":
                outletter += "%23"
            else:
                outletter += value
        return outletter

     
if __name__ == "__main__":
    Webscraper().main()