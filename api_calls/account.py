import pandas as pd

def get_futures_account_balance(client):
    # Search for Open Orders
    account = client.futures_account_balance()
    df = pd.DataFrame.from_dict(account)

    if not df.empty:
        df = df.drop(
            ['accountAlias', 'updateTime'],
            axis=1)

    return df

def get_futures_trades(client):
    # Search for Open Orders
    account = client.futures_account_trades()
    df = pd.DataFrame.from_dict(account)

    if not df.empty:
        df = df.drop(
            ['id', 'marginAsset', 'quoteQty', 'time', 'buyer'],
            axis=1)

    return df

def change_futures_margin_mode(client, symbol, marginType):
    try:
        if marginType == 'Isolated':
            client.futures_change_margin_type(symbol=symbol,
                                       marginType='ISOLATED')
            print(f'Margin Type of {symbol} changed to {marginType}')
        elif marginType == 'Cross':
            client.futures_change_margin_type(symbol=symbol,
                                              marginType='CROSS')
            print(f'Margin Type of {symbol} changed to {marginType}')
    except:

        print(f"Didn't change Margin Type of {symbol}")

    return marginType

def update_account_info(client):
    account = client.futures_account()
    asset_index = 5 # returns USDT

    account_info = {
        'assets': account['assets'][asset_index]['asset'],
        'walletBalance': account['assets'][asset_index]['walletBalance'],
        'unrealizedProfit': account['assets'][asset_index]['unrealizedProfit'],
        'marginBalance': account['assets'][asset_index]['marginBalance'],
        'maintMargin': account['assets'][asset_index]['maintMargin'],
        'initialMargin': account['assets'][asset_index]['initialMargin'],
        'positionInitialMargin': account['assets'][asset_index]['positionInitialMargin'],
        'openOrderInitialMargin': account['assets'][asset_index]['openOrderInitialMargin'],
        'maxWithdrawAmount': account['assets'][asset_index]['maxWithdrawAmount'],
        'crossWalletBalance': account['assets'][asset_index]['crossWalletBalance'],
        'crossUnrealizedProfit': account['assets'][asset_index]['crossUnPnl'],
        'availableBalance': account['assets'][asset_index]['availableBalance'],
        'marginAvailable': account['assets'][asset_index]['marginAvailable'],
    }

    return account_info

def get_margin_ratio(client):

    # Search for Open Orders
    account = client.futures_account()
    margin_ratio = round((float(account['totalMaintMargin']) / float(account['totalMarginBalance']) * 100), 2)

    return margin_ratio