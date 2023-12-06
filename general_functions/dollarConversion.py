def convert_to_dollar(currentAmount, entryPrice, leverage):

    return round((currentAmount * entryPrice) / leverage, 2)