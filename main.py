from src.betting_sites.unibet import Unibet
from src.betting_sites.veikkaus import Veikkaus

if __name__ == "__main__":
    '''ub = Unibet()
    ub.get_odds()'''
    vk = Veikkaus()
    vk.get_odds()
    for index, row in vk.odds_df.iterrows():
        print(row.League, row.Home, row.Away)
