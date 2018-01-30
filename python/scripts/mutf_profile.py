from finalysis.tools.GFI import get_price_history
from finalysis.tools.EmailUtils import send_gmail
import re
import datetime
import json
import os

def dict_to_html(l, caption=None) :
    if l is None or len(l) == 0 :
        return None

    html = """\
<html>
<head>
<style>
table, th, td {
  border: 1px solid black;
  border-collapse: collapse;
}
th {
  padding: 5px;
  text-align: left;    
}
td {
  padding: 5px;
  text-align: center;
}
</style>
</head>
<body>
<table style="width:100%">
"""
    if caption is not None :
        html += '<caption>' + caption + '</caption>'

    # Construct Header Row
    html += '<tr>'
    for hdr in l[0].keys() :
        html += '<th>'
        html += hdr
        html += '</th>'
    html += '</tr>'

    # Construct each data row
    for dct in l :
        html += '<tr>'
        for k in dct.keys() :
            html += '<td>'
            if re.search('(D|d)ifference', k) and isinstance(dct[k], float) :
                if dct[k] < 0 :
                    html += '<font color="red">' + str(dct[k]) + '</font>'
                else :
                    html += '<font color="green">' + str(dct[k]) + '</font>'
            elif not isinstance(dct[k], str) :
                html += str(dct[k])
            else : # just assumes if not float than must be string
                html += dct[k]
            html += '</td>'
                   
        html += '</tr>'

    # End the table and return
    html += '</table></body></html>'
    return html

def load_params(param_file) :
    f = open(os.environ['FINALYSIS_HOME'] + '/params/' + param_file, 'r')
    params = json.load(f)
    f.close()
    return params

def main(param_file='mutf_profile.json') :
    params = load_params(param_file)
    data = []
    for s in params['symbols'] :
        # Fetch the data from GF
        p_history = get_price_history(s, history='1Y')

        # Set up data structure
        feature_dict = {'Symbol': s}

        # Record Close Price
        close_price = p_history.Close[-1]
        feature_dict.update({'Close Price':close_price})

        # Record the price difference over one day
        one_day_diff = round(p_history.Close[-1] - p_history.Close[-2], 2)
        feature_dict.update({'One Day Difference':one_day_diff})

        # Record the price difference over one month
        one_month_diff = round(p_history.Close[-1] - p_history.Close[0], 2)
        feature_dict.update({'One Year Difference':one_month_diff})

        # Record the "monotonicity measure"
        num_pos_price_diff = (p_history.diff().Close[1:] > 0).sum()
        num_total = p_history.Close.size - 1
        mm = round(num_pos_price_diff/num_total,3)
        feature_dict.update({'Monotonicity Measure':mm})

        # Update the overall collecting data structure
        data.append(feature_dict)

    # Convert data to html string
    html = dict_to_html(data, caption='Price Summary')
    print(html)

    # Send the message out
    subject_line = 'MUTF Price Summary for '
    subject_line += datetime.datetime.now().strftime('%Y-%m-%d')
    send_gmail(subject_line,
               html,
               sender=params['sender'],
               recipients=params['recipients'],
               pw=params['password'])

if __name__ == '__main__' :
    main()
