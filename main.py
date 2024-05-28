from src.betting_sites.unibet import Unibet
from src.betting_sites.veikkaus import Veikkaus

if __name__ == "__main__":
    vk = Veikkaus()
    vk.get_odds()
    
    ub = Unibet()
    ub.get_odds()

    for i, r in ub.odds_df.iterrows():
        print(r['Match date'], r['Home'], r['Away'], r['Home odds'], r['Draw odds'], r['Away odds'])
        
    for i, r in vk.odds_df.iterrows():
        print(r['Match date'], r['Home'], r['Away'], r['Home odds'], r['Draw odds'], r['Away odds'])
