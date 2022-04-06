#This works

import dash
from dash import dcc, html
#import dash_core_components as dcc
#import dash_html_components as html
from dash.dependencies import Input, Output, State
from dash.exceptions import PreventUpdate
from helpers.key_finder import api_key
from helpers.api_call import *

#you can put these imports along with the below "sentiment_scores" function in a separate .py file and them import it
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
import numpy as np


########### Define a few variables ######

tabtitle = 'Movies'
sourceurl = 'https://www.kaggle.com/tmdb/tmdb-movie-metadata'
sourceurl2 = 'https://developers.themoviedb.org/3/getting-started/introduction'
githublink = 'https://github.com/MMartGA99/405-movie-reviews-api'



########### Initiate the app
external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']
app = dash.Dash(__name__, external_stylesheets=external_stylesheets)
server = app.server
app.title=tabtitle

####### Write your primary function here - vader sentiment
def sentiment_scores(sentence):
    sent_keys = ["Negative", "Neutral", "Positive"]
    # Create a SentimentIntensityAnalyzer object.
    sid_obj = SentimentIntensityAnalyzer()

    # polarity_scores method of SentimentIntensityAnalyzer
    # object gives a sentiment dictionary.
    sentiment_dict = sid_obj.polarity_scores(sentence)
    sent_values = [x for x in sentiment_dict.values()]
    sent_values=sent_values[:3]
    # find the index of the max value

    index_max = np.argmax(sent_values)

    # decide sentiment as positive, negative and neutral
    final = sent_keys[index_max]
    # responses
    response1=f"Overall sentiment is {final} with scores: {sentiment_dict}"
    return response1


########### Layout

app.layout = html.Div(children=[
    dcc.Store(id='tmdb-store', storage_type='session'),
    dcc.Store(id='summary-store', storage_type='session'),
    html.Div([
        html.H1(['Movie Reviews']),
        html.Div([
            html.Div([
                html.Div('Randomly select a movie summary'),
                html.Button(id='eek-button', n_clicks=0, children='API call', style={'color': 'rgb(255, 255, 255)'}),
                html.Div(id='movie-title', children=[]),
                html.Div(id='movie-release', children=[]),
                html.Div(id='movie-overview', children=[]),
                

            ], style={ 'padding': '12px',
                    'font-size': '22px',
                    # 'height': '400px',
                    'border': 'thick red solid',
                    'color': 'rgb(255, 255, 255)',
                    'backgroundColor': '#536869',
                    'textAlign': 'left',
                    },
            className='six columns'),

        ], className='twelve columns'),
        html.Br(),

    ], className='twelve columns'),
    html.Br(),
    html.Div(id='output-div-1'), 


        # Output
    html.Div([
        # Footer
        html.Br(),
        html.A('Code on Github', href=githublink, target="_blank"),
        html.Br(),
        html.A("Data Source: Kaggle", href=sourceurl, target="_blank"),
        html.Br(),
        html.A("Data Source: TMDB", href=sourceurl2, target="_blank"),
    ], className='twelve columns'),



    ]
)

########## Callbacks

# TMDB API call
@app.callback(Output('tmdb-store', 'data'),
              [Input('eek-button', 'n_clicks')],
              [State('tmdb-store', 'data')])
def on_click(n_clicks, data):
    if n_clicks is None:
        raise PreventUpdate
    elif n_clicks==0:
        data = {'title':' ', 'release_date':' ', 'overview':' '}
    elif n_clicks>0:
        data = api_pull(random.choice(ids_list))
    return data

@app.callback([Output('movie-title', 'children'),
                Output('movie-release', 'children'),
                Output('movie-overview', 'children'),
               Output(component_id='output-div-1', component_property='children')
                ],
              [Input('tmdb-store', 'modified_timestamp')],
              [State('tmdb-store', 'data')])
def on_data(ts, data):
    if ts is None:
        raise PreventUpdate
    else:
        sentence = data['overview']
        message = sentiment_scores(sentence)
        return data['title'], data['release_date'], data['overview'], message


############ Deploy
if __name__ == '__main__':
    app.run_server(debug=True)

