from bokeh.io import show, output_file
from bokeh.plotting import figure
from bokeh.models import ColumnDataSource, Range1d, FactorRange, DataRange1d
import pandas as pd

output_file("bar_basic.html")

book_fee=0
airline_fee=0
percent_fee=0

df = pd.read_csv("FB - real_exp diff per segment source for bokeh.csv")
df = df.sort_values(by=['diff'], ascending=False)
bid_list = [str(x) for x in df['bid']]
df['real_price'] = [float(str(x).replace(',','')) for x in df['real_price']]
df['expected_price'] = [float(str(x).replace(',','')) for x in df['expected_price']]
df['bid'] = bid_list
df = df.set_index('bid')
new_diffs = []
base_fare = []

for bid in df.index:
    
    diff, pax_number, segments, price, expected_price = df.loc[bid, 'diff'], df.loc[bid,'pax_number'], df.loc[bid,'number_of_segments'], df.loc[bid,'real_price'],df.loc[bid,'expected_price']
    
    bf, af, pf = df['book_fee'][bid], df['airline_fee'][bid], df['fee_percent'][bid]
    diff = diff + (bf*pax_number) + af
    if pf > 0:
        diff=diff + price*(pf/100)
        
    new_diff = diff - ((book_fee*pax_number*segments) + (airline_fee*segments))
    if percent_fee >0:
        new_diff = new_diff - (expected_price*(percent_fee/100))
    new_diff = round(new_diff,2)
    new_diffs.append(new_diff)

df['new_diff'] = new_diffs    
print(df)
sum = round(df['diff'].sum(),0)
new_sum = round(df['new_diff'].sum(),0)

if df['new_diff'].max() > df['diff'].max():
    limit = df['new_diff'].max()
else:
    limit = df['diff'].max()

source = ColumnDataSource(df)

TOOLS = "pan,wheel_zoom,reset,hover,save"
TOOLTIPS = [("BID", "@bid"),("Diff", "@diff"), ('New diff', '@new_diff'),
            ('Number of segments','@number_of_segments'), ('Number of passengers','@pax_number'),('Book fee', '@book_fee')]



p = figure(x_range=FactorRange(factors=bid_list, bounds='auto'), y_range = DataRange1d(bounds =(-limit,limit)), plot_height=1000, width=1500,
           title="real/exp sum = {0} after fee recalculation = {1}".format(sum, new_sum),
           toolbar_location=None, tools=TOOLS, tooltips=TOOLTIPS)

p.xaxis.major_label_orientation = "vertical"
p.vbar(x='bid', top='diff', width=0.9, alpha= 0.2, color='blue',source=source)
p.vbar(x='bid', top='new_diff', width=0.9, alpha= 0.3, color='red',source=source)
p.xgrid.grid_line_color = None
p.y_range.start = -limit
p.hover.point_policy = "follow_mouse"

show(p)
