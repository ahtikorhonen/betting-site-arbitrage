from datetime import datetime

from pydantic import BaseModel

class MatchObject(BaseModel):
    '''
    A dataclass to store information about a single match on a single betting site.
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