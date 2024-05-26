from collections import defaultdict
from datetime import datetime
import re

from selenium.webdriver.common.by import By
import pytz

from src.betting_sites.betting_site_scraper import BettingSiteScraper
from src.utils import read_json
from src.match_object import MatchObject

class Unibet(BettingSiteScraper):
        
    def __init__(self) -> None:
        super().__init__()
        self.data = read_json("data/unibet_data.json")
        self.leagues = self.data["leagues"]
        self.elements = self.data["elements"]
        
    def get_odds(self) -> None:
        '''
        Scrape the odds of all games from the leagues specified in the unibet_data.json file,
        and add them to the objects odds dictionary.
        '''
        for league_name, data in self.leagues.items():
            url = data["url"]
            self._driver.get(url=url)
            date_match_dict = defaultdict()
            dates = []
            
            for idx, e in enumerate(self._driver.find_elements(By.CLASS_NAME, self.elements["match_container"])):
                if idx == 0:
                    for t in e.find_elements(By.XPATH, self.elements["date_element"]):
                        datetime_str = t.get_attribute('datetime')
                        date = self.transform_to_datetime(datetime_str)
                        dates.append(date)
                
                for match in e.find_elements(By.CSS_SELECTOR, self.elements["match_element"]):
                    match_info = match.text.split('\n')[1:6]
                    date = dates[idx]
                    match_obj = MatchObject(url, *match_info, date)
                    date_match_dict[date] = match_obj
                        
            self.odds[league_name] = date_match_dict
            
        self._driver.close()
            
    def transform_to_datetime(self, datetime_str: str) -> datetime:
        '''
        Converts the datetime string from unibet to datetime object in GMT+00 format.
        
        Params:
             datetime_str (str): string to be converted to datetime object.
        returns: datetime object 
        '''
        cleaned_str = re.sub(r'\s+\([^)]*\)', '', datetime_str)
    
        local_time = datetime.strptime(cleaned_str, '%a %b %d %Y %H:%M:%S GMT%z')
        
        utc_time = local_time.astimezone(pytz.utc)
        
        return datetime(utc_time.year, utc_time.month, utc_time.day)
