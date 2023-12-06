import time

import pandas as pd

def get_futures_positions_information(client):

    # Search for Open Orders
    futureInfo = client.futures_position_information()

    trades = {'Long': [], 'Short': []}


    for info in futureInfo:
        if float(info["positionAmt"]) > 0:
            symbol = str(info["symbol"])
            positionAmt = float(info["positionAmt"])
            entryPrice = float(info["entryPrice"])
            unRealizedProfit = float(info["unRealizedProfit"])
            leverage = float(info["leverage"])
            side = "Long"

            trades[side].append([symbol, positionAmt, entryPrice, unRealizedProfit, leverage])

        elif float(info["positionAmt"]) < 0:
            symbol = str(info["symbol"])
            positionAmt = float(info["positionAmt"])
            entryPrice = float(info["entryPrice"])
            unRealizedProfit = float(info["unRealizedProfit"])
            leverage = float(info["leverage"])
            side = "Short"
            trades[side].append([symbol, positionAmt, entryPrice, unRealizedProfit, leverage])

    return trades

def get_futures_account_trades(client, symbol):

    # Search for Latest Trades for specific symbol
    account = client.futures_account_trades(symbol=symbol)

    client.ord
    df = pd.DataFrame.from_dict(account)

    if not df.empty:
        df = df.drop(
            ['id', 'marginAsset', 'quoteQty', 'buyer', 'maker', 'commissionAsset', 'time', 'symbol'],
            axis=1)

    return df

def get_futures_trade_pnl_and_comission(client, symbol, orderIdInitial, orderId2limit):

    time.sleep(3)

    account = client.futures_account_trades(symbol=symbol)

    print('\n\norderIdInitial: {} | orderId2limit: {}'.format(orderIdInitial, orderId2limit))

    print(f'Account Trades:\n\n {account}\n\n')
    realizedPnl1, comission1, quantityTrade, realizedPnl2, comission2 = 0, 0, 0, 0, 0

    print(f'Searching for PnL and Comission for the following orders:\n - Initial: {orderIdInitial}\n - Limit: {orderId2limit}')
    for info in account:
        if info['orderId']==orderIdInitial:
            realizedPnl1 += float(info["realizedPnl"])
            comission1 += float(info["commission"])
            quantityTrade += float(info['qty'])
            print(f'Found PnL and Comission for the order {orderIdInitial}:\n'
                  f' - quantity: {quantityTrade}\n'
                  f' - PnL: {realizedPnl1}\n'
                  f' - Comission: {comission1}')
        if info['orderId']==orderId2limit:
            realizedPnl2 += float(info["realizedPnl"])
            comission2 += float(info["commission"])
            print(f'Found PnL and Comission for the order {orderId2limit}:\n'
                  f' - PnL: {realizedPnl2}\n'
                  f' - Comission: {comission2}')

    finalPnl = realizedPnl1 + realizedPnl2
    finalComission = comission1 + comission2

    return finalPnl, finalComission, quantityTrade


