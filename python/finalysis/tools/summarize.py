import pandas as pd
import numpy as np
import yfinance as yf
import sys

TICKER_FILE = '/home/chrism/sw/finalysis/params/restaurant_sector_fund/tickers.csv'
OUT_FILE = None

a = 1
while a <= len(sys.argv)-1 :
	if sys.argv[a] == '-f' :
		TICKER_FILE = sys.argv[a+1]
		a += 2
	elif sys.argv[a] == '-o' :
		OUT_FILE = sys.argv[a+1]
		a += 2

def main () :
	sector_file = pd.read_csv(TICKER_FILE)
	ticker_list = sector_file.Symbol.tolist()
	holding_list = sector_file.Holding.tolist()
	avg_cost = sector_file.AverageCost.tolist()

	tickers = yf.Tickers(ticker_list)

	columns = ['Close',
	           '52Low',
	           '52High',
	           'CurrentValue',
	           '7DayValue',
	           '30DayValue',
	           'Price%',
	           'Value%',
	           'Holdings']
	d = pd.DataFrame([],columns=columns,index=ticker_list)
	history = tickers.history(period='1y')
	highs = history['Close'].max()
	lows = history['Close'].min()
	for i,sym in enumerate(ticker_list) :
		one_day_close_price = history['Close',sym][-1]
		seven_day_close_price = history['Close',sym][-7]
		thirty_day_close_price = history['Close',sym][-30]
		d.loc[sym,'Close'] = one_day_close_price
		d.loc[sym,'52Low'] = lows[sym]
		d.loc[sym,'52High'] = highs[sym]
		d.loc[sym,'CurrentValue'] =  holding_list[i]*(one_day_close_price - avg_cost[i])
		d.loc[sym,'7DayValue'] =  holding_list[i]*(seven_day_close_price - avg_cost[i])
		d.loc[sym,'30DayValue'] = holding_list[i]*(thirty_day_close_price - avg_cost[i])

	current_day_total_price = d['Close'].sum()
	current_day_total_value = d['CurrentValue'].sum()
	num_holdings = sum(holding_list)
	for i,sym in enumerate(ticker_list) :
		d.loc[sym,'Price%'] = 100*d.loc[sym,'Close']/current_day_total_price
		d.loc[sym,'Value%'] = 100*d.loc[sym,'CurrentValue']/current_day_total_value
		d.loc[sym,'Holdings'] = holding_list[i]

	if OUT_FILE is not None :
		print(f'writing to {OUT_FILE}')
		d.to_csv(OUT_FILE)

	print(d)
	print('Total value: ' + str(current_day_total_value))

if __name__ == '__main__' :
	main()