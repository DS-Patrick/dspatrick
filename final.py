#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Dec  6 13:25:11 2022

@author: patrick
"""
# import packages

import dash
import numpy as np
from dash import dcc
from dash import html
from dash.dependencies import Input, Output
import plotly.express as px
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.pyplot import figure
import dash_bootstrap_components as dbc
import plotly.graph_objs as go
import plotly.express as px
from dash.dash_table.Format import Group

# set colors
colors = {
    'background': '#D8ECF6',
    'text': '#181C93'
}

stylesheet = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

### pandas dataframe to html table
def generate_table(dataframe, max_rows=20000):
    return html.Table([
        html.Thead(
            html.Tr([html.Th(col) for col in dataframe.columns])
        ),
        html.Tbody([
            html.Tr([
                html.Td(dataframe.iloc[i][col]) for col in dataframe.columns
            ]) for i in range(min(len(dataframe), max_rows))
        ])
    ])

# initialize dash
app = dash.Dash(external_stylesheets=[dbc.themes.BOOTSTRAP])
server = app.server

# create title

app.title = "Metacritic Score vs. User Score over the Years"

game = pd.read_csv("/Users/patrick/Desktop/mc.csv")
game_title = game.name.tolist()
game_release = game.date.tolist()
game_platform = game.platform.tolist()
game_score = game.score.tolist()
game_user = game.userscore.tolist()
userscore = "User Score:"


df = pd.DataFrame(list(zip(game_title, game_release, game_platform, game_score, game_user)),
    columns = ["Title", "Release Date", "Platform", "Metacritic Score", "User Score"])

df['Release Date'] = pd.to_datetime(df['Release Date'], format='%Y-%m-%d')
df['Release Date'] = pd.DatetimeIndex(df['Release Date']).year
#df['Release Date'] = pd.to_datetime(df['Release Date'], format = '%Y')
df = df.loc[df['User Score'] != 'tbd']
df['User Score'] = pd.to_numeric(df['User Score'])

# create year options for dropdown menu
year_options = []
years = df["Release Date"].unique()
years = list(years)
sorted_years = sorted(years)
for year in sorted_years:
    year_options.append({'label':str(year),'value':year})

app.layout = html.Div(style={'backgroundColor': colors['background']}, children=[
    # title
    html.H1('Metacritic Score vs. User Rating over the Years',
        style={
            'textAlign': 'center',
            'color': colors['text']
        }
    ),
    
    # subtitle
    html.Div('MA705 Patrick Park',
        style={
            'textAlign': 'center',
            'color': colors['text']
        }
    ),
    html.Br(),
    html.Div('Metacritic ratings vs. User Scores by Platforms', style={
        'textAlign': 'center',
        'color': colors['text']
    }),
    html.Br(),
    html.Div('Choose the year and see the ratings by each platforms', style={
        'textAlign': 'center',
        'color': colors['text']
    }),
    html.Br(),
    html.Div('Each marker is a game. If you hover over the cursor,', style={
        'textAlign': 'center',
        'color': colors['text']
    }),
    html.Div('you can check the title of the game and the user rating out of 10.', style={
        'textAlign': 'center',
        'color': colors['text']
    }),
    # graph
    dcc.Graph(id='graph'),
    dcc.Dropdown(id='year-picker',options=year_options,value=df['Release Date'].max()),
     
    html.Div('Choose the year to check the ratings', style = {
        'textAlign': 'center',
        'color': colors['text']}),
    html.Br(),
    html.Br(),
    html.Br(),
    html.Div('Below is the list of games which were released in chosen year', style = {
        'textAlign': 'center',
        'color': colors['text']}),    
    html.Div('sorted by the User Rating', style = {
        'textAlign': 'center',
        'color': colors['text']}),
    html.Br(),
    html.Div(id='table')
    
])

# table callback

@app.callback(
    Output("table", "children"),
    Input("year-picker", "value")
)
def update_table(gameyears):
    x = df[df['Release Date'] == (gameyears)].sort_values('User Score', ascending = False)
    return generate_table(x)

# graph callback
@app.callback(Output('graph', 'figure'),
              [Input('year-picker', 'value')])

# update figure
def update_figure(selected_year):
    filtered_df = df[df['Release Date'] == selected_year]
    traces = []
    for platform_name in filtered_df['Platform'].unique():
        df_by_platform = filtered_df[filtered_df['Platform'] == platform_name]
        traces.append(go.Scatter(
            x=df_by_platform['Platform'],
            y=df_by_platform['Metacritic Score'],
            text=df_by_platform['Title'].astype(str) + "   " + df_by_platform['User Score'].astype(str),
            mode='markers',
            opacity=0.7,
            marker={'size': 6},
            name=" "
        ))
    return {
        'data': traces,
        'layout': go.Layout(
            xaxis={'title': 'Gaming Platform'},
            yaxis={'title': 'Metacritic Scores'},
            hovermode='closest'
        )
    }

if __name__ == '__main__':
    app.run_server(debug=True)
    




