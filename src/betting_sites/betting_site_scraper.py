from abc import abstractmethod
from collections import defaultdict

from selenium import webdriver
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
import pandas as pd

class BettingSiteScraper:
    '''
    A base class for all betting sites that are used.
    
    Parameters:
        odds_df (pd.Dataframe): A dataframe which contains all the odds of specific bookmaker.
        _driver (WebDrived): Selenium chrome webdriver object.
        _wait (WebDriverWait): Selenium webdriverwait object.
    '''
    def __init__(self) -> None:
        self.odds = defaultdict()
        self.odds_df = pd.DataFrame(columns=['League', 'URL', 'Match date', 'Home', 'Away', 'Home odds', 'Draw odds', 'Away odds'])
        self._driver = webdriver.Chrome("/Users/ahtikorhonen/Desktop/bet-arb/chromedriver")
        self._wait = WebDriverWait(self._driver, 30)
        
    @abstractmethod
    def get_odds():
        '''
        Abstract method that all subclasses need to implement. Fills the odds dictionary.
        '''
        pass
    
    def click(self, xpath):
        try:
            self._wait.until(EC.element_to_be_clickable((By.XPATH, xpath))).click()
        except Exception as e:
            raise Exception(str(e))
        