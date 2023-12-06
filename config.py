# config.py

RISK_PER_DAY = "10%"
OBJECTIVE_PER_DAY = "100%"
# Add other configurations like SQL credentials here


# Variables Bot
symbol = 'ADAUSDT'
leverage = 20
fee = 0.008

# Normal Stop-Loss Variables:
stopLoss = 15 # value in % (leveraged)

# Stop-Loss Plus Variables
maxRiskInDollar = 1
buyInDollars = 2 # value bought on each
stopLossPlusTriggerPercentage = 1.5  # percentage where new buy gets activated
stopLossPlusSafePercentage = 15  # percentage profit starts to be locked
stopLossPlusSafeRatio = 0.3 # percentage of profit locks comparing to the maximum percentage reached

nextBuyIncrease = 1.3 # When adding more to the trade, increase the amount multiplying this %
addPercentageIncrease = 1.25 # When adding more to the trade, increase the percentage multiplying this %
maximumRiskDecrease = 0.2 # When adding more to the trade, decrease the maximum risk by this $

# Buy
maxBuyAmount = 100 # Maximum Amount to Buy in Dollars $

# SELL
sellInDollars = 1
fullAmountPercentageSell = 10 # When account is more than this % it starts selling units on profit
