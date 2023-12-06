from api_calls.leverage import change_lev
from api_calls.orders import market_long_hedge_futures, market_short_hedge_futures, stop_order_short_hedge_futures, \
    stop_order_long_hedge_futures, cancel_futures_order
from api_calls.price import get_futures_current_price
from config import *
from general_functions.dollarConversion import convert_to_dollar
from general_functions.get_filters import get_futures_filters
import binance.exceptions


class TradingBot:

    def __init__(self, symbol, side,  initialInvestment, leverage, fee, client, logging):

        self.client = client
        self.logging = logging

        # Class Variables
        self.symbol = symbol
        self.side = side
        self.leverage = leverage
        self.investedAmount = abs(float(initialInvestment))
        self.fee = fee

        # Percentages
        self.actualPercentage = None
        self.actualPnLinDollar = None
        self.maximumPercentage = 0

        # Prices
        self.entryPrice = None
        self.currentPrice = get_futures_current_price(self.symbol, self.client)

        # Order Ids
        self.stopLossId = ''
        self.stopLossPlusId = ''
        self.stopLossPlusPercentage = 0


        # NEWLY ADDED
        self.addPercentage = stopLossPlusTriggerPercentage
        self.maximumRisk = maxRiskInDollar
        self.nextBuy = buyInDollars
        self.safeStopLossPlus = False

        # Fetch and set precision values
        self.quantityPrecision, self.pricePrecision, self.baseAssetPrecision, self.quoteAssetPrecision = get_futures_filters(
            client, symbol)

        # Important functions to start the Bot
        change_lev(client, symbol, self.leverage)

        self.investedAmountInDollar = convert_to_dollar(initialInvestment, self.currentPrice, self.leverage)

        print(
            f'[{self.symbol}] - [{self.side}] BOT INITIALISED')

    def buy(self, quantityToBuy):

        # Calculate the amount to buy
        self.currentPrice = get_futures_current_price(self.symbol, self.client)
        amountToBuy = (float(quantityToBuy) * leverage) / self.currentPrice
        amountToBuyInCurrency = round(amountToBuy, self.quantityPrecision)
        amountToBuyInDollar = convert_to_dollar(amountToBuyInCurrency, self.currentPrice, self.leverage)

        # Initialize variables
        order_id = None

        #  Verify if the amountToBuy is lower than the maximum allowed under maxBuyAmount
        if amountToBuyInDollar < (maxBuyAmount - amountToBuyInDollar):
            if self.side == 'Long':
                order_id = \
                    market_long_hedge_futures(self.client, amountToBuyInCurrency, self.symbol, 'Buy', self.logging)[
                        'orderId']


            elif self.side == 'Short':
                order_id = \
                    market_short_hedge_futures(self.client, amountToBuyInCurrency, self.symbol, 'Sell', self.logging)[
                        'orderId']

        else:
            print('Amount to buy is higher than the maximum allowed')
            return

        print(f'[{self.symbol}] - [{self.side}] BUY {amountToBuy} ({amountToBuyInDollar}$) at price {self.currentPrice}')

        self.investedAmount += abs(amountToBuyInCurrency)
        self.investedAmountInDollar = convert_to_dollar(self.investedAmount, self.currentPrice, self.leverage)

    def sell(self, quantityToSell, curency='USD'):

        amountToSell = 0

        if curency=='USD':
            # Calculate the amount to buy
            self.currentPrice = get_futures_current_price(self.symbol, self.client)
            amountToSell = (float(quantityToSell) * leverage) / self.currentPrice
            amountToSellInCurrency = round(amountToSell, self.quantityPrecision)
            amountToSellInDollar = convert_to_dollar(amountToSellInCurrency, self.currentPrice, self.leverage)
        else:
            amountToSellInCurrency = quantityToSell
            amountToSellInDollar = convert_to_dollar(amountToSellInCurrency, self.currentPrice, self.leverage)
        # Initialize variables
        order_id = None

        #  Verify if the amountToBuy is lower than the maximum allowed under maxBuyAmount
        if amountToSellInCurrency < self.investedAmount:
            if self.side == 'Long':
                order_id = \
                    market_long_hedge_futures(self.client, amountToSellInCurrency, self.symbol, 'Sell', self.logging)[
                        'orderId']

                self.investedAmount -= abs(amountToSellInCurrency)
                self.investedAmountInDollar = convert_to_dollar(self.investedAmount, self.currentPrice, self.leverage)

            elif self.side == 'Short':
                order_id = \
                    market_short_hedge_futures(self.client, amountToSellInCurrency, self.symbol, 'Buy', self.logging)[
                        'orderId']

            self.investedAmount -= abs(amountToSellInCurrency)
            self.investedAmountInDollar = convert_to_dollar(self.investedAmount, self.currentPrice, self.leverage)

        elif amountToSellInCurrency >= self.investedAmount:
            if self.side == 'Long':
                order_id = \
                    market_long_hedge_futures(self.client, self.investedAmount, self.symbol, 'Sell', self.logging)[
                        'orderId']

            elif self.side == 'Short':
                order_id = \
                    market_short_hedge_futures(self.client, self.investedAmount, self.symbol, 'Buy', self.logging)[
                        'orderId']

            self.investedAmount = 0
            self.investedAmountInDollar = 0


        else:
            print('Amount to buy is higher than the maximum allowed')
            return

        print(f'[{self.symbol}] - [{self.side}] BUY {amountToSell} ({amountToSellInDollar}$) at price {self.currentPrice}')



    def calculate_stop_loss(self, percentage_loss):

        # Calculate the total fee
        total_fee = abs(self.investedAmount) * self.fee / 100

        # Adjusted amount after fee
        adjusted_amount = abs(self.investedAmount) - total_fee

        # Calculate the leveraged amount
        leveraged_amount = adjusted_amount * self.leverage

        # Calculate the dollar value at risk
        dollar_risk = leveraged_amount * percentage_loss / 100

        # Calculate the price difference per unit
        price_difference_per_unit = dollar_risk / (leveraged_amount / self.entryPrice)

        # Calculate stop-loss price
        if self.side == 'Long':
            # For a long position, stop-loss is below the entry price
            stop_loss_price = self.entryPrice - price_difference_per_unit
        elif self.side == 'Short':
            # For a short position, stop-loss is above the entry price
            stop_loss_price = self.entryPrice + price_difference_per_unit
        else:
            raise ValueError("Invalid position type. Choose 'long' or 'short'.")

        return stop_loss_price

    def calculate_stop_loss_plus(self):

        # Calculate the total fee
        total_fee = abs(self.investedAmount) * self.fee / 100

        # Adjust the maximum risk for the fee
        adjusted_max_risk = self.maximumRisk - total_fee

        # Calculate the leverage factor
        leverage_factor = abs(self.investedAmount) / (abs(self.investedAmount) - total_fee)

        # Calculate stop-loss price
        if self.side == 'Long':
            # For a long position, the stop-loss price is lower than the average price
            price_difference = adjusted_max_risk / (abs(self.investedAmount) * leverage_factor)
            stop_loss_price = self.entryPrice - price_difference
        elif self.side == 'Short':
            # For a short position, the stop-loss price is higher than the average price
            price_difference = adjusted_max_risk / (abs(self.investedAmount) * leverage_factor)
            stop_loss_price = self.entryPrice + price_difference
        else:
            raise ValueError("Invalid position type. Choose 'long' or 'short'.")

        return stop_loss_price

    def calculate_stop_loss_safe(self, percentage_win):

        # Calculate the fee
        fee = abs(self.investedAmount) * self.fee / 100

        # Adjusted amount after fee
        adjusted_amount = abs(self.investedAmount) - fee

        # Calculate the leveraged amount
        leveraged_amount = adjusted_amount * (1 + self.fee / 100)

        # Calculate the dollar value at risk
        dollar_risk = leveraged_amount * percentage_win / 100

        # Calculate the price difference per unit
        price_difference_per_unit = dollar_risk / adjusted_amount

        # Calculate stop-loss price
        if self.side == 'Long':
            # For a long position, stop-loss is below average price
            stop_loss_price = self.entryPrice + price_difference_per_unit
        elif self.side == 'Short':
            # For a short position, stop-loss is above average price
            stop_loss_price = self.entryPrice - price_difference_per_unit
        else:
            raise ValueError("Invalid position type. Choose 'long' or 'short'.")

        return stop_loss_price




    def activate_stop_loss(self, stopPercentage=stopLoss):

        priceStopLoss = None
        order_id = None

        # Calculate Price Stop Loss
        priceStopLoss = round(self.calculate_stop_loss(stopPercentage), self.pricePrecision)

        # Cancel other Stop Losses
        if self.stopLossPlusId != '':
            self.cancel_order(self.stopLossPlusId)
        if self.stopLossId != '':
            self.cancel_order(self.stopLossId)

        if self.side == 'Long':

            order_id = stop_order_long_hedge_futures(self.client, self.investedAmount, self.symbol, 'Sell',
                                                         priceStopLoss, self.logging)['orderId']

        elif self.side == 'Short':
            order_id = \
                stop_order_short_hedge_futures(self.client, abs(self.investedAmount), self.symbol, 'Buy',
                                               priceStopLoss, self.logging)['orderId']
        else:
            raise ValueError("Not possible to set Stop-Loss")
            return


        print(f'[{self.symbol}] - [{self.side}] STOP-LOSS - {self.investedAmount} ({self.investedAmountInDollar}$) at price {priceStopLoss}')

        self.stopLossId = order_id

    def activate_stop_loss_plus(self, mode):

        priceStopLoss = None
        order_id = None

        if mode == "Add":
            priceStopLoss = round(self.calculate_stop_loss_plus(), self.pricePrecision)
        elif mode == "Safe":
            priceStopLoss = round(self.calculate_stop_loss_safe(self.percentageStopSafe * stopLossPlusSafeRatio), self.pricePrecision)
            self.stopLossPlusPercentage = self.percentageStopSafe

        # Cancel other Stop Losses
        if self.stopLossPlusId != '':
            self.cancel_order(self.stopLossPlusId)
        if self.stopLossId != '':
            self.cancel_order(self.stopLossId)

        if self.side == 'Long':
            try:
                order_id = stop_order_long_hedge_futures(self.client, abs(round(self.investedAmount, self.quantityPrecision)), self.symbol, 'Sell',
                                                             round(priceStopLoss, self.pricePrecision), self.logging)['orderId']
            except binance.exceptions.BinanceAPIException as e:
                if e.code == -2021:
                    # Log the error
                    self.logging.error(f'Binance API Exception: {e}')

                    # Create a market order to sell
                    try:
                        self.sell(self.investedAmount, curency='NOTUSD')
                        self.logging.info(f"Market order placed instead - all sold")
                    except Exception as market_order_exception:
                        self.logging.error(f"Failed to place market order: {market_order_exception}")

                else:
                    # Handle other Binance API exceptions if necessary
                    self.logging.error(f'Unexpected Binance API Exception: {e}')


        elif self.side == 'Short':
            try:
                order_id = \
                    stop_order_short_hedge_futures(self.client, abs(round(self.investedAmount, self.quantityPrecision)), self.symbol, 'Buy',
                                                   round(priceStopLoss, self.pricePrecision), self.logging)['orderId']
            except binance.exceptions.BinanceAPIException as e:
                if e.code == -2021:
                    # Log the error
                    self.logging.error(f'Binance API Exception: {e}')

                    # Create a market order to sell
                    try:
                        self.sell(self.investedAmount, curency='NOTUSD')
                        self.logging.info(f"Market order placed instead - all sold")
                    except Exception as market_order_exception:
                        self.logging.error(f"Failed to place market order: {market_order_exception}")

                else:
                    # Handle other Binance API exceptions if necessary
                    self.logging.error(f'Unexpected Binance API Exception: {e}')
        else:
            raise ValueError("Not possible to set Stop-Loss Plus")
            return

        print(
            f'[{self.symbol}] - [{self.side}] STOP-LOSS PLUS - {self.investedAmount} ({self.investedAmountInDollar}$) at price {priceStopLoss}')

        self.stopLossPlusId = order_id

    def cancel_order(self, orderNumber):
        try:

            cancel_futures_order(self.client, orderNumber, self.symbol)

            if orderNumber == self.stopLossId:
                self.stopLossId = ''
                print(
                    f'[{self.symbol}] - [{self.side}] STOP-LOSS PLUS - Id. {orderNumber} Canceled')
            elif orderNumber == self.stopLossPlusId:
                self.stopLossPlusId = ''
                print(
                    f'[{self.symbol}] - [{self.side}] STOP-LOSS PLUS - Id.  {orderNumber} Canceled')

        except binance.exceptions.BinanceAPIException as e:

            # Handle other Binance API exceptions if necessary
            print(f'Unexpected Binance API Exception: {e}')

    def update_stats(self, positions_info):

        found = False

        # Update bot stats, log bot
        for side, positions in positions_info.items():
            for position in positions:
                if self.symbol == position[0] and self.side == side:
                    self.investedAmount = abs(position[1])
                    self.entryPrice = position[2]
                    found = True

        if not found:
            self.investedAmount = 0
            self.entryPrice = 0
            return


        self.currentPrice = float(get_futures_current_price(self.symbol, self.client))

        # Calculate the fee
        if self.side == 'Long':

            # Calculations
            self.investedAmountInDollar = convert_to_dollar(self.investedAmount, self.currentPrice, self.leverage)
            realPercentage = (((self.currentPrice / self.entryPrice) - 1) * 100)
            self.actualPercentage = round((realPercentage * self.leverage) - (fee * self.leverage), 2)
            self.actualPnLinDollar = round(self.investedAmountInDollar * (self.actualPercentage / 100), 2)

        elif self.side == 'Short':

            # Calculations
            self.investedAmountInDollar = convert_to_dollar(self.investedAmount, self.currentPrice, self.leverage)
            realPercentage = (((self.currentPrice / self.entryPrice) - 1) * -1 * 100)
            self.actualPercentage = round((realPercentage * self.leverage) - (fee * self.leverage), 2)
            self.actualPnLinDollar = round(self.investedAmountInDollar * (self.actualPercentage / 100), 2)

        if self.actualPercentage > self.maximumPercentage:
            self.maximumPercentage = self.actualPercentage

        self.percentageStopSafe = self.maximumPercentage * stopLossPlusSafeRatio

        print(
            f'[{self.symbol}] - [{self.side}] STATUS UPDATED')