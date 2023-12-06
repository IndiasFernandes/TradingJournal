import binance
import pandas as pd


pd.set_option('display.max_rows', None)
pd.set_option('display.max_columns', 500)

from api_calls.price import get_futures_current_price

def set_futures_stop_loss(symbol, sl_percentage, side, quantity, client):

    price = get_futures_current_price(symbol, client)
    len_price = len(str(price).split(".")[1])

    if side == 'Short':
        positionSide = 'SHORT'
        price_stop = round(price + (price * sl_percentage * 0.001), len_price)
        price_exec = round(price + (price * (sl_percentage - 1) * 0.001), len_price)
    elif side == 'Long':
        positionSide = 'LONG'
        price_stop = round(price - (price * sl_percentage * 0.001), len_price)
        price_exec = round(price - (price * (sl_percentage - 1) * 0.001), len_price)
    try:
        client.futures_create_order(positionSide=positionSide,
                                    symbol=symbol,
                                    side=binance.enums.SIDE_SELL,
                                    type=binance.enums.FUTURE_ORDER_TYPE_STOP,
                                    quantity=quantity,
                                    price=price_exec,
                                    stopPrice=price_stop)
        status = f'Added Stop-Loss of {quantity} to {symbol} at price {price}'
    except:
        status = f'Impossible to implement Stop-Loss to {symbol}'

    return status, price_stop, price_exec

def get_all_open_orders(client):
    account = client.futures_get_all_orders()
    orders = {'Long': [], 'Short': []}
    for info in account:
        if info['status'] == 'NEW':
            if info['type'] == 'TRAILING_STOP_MARKET':
                type = 'Trailing Stop'
                if info['positionSide'] == 'LONG':

                    side = 'Long'
                    orderId = info['orderId']
                    stopPrice = info['stopPrice']
                    activatePrice = info['activatePrice']
                    priceRate = info['priceRate']
                    origQty = info['origQty']
                    symbol = info['symbol']
                    orders[side].append([symbol,type, orderId, stopPrice, activatePrice, priceRate, origQty])
                elif info['positionSide'] == 'SHORT':
                    side = 'Short'
                    orderId = info['orderId']
                    stopPrice = info['stopPrice']
                    activatePrice = info['activatePrice']
                    priceRate = info['priceRate']
                    origQty = info['origQty']
                    symbol = info['symbol']
                    orders[side].append([symbol,type, orderId, stopPrice, activatePrice, priceRate, origQty])
            if info['type'] == 'LIMIT':
                type = 'Limit'
                if info['positionSide'] == 'LONG':

                    side = 'Long'
                    orderId = info['orderId']
                    price = info['price']
                    origQty = info['origQty']
                    symbol = info['symbol']
                    orders[side].append([symbol,type, orderId, price, origQty])
                elif info['positionSide'] == 'SHORT':
                    side = 'Short'
                    orderId = info['orderId']
                    price = info['price']
                    origQty = info['origQty']
                    symbol = info['symbol']
                    orders[side].append([symbol,type, orderId, price, origQty])
            if info['type'] == 'STOP_MARKET':
                type = 'Stop'
                if info['positionSide'] == 'LONG':

                    side = 'Long'
                    orderId = info['orderId']
                    stopPrice = info['stopPrice']
                    origQty = info['origQty']
                    symbol = info['symbol']
                    orders[side].append([symbol,type, orderId, stopPrice, origQty])
                elif info['positionSide'] == 'SHORT':
                    side = 'Short'
                    orderId = info['orderId']
                    stopPrice = info['stopPrice']
                    origQty = info['origQty']
                    symbol = info['symbol']
                    orders[side].append([symbol,type, orderId, stopPrice, origQty])
    return orders

def get_spot_open_orders(symbol, client):
    orders = client.get_spot_open_orders(symbol=symbol)
    df = pd.DataFrame.from_dict(orders)

    return df

def get_futures_symbol_open_orders(client, symbol):
    # Search for Open Orders for a specific symbol
    orders = client.futures_get_open_orders()
    df = pd.DataFrame.from_dict(orders)

    if not df.empty:
        df = df.drop(
            ['status', 'clientOrderId', 'executedQty', 'cumQuote', 'timeInForce', 'type', 'reduceOnly', 'closePosition', 'workingType', 'priceProtect', 'origType', 'updateTime', 'time', 'avgPrice', 'stopPrice'],
            axis=1)

    return df

def get_futures_all_orders(client):
    # Search for Open Orders
    orders = client.futures_get_all_orders()
    df = pd.DataFrame.from_dict(orders)

    if not df.empty:
        df = df.drop(
            ['maxNotionalValue', 'isAutoAddMargin', 'notional', 'isolatedWallet', 'updateTime'],
            axis=1)

    return df

def cancel_futures_order(client, orderID, symbol):
    result = client.futures_cancel_order(
        symbol=symbol,
        orderId=orderID)

    return result

def cancel_all_futures_orders(client, symbol):
    result = client.futures_cancel_all_open_orders(
        symbol=symbol)

    return result

