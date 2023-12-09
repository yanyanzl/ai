
# Learn the basics of the dash and plotly chart tools

from dash import Dash, dcc, html, Input, Output
import plotly.express as px

app = Dash(__name__)


app.layout = html.Div([
    html.H4('Stock price analysis'),
    dcc.Graph(id="time-series-chart"),
    html.P("Select stock:"),
    dcc.Dropdown(
        id="ticker",
        options=["AMZN", "FB", "NFLX", "GOOG", "MSFT", "AAPL"],
        value="AMZN",
        clearable=False,
    ),
])


@app.callback(
    Output("time-series-chart", "figure"), 
    Input("ticker", "value"))
def display_time_series(ticker):
    df = px.data.stocks() # replace with your own data source
    
    # Line Chart
    fig = px.line(df, x='date', y=ticker)

    # Bar Chart
    # fig = px.bar(df, x='date', y=ticker)

    # Area Chart
    # df = px.data.stocks(indexed=True)-1
    # fig = px.area(df, facet_col="company", facet_col_wrap=2)

    fig.update_xaxes(
        dtick="M1",
        tickformat="%b\n%Y",
        ticklabelmode="period")

    fig.update_xaxes(
        rangeslider_visible=True,
        rangeselector=dict(
        buttons=list([
            dict(count=1, label="1m", step="month", stepmode="backward"),
            dict(count=6, label="6m", step="month", stepmode="backward"),
            dict(count=1, label="YTD", step="year", stepmode="todate"),
            dict(count=1, label="1y", step="year", stepmode="backward"),
            dict(step="all")
        ])
        ),
        rangebreaks=[
        dict(bounds=["sat", "mon"]), #hide weekends
        dict(values=["2015-12-25", "2016-01-01"])  # hide Christmas and New Year's
        ]
    )

    fig.update_layout(
    plot_bgcolor='LightSteelBlue',
    paper_bgcolor='lightblue',
    font_color='Orange',
    autosize=True,
    margin=dict(l=20, r=20, t=20, b=20),
    minreducedwidth=250,
    # minreducedheight=2000
    # width=1600,
    height=800,
    )

    print(fig)
    return fig


app.run_server(debug=True)



''' Candle Stick chart
from dash import Dash, dcc, html, Input, Output
import plotly.graph_objects as go
import pandas as pd


app = Dash(__name__)

app.layout = html.Div([
    html.H4('Apple stock candlestick chart'),
    dcc.Checklist(
        id='toggle-rangeslider',
        options=[{'label': 'Include Rangeslider', 
                  'value': 'slider'}],
        value=['slider']
    ),
    dcc.Graph(id="graph"),
])


@app.callback(
    Output("graph", "figure"), 
    Input("toggle-rangeslider", "value"))
def display_candlestick(value):
    df = pd.read_csv('https://raw.githubusercontent.com/plotly/datasets/master/finance-charts-apple.csv') # replace with your own data source
    fig = go.Figure(go.Candlestick(
        x=df['Date'],
        open=df['AAPL.Open'],
        high=df['AAPL.High'],
        low=df['AAPL.Low'],
        close=df['AAPL.Close']
    ))

    fig.update_layout(
        xaxis_rangeslider_visible='slider' in value,
        title='Candle Stick Chart',
        yaxis_title='AAPL Stock Price',
        xaxis_title="date"
    )

    print(fig)

    return fig


app.run_server(debug=True, use_reloader=True)

'''