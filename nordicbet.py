from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By

from betting_site_scraper import BettingSiteScraper

class NordicBet(BettingSiteScraper):
    
    url_base_path = "https://www.nordicbet.com/en/sportsbook/"
    
    def __init__(self, league: str, sport: str, country: str) -> None:
        super().__init__(league, sport, country)
        self.url = f'{self.url_base_path}{self.sport}/{self.league}/{self.league}'
        
    def get_odds(self):
        self.driver.get(url=self.url)
        WebDriverWait(driver=self.driver, timeout=15).until(
            EC.presence_of_element_located((By.CLASS_NAME, "mat-typography"))
        )
        
        elements = self.driver.find_elements(By.ID, 'ng-star-inserted')
        print(elements)