from datetime import datetime
from typing import Optional

from pydantic import BaseModel, validator

class MatchObject(BaseModel):
    '''
    A dataclass to store information about a single match on a single betting site.
    
    Params:
        site (str): betting site url
        home_name (str): name of the home team
        away_name (str): name of the away team
        home_odds (float): odds of home team winning
        draw_odds (float | None): odds of a draw
        away_odds (float): odds of away team winning
        date (datetime): year, month and day that the match will be played on
    '''
    site: str
    home_name: str
    away_name: str
    home_odds: float
    draw_odds: Optional[float] = None
    away_odds: float
    date: datetime
    
    def __init__(self, *args):
        '''
        __init__ function overriden for the purpose of initializing objects without a dict.
        '''
        field_names = self.__fields__.keys()
        kwargs = dict(zip(field_names, args))
        
        super().__init__(**kwargs)
        
    @validator('home_odds', 'draw_odds', 'away_odds', pre=True, always=True)
    def replace_comma(cls, v):
        '''
        Replace commas in odds with periods to make float conversion possible.
        '''
        if v is not None:
            return v.replace(',', '.')
        return v