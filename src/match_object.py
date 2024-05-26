from datetime import datetime

from pydantic import BaseModel

class MatchObject(BaseModel):
    '''
    A dataclass to store information about a single match on a single betting site.
    
    Params:
        site (str): betting site url
        home_name (str): name of the home team
        away_name (str): name of the away team
        home_odds (float): odds of home team winning
        tie_odds (float): odds of a tie
        away_odds (float): odds of away team winning
        date (datetime): year, month and day that the match will be played on
    '''
    site: str
    home_name: str
    away_name: str
    home_odds: float
    tie_odds: float
    away_odds: float
    date: datetime
    
    def __init__(self, *args):
        '''
        Define the __init__ function for the purpose of initializing objects from a list e.g. MatchObject(*input_list).
        '''
        field_names = self.__fields__.keys()
        kwargs = dict(zip(field_names, args))
        
        super().__init__(**kwargs)