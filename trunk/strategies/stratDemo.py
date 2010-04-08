import random


# Rudimentary proof-of-concept strategy; takes in a 'portfolio' that is a two-element list; first is a float
# (cash on hand) and second is a list of stocks, organized as follows:
# [$$$$$, [ [symbol, shares], [symbol, shares], [symbol, shares],...] ]

# Note: actual portfolio will be OO


# This demo strategy prints out the current amount of money in the portfolio and adds a random amount 
# (up to 1000) to it, then prints the stocks and volume owned
def firstStrategy(portfolio,positions,timestamp,stockInfo):
    '''
    Decides what to do based on current and past stock data.
    Returns a tuple of lists (sellData, buyData) - the infomation needed to execute buy and sell transactions
    The portfolio is a portfolio object that has your currently held stocks (currStocks) and your current cash (currCash)
    The timestamp is the current timestamp that the simulator is running on
    stockInfo is the StrategyData that the strategy can use to find out information about the stocks.  See below.
    '''
    output = []
    #This first for loop goes over all of the stock data to determine which stocks to buy
    for stock in stockInfo.getStocks(startTime = timestamp - 86400,endTime = timestamp):
        if stock['adj_open'] < stock['adj_close'] and (stock['adj_high'] - stock['adj_close']) > (stock['adj_open'] - stock['adj_close']):
            # Format for stock buys (volume,symbol,type,lengthValid,closeType,OPTIONAL: limitPrice)
            order = stockInfo.OutputOrder()
            order.symbol = stock['symbol']
            order.volume = stock['volume']/2
            order.task = 'buy'
            order.orderType = 'moc'
            order.duration = 172800
            output.append(order.getOuput())      
            
    #This for loop goes over all of our current stocks to determine which stocks to sell
    for stock in portfolio.currStocks:
        if (stockInfo.getPrices(timestamp - 86400, timestamp,stock,'adj_close')[0]-stockInfo.getPrices(timestamp - 86400, timestamp,stock,'adj_low')[0]) > (stockInfo.getPrices(timestamp - 86400, timestamp,stock,'adj_high')[0]-stockInfo.getPrices(timestamp - 86400, timestamp,stock,'adj_open')[0]):
            # Format for stock sells (volume,symbol,type,lengthValid,closeType,OPTIONAL: limitPrice)
            order = stockInfo.OutputOrder()
            order.symbol = stock
            order.volume = portfolio.currStocks[stock]/2
            order.task = 'sell'
            order.orderType = 'moo'
            order.closeType = 'fifo'
            order.duration = 172800
            output.append(order.getOuput())
    # return the sell orders and buy orders to the simulator to execute
    return output

def dollarStrategy(portfolio,positions,timestamp,stockInfo):
    '''
    COMMENTS HERE
    '''
    output = []
    for yesterday in stockInfo.getStocksArray(timestamp - 86400 * 2, timestamp - 86400):
        if yesterday['close'] > 1:
            for today in stockInfo.getStocksArray(timestamp-86400,timestamp,yesterday['symbol']):
                if today['close'] < 1:
                    order = stockInfo.OutputOrder()
                    order.symbol = today['symbol']
                    order.volume = 10000./today['close']
                    order.task = 'buy'
                    order.orderType = 'limit'
                    order.limitPrice = today['close']
                    order.duration = 86400
                    output.append(order.getOuput())
    for position in positions.getPositions():
        if (position['timestamp'] <= (timestamp - 86400 * 20)) and (position['shares'] > 0):
            order = stockInfo.OutputOrder()
            order.symbol = position['symbol']
            order.volume = position['shares']
            order.task = 'sell'
            order.orderType = 'moo'
            order.closeType = 'fifo'
            order.duration = 86400
            output.append(order.getOuput())
    return output