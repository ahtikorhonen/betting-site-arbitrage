from enum import Enum, auto

from src.unibet import Unibet

class Leagues(Enum):
    EPL = auto()
    NHL = auto()

if __name__ == "__main__":
    ub = Unibet()
    ub.get_odds()
    
    for k,v in ub.odds.items():
        print(k,'\n',v.keys(),'\n')
        for k2, v2 in v.items():
            print(v2)
