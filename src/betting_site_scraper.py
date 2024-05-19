from abc import abstractmethod
from collections import defaultdict

from selenium import webdriver
from selenium.webdriver.support.wait import WebDriverWait

class BettingSiteScraper:
    '''
    A base class for all betting sites that are used.
    
    Parameters:
        odds (dict): a nested dictionary of the form {'league_name': {'date': [match_obj, ...]}}.
        _driver (WebDrived): Selenium chrome webdriver object.
        _wait (WebDriverWait): Selenium webdriverwait object.
    '''
    def __init__(self) -> None:
        self.odds = defaultdict()
        self._driver = webdriver.Chrome("/Users/ahtikorhonen/Desktop/bet-arb/chromedriver")
        self._wait = WebDriverWait(self._driver, 30)
        
    @abstractmethod
    def get_odds():
        '''
        Abstract method that all subclasses need to implement. Fills the odds dictionary.
        '''
        pass
        