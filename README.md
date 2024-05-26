A bot that finds arbitrages between sports betting sites.

How the bot works:
    1. scrape odds from betting sites.
    2. compare odds between different sites to check for arbs.
    3. if arbs exist notify via telegram.

How arbitrage betting works:

total implied probability (TIP) = 1/home win odds + 1/draw odds + 1/away team odds

if TIP > 1, bookmaker has the edge.
if TIP < 1, arbitrage exists.

strategies:
- unbiased arbitrage: make a (small) profit regardless of match outcome
- biased arbitrage: win big on one outcome, no loss on other outcomes

