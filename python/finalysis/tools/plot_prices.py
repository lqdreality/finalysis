import pandas as pd
import numpy as np
import yfinance as yf
import sys

TICKER_FILE = None
TICKER_LIST = []
TIME_LAG = '1mo'
NORMALIZED = False
AVERAGE = False
PLOT_LIB = 'matplotlib'

a = 1
while a <= len(sys.argv)-1 :
	if sys.argv[a] == '-f' :
		TICKER_FILE = sys.argv[a+1]
		a += 2
	elif sys.argv[a] == '-h' :
		TIME_LAG = sys.argv[a+1]
		a += 2
	elif sys.argv[a] == '-n' :
		NORMALIZED = True
		a += 1
	elif sys.argv[a] == '-i' :
		a += 1
		while a <= len(sys.argv)-1 and sys.argv[a][0] != '-' :
			TICKER_LIST.append(sys.argv[a])
			a += 1
	elif sys.argv[a] == '--average' :
		AVERAGE = True
		a += 1
	elif sys.argv[a] == '--plot' :
		PLOT_LIB = sys.argv[a+1].lower()
		a += 2
	else :
		raise Exception(f'Unrecognized option: {sys.argv[a]}')

if PLOT_LIB == 'matplotlib' :
	import matplotlib.pyplot as plt
	LINE_WIDTH = 2
	MARKER_SIZE = 10
elif PLOT_LIB == 'plotly' :
	import plotly.graph_objects as go

def main () :
	if TICKER_FILE is not None :
		sector_file = pd.read_csv(TICKER_FILE)
		ticker_list = sector_file.Symbol.tolist()

	if len(TICKER_LIST) != 0 :
		ticker_list = TICKER_LIST
	
	tickers = yf.Tickers(ticker_list)

	history = tickers.history(period=TIME_LAG)

	if AVERAGE :
		N = history.shape[0]
		average = np.zeros(N,)

	if NORMALIZED :
		max_vals = history['Close'].max()

	if PLOT_LIB == 'plotly' :
		fig = go.Figure()
	elif PLOT_LIB == 'matplotlib' :
		legend = []

	for i,sym in enumerate(ticker_list) :	
		if NORMALIZED :
			y = history['Close',sym].values/max_vals[sym]
		else :
			y = history['Close',sym].values
		if PLOT_LIB == 'matplotlib' :
			plt.plot(history.index,
			     	 y,
			     	 '.-',
			      	 linewidth=LINE_WIDTH,
			     	 ms=MARKER_SIZE)
			legend.append(sym)
		elif PLOT_LIB == 'plotly' :
			fig.add_trace(go.Scatter(x=history.index,
				                     y=y,
				                     mode='lines+markers',
				                     line=dict(width=4),
				                     text=sym,
				                     name=sym))
		if AVERAGE :
			average = (i*average + y)/(i+1)

	if AVERAGE :
		if PLOT_LIB == 'matplotlib' :
			plt.plot(history.index,average,'k-',linewidth=2.5)
			legend.append('Average')
		elif PLOT_LIB == 'plotly' :
			fig.add_trace(go.Scatter(x=history.index,
				                     y=average,
				                     name='Avg',
				                     text='Avg',
				                     mode='lines'))

	if PLOT_LIB == 'matplotlib' :
		plt.xticks(rotation=45)
		if NORMALIZED :
			plt.ylabel('% of history max')
			plt.ylim([0,1])
		else :
			plt.ylabel('Price')
		plt.legend(legend)
		plt.grid()
		plt.show()
	elif PLOT_LIB == 'plotly' :
		fig.update_yaxes(range=[0,1])
		fig.update_layout(yaxis_title='% of history max',
			              font=dict(size=20))
		"""
		fig.update_layout(title="Plot Title",
                          xaxis_title="x Axis Title",
                          yaxis_title="y Axis Title",
                          font=dict(family="Courier New, monospace",
                                    size=18,
                                    color="#7f7f7f"))
        """
		fig.write_html('out.html',auto_open=True)

if __name__ == '__main__' :
	main()