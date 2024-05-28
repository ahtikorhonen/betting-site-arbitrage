from datetime import datetime
import re

from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
import pytz
import pandas as pd

from src.betting_sites.betting_site_scraper import BettingSiteScraper
from src.utils import read_json

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
            dates = []
            
            for idx, e in enumerate(self._wait.until(EC.presence_of_all_elements_located((By.CLASS_NAME, self.elements["tournament_container"])))):
                for t in e.find_elements(By.XPATH, self.elements["date_element"]):
                        datetime_str = t.get_attribute('datetime')
                        date = self.transform_to_datetime(datetime_str)
                        dates.append(date)

                for match in e.find_elements(By.CSS_SELECTOR, self.elements["nested_match_element"]):
                    match_details = match.text.split('\n')[:6]
                    match_date = dates[idx]
                    match_details = self.handle_match_data(match_details)
                    # skip matches that are ongoing or are missing data
                    if match_details is None:
                        continue
                    single_match_data_df = pd.DataFrame(columns=self.odds_df.columns.values.tolist(), data=[[league_name, url, match_date, *match_details]])
                    self.odds_df = pd.concat([self.odds_df, single_match_data_df])
                    
    def handle_match_data(self, match_details: list[str]) -> list:
        '''
        TODO: add description
        '''
        time_re = re.compile(r'^(([01]\d|2[0-3]):([0-5]\d)|24:00)$')
        is_time_format = bool(time_re.match(match_details[0]))
        # If match is ongoing or data is missing return None
        if not is_time_format or len(match_details) < 6:
            return None
        
        if not match_details[-1][0].isnumeric():
            match_details.pop(-1)
            match_details.insert(-1, None)
                    
        return match_details[1:]
        
                        
    def transform_to_datetime(self, datetime_str: str) -> datetime:
        '''
        Converts the datetime string from unibet to datetime object in utc format.
        
        Params:
             datetime_str (str): string to be converted to datetime object.
        returns: datetime object 
        ''' 
        cleaned_str = re.sub(r'\s+\([^)]*\)', '', datetime_str)
    
        local_time = datetime.strptime(cleaned_str, '%a %b %d %Y %H:%M:%S GMT%z')
        
        utc_time = local_time.astimezone(pytz.utc)
                
        return utc_time
