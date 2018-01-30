import requests
from datetime import datetime
import pandas as pd

def get_price_history(symbol,
                      interval=86400,
                      history='1M'):
    url = 'https://finance.google.com/finance/getprices'

    # Formulate Query
    query = {}
    query.update({'q': symbol})
    query.update({'i': str(interval)})
    query.update({'p': history})

    # Make request
    r = requests.get(url, params=query)

    # Parse the response
    response = r.text.splitlines()
    data = []
    index = []
    basetime = 0
    for i in response :
        ij = i.split(",")
        if ij[0][0] == 'a' :
            basetime = int(ij[0][1:])
            date = basetime
        elif ij[0][0].isdigit():
            date = basetime + int(ij[0])*interval
        else :
            continue
            
        index.append(datetime.fromtimestamp(date))
        data.append([float(ij[4]),
                     float(ij[2]), 
                     float(ij[3]), 
                     float(ij[1]), 
                     int(ij[5])])
    return pd.DataFrame(data, 
                        index=index, 
                        columns=['Open', 'High', 'Low', 'Close', 'Volume'])