def market_futures(client, amount, symbol, action):
    if action == 'Buy':
        side = binance.enums.SIDE_BUY
    elif action == 'Sell':
        side = binance.enums.SIDE_SELL

    order = client.futures_create_order(symbol=symbol,
                                side=side,
                                type=binance.enums.ORDER_TYPE_MARKET,
                                quantity=amount)

    print(f'Placed Futures Market {action} Order of {amount} for {symbol}')

    return order

def limit_futures(client, amount, symbol, action, price):

    if action == 'Buy':
        side = binance.enums.SIDE_BUY
    elif action == 'Sell':
        side = binance.enums.SIDE_SELL

    order = client.futures_create_order(symbol=symbol,
                            side=side,
                            type=binance.enums.ORDER_TYPE_LIMIT,
                            quantity=amount,
                            timeInForce='GTC',
                            price=price)

    print(f'Placed Futures Limit {action} Order of {amount} for {symbol} at {price}')

    return order

def stop_order_futures(client, amount, symbol, action, price):

    if action == 'Buy':
        side = binance.enums.SIDE_BUY
    elif action == 'Sell':
        side = binance.enums.SIDE_SELL

    order = client.futures_create_order(symbol=symbol,
                            side=side,
                            type=binance.enums.FUTURE_ORDER_TYPE_STOP_MARKET,  # t
                            quantity=amount, #try without
                            timeInForce='GTC',
                            stopPrice=price,
                            reduceOnly=True)

    print(f'Placed Futures Stop {action} Order of {amount} for {symbol} at {price}')

    return order

def take_profit_futures(client, amount, symbol, action, price):

    if action == 'Buy':
        side = binance.enums.SIDE_BUY
    elif action == 'Sell':
        side = binance.enums.SIDE_SELL

    order = client.futures_create_order(symbol=symbol,
                            side=side,
                            type=binance.enums.FUTURE_ORDER_TYPE_TAKE_PROFIT_MARKET,  # t
                            quantity=amount, #try without
                            timeInForce='GTC',
                            stopPrice=price,
                            reduceOnly=True)

    print(f'Placed Futures Take Profit {action} Order of {amount} for {symbol} at {price}')

    return order

def market_long_hedge_futures(client, amount, symbol, action, logger):

    if action == 'Buy':
        side = binance.enums.SIDE_BUY
    elif action == 'Sell':
        side = binance.enums.SIDE_SELL

    # print(f'Placing Futures Market Long {action} Order of {amount} for {symbol} for side {side}')
    # logger.info(f'Placing Futures Market Long {action} Order of {amount} for {symbol} for side {side}')
    try:

        order = client.futures_create_order(symbol=symbol,
                                    side=side,
                                    type=binance.enums.ORDER_TYPE_MARKET,
                                    positionSide='LONG',
                                    quantity=amount)
        print(f'Placed Futures Market Long {action} Order of {amount} for {symbol}')

        return order


    except binance.exceptions.BinanceAPIException as e:

        # Log and handle exceptions
        logger.info(f'Error occurred: {str(e)}', exc_info=True)

def stop_order_long_hedge_futures(client: object, amount: object, symbol: object, action: object, price: object, logger: object) -> object:

    if action == 'Buy':
        side = binance.enums.SIDE_BUY
    elif action == 'Sell':
        side = binance.enums.SIDE_SELL

    # print(f'Placing Futures Stop Long {action} Order of {amount} for {symbol} for side {side} at {price}')
    # logger.info(f'Placing Futures Stop Long {action} Order of {amount} for {symbol} for side {side} at {price}')

    order = client.futures_create_order(symbol=symbol,
                            side=side,
                            type=binance.enums.FUTURE_ORDER_TYPE_STOP_MARKET,  # t
                            quantity=amount, #try without
                            timeInForce='GTC',
                            stopPrice=price,
                            positionSide='LONG')

    print(f'Placed Futures Stop Long {action} Order of {amount} for {symbol} at {price}')

    return order




def take_profit_long_hedge_futures(client, amount, symbol, action, price, logger):

    if action == 'Buy':
        side = binance.enums.SIDE_BUY
    elif action == 'Sell':
        side = binance.enums.SIDE_SELL

    #print(f'Placing Futures Take Profit Long {action} Order of {amount} for {symbol} for side {side} at {price}')
    # logger.info(f'Placing Futures Take Profit Long {action} Order of {amount} for {symbol} for side {side} at {price}')
    try:

        order = client.futures_create_order(symbol=symbol,
                                side=side,
                                type=binance.enums.FUTURE_ORDER_TYPE_TAKE_PROFIT_MARKET,  # t
                                quantity=amount, #try without
                                timeInForce='GTC',
                                positionSide='LONG',
                                stopPrice=price)

        print(f'Placed Futures Take Profit Long{action} Order of {amount} for {symbol} at {price}')

        return order

    except binance.exceptions.BinanceAPIException as e:

        # Log and handle exceptions
        logger.info(f'Error occurred: {str(e)}', exc_info=True)


