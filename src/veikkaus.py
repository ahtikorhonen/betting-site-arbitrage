from collections import defaultdict
from datetime import datetime, timedelta

from selenium.webdriver.common.by import By
import pytz

from src.betting_site_scraper import BettingSiteScraper
from src.utils import read_json
from src.match_object import MatchObject
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
        and add them to the objects odds dictionary.
        '''
        
        for league_name, data in self.leagues.items():
            url = data["url"]
            self._driver.get(url=url)
            date_match_dict = defaultdict()
            
            self.click(self.elements['accept_cookies'])
            for match_data_row in self._driver.find_elements(By.CLASS_NAME, self.elements["match_data_row"]):
                single_match_data = match_data_row.text.split('\n')[:-2]
                match_date, match_details = self.handle_match_data(single_match_data)
                match_obj = MatchObject(url, *match_details, match_date)
                date_match_dict[match_date] = match_obj
            
            self.odds[league_name] = date_match_dict
        
        print(self.odds)
            
    def handle_match_data(self, match_data):
        '''
        A helper function that parses single rows of match information into a form that is suitable for MatchObject creation.
        
        Params:
            match_data (List[str]): list containing all the information of a single match from Veikkaus.
        Returns:
            tuple of matchdate as a datetime object and list of match info of the form [home_team_name, away_team_name,
                home_odds, tie_odds, away_odds]
        '''
        
        # odds have commas instead of periods that need to be replaced.
        match_details = [value.replace(",", ".") for value in match_data]
        if match_details[0].replace(".", "", 1).isdigit():
            date = self.get_today_date(match_details[0])
            # remove league name from match details.
            match_details.pop(3)
            match_details = match_details[1:]
            
            return date, match_details
        
        else:
            date = self.get_future_date(match_details[0], match_details[1])
            # remove league name from match details.
            match_details.pop(4)
            match_details = match_details[2:]
            
            return date, match_details
    
    def get_today_date(self, time: str) -> datetime:
        '''
        Converts hours to datetime object in utc format
        
        Params:
            time (str): string of the form hour.minute. Values are between 00.00 - 24.00
        Returns:
            datetime object
        '''
        hour, minute = time.split('.')
        today = datetime.now()
        utc_datetime_obj = datetime(today.year, today.month, today.day, int(hour), int(minute)) - timedelta(hours=FIN_UTC_DIFF)
        
        return utc_datetime_obj

    def get_future_date(self, day_abbr: str, time_str: str) -> datetime:
        '''
        Converts Finnish day abbreviation + finnish local time to utc time
        
        Params:
            day_abbr (str): weekday abbreviation in Finnish
            time_str (str): finnish local time
        Returns:
            datetime object
        '''
        finnish_days = {
            'ma': 0,
            'ti': 1,
            'ke': 2,
            'to': 3,
            'pe': 4,
            'la': 5,
            'su': 6
        }
        finland_tz = pytz.timezone('Europe/Helsinki')
        now = datetime.now(finland_tz)
        
        # Find the next occurrence of the given weekday
        target_weekday = finnish_days[day_abbr.lower()]
        days_ahead = target_weekday - now.weekday()
        if days_ahead <= 0:
            days_ahead += 7
        next_day = now + timedelta(days=days_ahead)
        
        # Parse the provided time string
        time_parts = time_str.split('.')
        hour = int(time_parts[0])
        minute = int(time_parts[1])
        
        # Combine the next day with the provided time
        next_day_at_time = datetime(
            year=next_day.year,
            month=next_day.month,
            day=next_day.day,
            hour=hour,
            minute=minute,
            second=0,
            microsecond=0,
            tzinfo=finland_tz
        )
        
        # Convert to UTC
        gmt_time = next_day_at_time.astimezone(pytz.utc)
            
        return datetime(gmt_time.year, gmt_time.month, gmt_time.day)
