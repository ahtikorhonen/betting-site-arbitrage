from datetime import datetime, timedelta

from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
import pytz
import pandas as pd

from src.betting_sites.betting_site_scraper import BettingSiteScraper
from src.utils import read_json
from src.constants import FIN_UTC_DIFF

class Veikkaus(BettingSiteScraper):
        
    def __init__(self) -> None:
        super().__init__()
        self.data = read_json("data/veikkaus_data.json")
        self.leagues = self.data["leagues"]
        self.elements = self.data["elements"]
        
    def get_odds(self) -> None:
        '''
        Scrape the odds of all games from the leagues specified in the unibet_data.json file,
        and add them to the objects odds_df dataframe.
        '''
        
        for idx, (league_name, data) in enumerate(self.leagues.items()):
            url = data["url"]
            self._driver.get(url=url)
            
            if idx == 0: self.click(self.elements['accept_cookies'])
            for match_data_row in self._wait.until(EC.presence_of_all_elements_located((By.CLASS_NAME, self.elements["match_data_row"]))):
                single_match_data = match_data_row.text.split('\n')[:-2]
                
                # if match is ongoing skip.
                if single_match_data[0].isdigit():
                    continue
                
                match_date, match_details = self.handle_match_data(single_match_data)
                
                # some data is missing, skip.
                if len(match_details) != 5:
                    continue
                single_match_data_df = pd.DataFrame(columns=self.odds_df.columns.values.tolist(), data=[[league_name, url, match_date, *match_details]])
                self.odds_df = pd.concat([self.odds_df, single_match_data_df])
                    
    def handle_match_data(self, match_details: list[str]) -> pd.DataFrame:
        '''
        A helper function that parses single rows of match information into a form that is suitable for our dataframe.
        
        Params:
            match_data (List[str]): list containing all the information of a single match from Veikkaus.
        Returns:
            single row of pandas dataframe containing [home_team_name, away_team_name, home_odds, draw_odds, away_odds]
        '''
        if match_details[0].replace(".", "", 1).isdigit():
            match_details.insert(0, None)
            
        date = self.get_date(match_details[0], match_details[1])

        # remove league name from match details.
        match_details.pop(4)
        match_details = match_details[2:]
        # if draw is not possible add None to draw_odds index.
        if len(match_details) == 4:
            match_details.insert(-1, None)

        return date, match_details

    def get_date(self, day_abbr: str, time_str: str) -> datetime:
        '''
        Converts Finnish day abbreviation + finnish local time to utc time for games after today.
        
        Params:
            day_abbr (str): weekday abbreviation in Finnish
            time_str (str): finnish local time
        Returns:
            datetime object
        '''
        hour, minute = time_str.split('.')
        finland_tz = pytz.timezone('Europe/Helsinki')
        now = datetime.now(finland_tz)
        
        # if day_abbr is None match is played today
        if day_abbr is  None:
            return datetime(now.year, now.month, now.day, int(hour), int(minute)) - timedelta(hours=FIN_UTC_DIFF)
        
        finnish_days = {
            'ma': 0,
            'ti': 1,
            'ke': 2,
            'to': 3,
            'pe': 4,
            'la': 5,
            'su': 6
        }
        
        target_weekday = finnish_days[day_abbr.lower()]
        days_ahead = target_weekday - now.weekday()
        if days_ahead <= 0:
            days_ahead += 7
        next_day = now + timedelta(days=days_ahead)
        
        next_day_at_time = datetime(
            year=next_day.year,
            month=next_day.month,
            day=next_day.day,
            hour=int(hour),
            minute=int(minute),
            tzinfo=finland_tz
        )
        
        gmt_time = next_day_at_time.astimezone(pytz.utc)
            
        return datetime(gmt_time.year, gmt_time.month, gmt_time.day)