def market_short_hedge_futures(client, amount, symbol, action, logger):

    if action == 'Buy':
        side = binance.enums.SIDE_BUY
    elif action == 'Sell':
        side = binance.enums.SIDE_SELL

    #print(f'Placing Futures Market Short {action} Order of {amount} for {symbol} for side {side}')

    #print(f'Placing Futures Market Short {action} Order of {amount} for {symbol} for side {side}')
    # logger.info(f'Placing Futures Market Short {action} Order of {amount} for {symbol} for side {side}')
    order = client.futures_create_order(symbol=symbol,
                                side=side,
                                type=binance.enums.ORDER_TYPE_MARKET,
                                positionSide='SHORT',
                                quantity=amount)

    #print(f'Placed Futures Market Short {action} Order of {amount} for {symbol}')

    return order



def stop_order_short_hedge_futures(client, amount, symbol, action, price, logger):

    if action == 'Buy':
        side = binance.enums.SIDE_BUY
    elif action == 'Sell':
        side = binance.enums.SIDE_SELL

    #print(f'Placing Futures Stop Short {action} Order of {amount} for {symbol} for side {side} at {price}')

    # logger.info(f'Placing Futures Stop Short {action} Order of {amount} for {symbol} for side {side} at {price}')

    order = client.futures_create_order(symbol=symbol,
                            side=side,
                            type=binance.enums.FUTURE_ORDER_TYPE_STOP_MARKET,  # t
                            quantity=amount, #try without
                            timeInForce='GTC',
                            stopPrice=price,
                            positionSide='SHORT')

    #print(f'Placed Futures Stop Short {action} Order of {amount} for {symbol} at {price}')

    return order



def take_profit_short_hedge_futures(client, amount, symbol, action, price, logger):

    if action == 'Buy':
        side = binance.enums.SIDE_BUY
    elif action == 'Sell':
        side = binance.enums.SIDE_SELL

    #print(f'Placing Futures Take Profit Short {action} Order of {amount} for {symbol} for side {side} at {price}')
    # logger.info(f'Placing Futures Take Profit Short {action} Order of {amount} for {symbol} for side {side} at {price}')
    try:

        order = client.futures_create_order(symbol=symbol,
                                side=side,
                                type=binance.enums.FUTURE_ORDER_TYPE_TAKE_PROFIT_MARKET,  # t
                                quantity=amount, #try without
                                timeInForce='GTC',
                                stopPrice=price,
                                positionSide='SHORT')

        #print(f'Placed Futures Take Profit Short {action} Order of {amount} for {symbol} at {price}')

        return order

    except binance.exceptions.BinanceAPIException as e:

        # Log and handle exceptions
        logger.info(f'Error occurred: {str(e)}', exc_info=True)


def trailing_stop_long_futures(client, amount, symbol, action, activationPrice, callbackRate, logger):

    if action == 'Buy':
        side = binance.enums.SIDE_BUY
    elif action == 'Sell':
        side = binance.enums.SIDE_SELL

    #print(f'Placing Futures Trailing Stop Long {action} Order of {amount} for {symbol} for side {side} at {activationPrice} with a callback of {callbackRate}%')
    # logger.info(f'Placing Futures Trailing Stop Long {action} Order of {amount} for {symbol} for side {side} at {activationPrice} with a callback of {callbackRate}%')
    try:
        order = client.futures_create_order(symbol=symbol,
                                                side=side,
                                                type='TRAILING_STOP_MARKET',
                                                activationPrice=activationPrice,
                                                callbackRate=callbackRate,
                                                positionSide='LONG',
                                                quantity=amount)

        #print(f'Placed Futures Trailing Stop Long {action} Order of {amount} for {symbol} at {activationPrice} with a callback of {callbackRate}%')

        return order

    except binance.exceptions.BinanceAPIException as e:

        # Log and handle exceptions
        logger.info(f'Error occurred: {str(e)}', exc_info=True)



def trailing_stop_short_futures(client, amount, symbol, action, activationPrice, callbackRate, logger):
    if action == 'Buy':
        side = binance.enums.SIDE_BUY
    elif action == 'Sell':
        side = binance.enums.SIDE_SELL

    #print (f'Placing Futures Trailing Stop Short {action} Order of {amount} for {symbol} for side {side} at {activationPrice} with a callback of {callbackRate}%')
    # logger.info(f'Placing Futures Trailing Stop Short {action} Order of {amount} for {symbol} for side {side} at {activationPrice} with a callback of {callbackRate}%')
    try:

        order = client.futures_create_order(symbol=symbol,
                                            side=side,
                                            type='TRAILING_STOP_MARKET',
                                            activationPrice=activationPrice,
                                            callbackRate=callbackRate,
                                            positionSide='SHORT',
                                            quantity=amount)

        #print(
        #    f'Placed Futures Trailing Stop Short {action} Order of {amount} for {symbol} at {activationPrice} with a callback of {callbackRate}%')

        return order

    except binance.exceptions.BinanceAPIException as e:

        # Log and handle exceptions
        logger.info(f'Error occurred: {str(e)}', exc_info=True)

