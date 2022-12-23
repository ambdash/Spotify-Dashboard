from dash import html
from dash import dcc
import plotly.express as px
from dash.dependencies import Input, Output
import plotly.graph_objs as go

import config as cfg
from data import *
from application import app

''' LAYOUT '''
layout = html.Div([
    html.Div([
        html.Div([
            html.Img(src=app.get_asset_url('Spotify_Logo_RGB_Green.png'),
                     id='logo',
                     style={
                         "height": "70px",
                         "width": "auto",
                         "margin-bottom": "5px",
                     },
                     )
        ],
            className="one-third column",
        ),
        html.Div([
            html.Div([
                html.H2("Spotify Popular Songs 1999–2019",
                        style={"margin-bottom": "20px", 'color': cfg.COLORS['green']}),
                html.H5("Analysis of tracks, song features and artists by genre",
                        style={"margin-top": "20px", 'color': 'white', 'font-family': 'Gotham-b'}),
            ])
        ], className="one-half column", id="title"),
    ], id="header", className="row flex-display", style={"margin-bottom": "25px"}),

    html.Div([
        html.Div([
            html.H6(children='Total Tracks',
                    style=cfg.CARD_TITLE_STYLE
                    ),

            html.P(f"{n_tracks}",
                   style=cfg.CARD_VALUE_STYLE
                   ),
        ], className="card_container three columns",
        ),
        html.Div([
            html.H6(children='Total Duration',
                    style=cfg.CARD_TITLE_STYLE
                    ),

            html.P(f"{duration} min",
                   style=cfg.CARD_VALUE_STYLE
                   ),
        ], className="card_container three columns",
        ),
        html.Div([
            html.H6(children='Total Artists',
                    style=cfg.CARD_TITLE_STYLE
                    ),

            html.P(f"{n_artists}",
                   style=cfg.CARD_VALUE_STYLE
                   ),
        ], className="card_container three columns",
        ),
        html.Div([
            html.H6(children='Total Genres',
                    style=cfg.CARD_TITLE_STYLE
                    ),

            html.P(f"{n_genres}",
                   style=cfg.CARD_VALUE_STYLE
                   ),
        ], className="card_container three columns",
        ),
    ], className="row flex-display"),
    html.Div([
        html.Div([
            dcc.Graph(id='bar_chart_art',
                      config={'displayModeBar': True}),
        ], className="card_container six columns"),
        html.Div([
            dcc.Graph(id='bar_chart_songs',
                      config={'displayModeBar': True}),
        ], className="card_container six columns"),
    ], className="row flex-display"),
    html.Div([

        html.P('Select Year:', className='fix_label', style={'color': cfg.COLORS['green'], 'font-family': 'Gotham-b'}),

        dcc.RangeSlider(id='select_years',
                        min=min_year,
                        max=max_year,
                        step=1,
                        dots=True,
                        marks={i: {'label': str(i), 'style': {'color': 'white'}} for i in
                               range(min_year, max_year + 1)},
                        value=[1999, 2019], className='dcc_compon')
    ], className="eleven columns", id="cross-filter-options"),

    html.Div([
        html.Div([
            html.P('Select Genre:', className='fix_label',
                   style={'color': cfg.COLORS['green'], 'font-family': 'Gotham-b'}),
            dcc.Dropdown(
                id='genres_multiple_dropdown',
                placeholder='Select Genre',
                options=[{'label': k, 'value': k} for k in unique_genres],
                value=['pop', 'hip hop'],  # default value to show
                multi=True,
                searchable=False, className="custom-dropdown"),
        ], className="eleven columns"),
    ], className="row flex-display"),

    html.Div([
        html.Div([
            dcc.Graph(id='line_genre',
                      config={'displayModeBar': True}),
        ], className="card_container six columns"),
        html.Div([
            dcc.Graph(id='line_md',
                      config={'displayModeBar': True}),
        ], className="card_container six columns"),
    ], className="row flex-display"),

    html.Div([
        html.Div([
            html.H6(children='Description',
                    style={
                        'textAlign': 'center',
                        'color': cfg.COLORS['green'],
                        'fontSize': 24,
                        'font-family': 'Gotham-b'}
                    ),

            dcc.Markdown('''
           * Danceability: how suitable a track is for dancing based on a combination of
          musical elements including tempo, rhythm stability, beat strength, and overall regularity (0.0-1.0) 
          * Valence: the musical positiveness conveyed by a track. Tracks with high 
          valence sound more positive (0.0-1.0)
          * Energy: perceptual measure of intensity and activity (0.0-1.0)
          * Tempo: speed or pace of a given piece and derives directly from the average beat duration, 
          estimated in BPM (24-200+)
          * Explicit: lyrics of a song contain criteria offensive or unsuitable for children
          ''',
                         style={
                             'textAlign': 'left',
                             'color': 'white',
                             'fontSize': 15,
                             'font-family': 'Gotham-M'
                         }
                         ),
        ], className="description_container four columns"),
        html.Div([
            dcc.Graph(id='scatter_plot_dance',
                      config={'displayModeBar': True})
        ], className="card_container four columns"),
        html.Div([
            dcc.Graph(id='scatter_plot_valence',
                      config={'displayModeBar': True})
        ], className="card_container four columns"),

    ], className="row flex-display"),
    html.Div([
        html.Div([
            dcc.Graph(id='pie_chart',
                      config={'displayModeBar': 'hover'}),
        ], className="card_container four columns"),
        html.Div([
            dcc.Graph(id='scatter_plot_energy',
                      config={'displayModeBar': True})
        ], className="card_container four columns"),
        html.Div([
            dcc.Graph(id='scatter_plot_tempo',
                      config={'displayModeBar': True})
        ], className="card_container four columns"),

    ], className="row flex-display"),
], id="mainContainer",
    style=cfg.PAGE_STYLE)

''' CALLBACKS'''


# genres occurrences over the years
@app.callback(Output('line_genre', 'figure'),
              [Input('genres_multiple_dropdown', 'value')
               ])
def update_genre(genres_multiple_dropdown):
    line_genre = go.Figure()
    line_genre.update_layout({
        'plot_bgcolor': cfg.COLORS['black'],
        'paper_bgcolor': cfg.COLORS['black'],
        'font_family': "Gotham-b",
        'font_color': "white",
        'font': {'size': 14},
        'xaxis': {'title': 'Year', 'visible': True, 'showticklabels': True},
        'yaxis': {'title': 'Number of Songs', 'visible': True, 'showticklabels': True},
        'title': 'Tracks Per Year by Genre',
        'xaxis_showgrid': False,
        'yaxis_showgrid': False,
        'title_x': 0.5
    })
    line_genre.update_xaxes(cfg.X_AXES_STYLE)
    line_genre.update_yaxes(cfg.X_AXES_STYLE)

    for i in genres_multiple_dropdown:
        df_genre = df[df.isin([i]).any(axis=1)].groupby('year')[['genre']].count().reset_index(level='year')
        line_genre.add_trace(go.Scatter(x=df_genre['year'], y=df_genre['genre'], name=i,
                                        line={'color': cfg.COLORS[i]}))
    return line_genre


@app.callback(Output('line_md', 'figure'),
              [Input('genres_multiple_dropdown', 'value')]
              )
def update_graph_md(genres_multiple_dropdown):
    # mean track duration over the years
    line_md = go.Figure()
    line_md.update_layout({
        'plot_bgcolor': cfg.COLORS['black'],
        'paper_bgcolor': cfg.COLORS['black'],
        'font_family': "Gotham-b",
        'font_color': "white",
        'font': {'size': 14},
        'xaxis': {'title': 'Year', 'visible': True, 'showticklabels': True},
        'yaxis': {'title': 'Minutes', 'visible': True, 'showticklabels': True},
        'title': 'Average Tracks Duration',
        'xaxis_showgrid': False,
        'yaxis_showgrid': False,
        'title_x': 0.5
    })
    for i in genres_multiple_dropdown:
        df_md = df[df.isin([i]).any(axis=1)].groupby('year')[['duration_min']].mean().reset_index(level='year').round(2)
        line_md.add_trace(go.Scatter(x=df_md['year'], y=df_md['duration_min'], name=i,
                                     line={'color': cfg.COLORS[i]}))
    line_md.update_xaxes({'tickfont': {'size': 12, 'family': 'Gotham-M'},
                          'titlefont': {'size': 12, 'family': 'Gotham-M'},
                          'tick0': 2000,
                          'dtick': 5})
    line_md.update_yaxes(cfg.X_AXES_STYLE)
    return line_md


@app.callback(Output('pie_chart', 'figure'),
              [
                  Input('select_years', 'value'),
                  Input('genres_multiple_dropdown', 'value')
              ])
def update_graph(select_years, genres_multiple_dropdown):
    df_expl = df[df.isin(genres_multiple_dropdown).any(axis=1)].groupby(['explicit', 'year'])['artist'].count() \
        .reset_index(level=['explicit', 'year'])

    explicit_0 = df_expl[(df_expl['year'] >= select_years[0]) & (df_expl['year'] <= select_years[1])
                         & (df_expl['explicit'] == False)].iloc[0, -1]
    explicit_1 = df_expl[(df_expl['year'] >= select_years[0]) & (df_expl['year'] <= select_years[1])
                         & (df_expl['explicit'] == True)].iloc[0, -1]
    colors = [cfg.COLORS['green'], 'white']

    return {
        'data': [go.Pie(labels=['Explicit', 'Not Explicit'],
                        values=[explicit_1, explicit_0],
                        marker=dict(colors=colors),
                        hoverinfo='label+value+percent',
                        textinfo='percent',
                        textfont=dict(size=13),
                        hole=.6,
                        rotation=45,
                        )],

        'layout': go.Layout(
            plot_bgcolor=cfg.COLORS['black'],
            paper_bgcolor=cfg.COLORS['black'],
            hovermode='closest',
            title={
                'text': 'Explicit Content',
                'y': 0.93,
                'x': 0.5,
                'xanchor': 'center',
                'yanchor': 'top'},
            titlefont={
                'family': 'Gotham-b',
                'color': 'white',
                'size': 20},
            legend={
                'orientation': 'h',
                'bgcolor': cfg.COLORS['black'],
                'xanchor': 'center', 'x': 0.5, 'y': -0.07},
            font=dict(
                family='Gotham-M',
                size=13,
                color=cfg.COLORS['grey'])
        ),

    }


@app.callback(
    Output('bar_chart_art', 'figure'),
    [Input('select_years', 'value'),
     Input('genres_multiple_dropdown', 'value')]
)
def update_popular_artists(select_years, genres_multiple_dropdown):
    df_popular_artists = df[(df.isin(genres_multiple_dropdown).any(axis=1)) &
                            (df['year'] >= select_years[0]) &
                            (df['year'] <= select_years[1])
                            ].groupby(['artist'])['song'].count(). \
        sort_values(ascending=False).reset_index(
        level=['artist'])
    bar_chart_artists = px.bar(df_popular_artists.head(7),
                               x='song',
                               y='artist',
                               text_auto=True,
                               opacity=1,
                               orientation='h',
                               title='Most Popular Artists'
                               )
    bar_chart_artists.update_traces(textfont_color='white', textfont_size=16,
                                    textangle=0, textposition="outside",
                                    cliponaxis=True, marker_color=cfg.COLORS['green'])
    bar_chart_artists.update_layout({
        'plot_bgcolor': cfg.COLORS['black'],
        'paper_bgcolor': cfg.COLORS['black'],
        'font_family': "Gotham-b",
        'font_color': "white",
        'font': {'size': 14},
        'xaxis': {'title': 'Number of Songs', 'visible': True, 'showticklabels': False},
        'yaxis': {'title': None, 'visible': True, 'showticklabels': True, 'autorange': 'reversed'},
        'xaxis_showgrid': False,
        'yaxis_showgrid': False,
        'title_x': 0.5
    })
    bar_chart_artists.update_xaxes(cfg.X_AXES_STYLE)
    bar_chart_artists.update_yaxes(cfg.X_AXES_STYLE)
    return bar_chart_artists


@app.callback(
    Output('bar_chart_songs', 'figure'),
    [Input('select_years', 'value'),
     Input('genres_multiple_dropdown', 'value')]
)
def update_popular_songs(select_years, genres_multiple_dropdown):
    sorted_df_songs = df.sort_values(['popularity'], ascending=False)
    bar_chart_songs = px.bar(sorted_df_songs[(sorted_df_songs['year'] >= select_years[0]) &
                                             (sorted_df_songs['year'] <= select_years[1]) &
                                             ((sorted_df_songs['genre_0'].isin(genres_multiple_dropdown))
                                              | (sorted_df_songs['genre_1'].isin(genres_multiple_dropdown))
                                              | (sorted_df_songs['genre_2'].isin(genres_multiple_dropdown))
                                              | (sorted_df_songs['genre_3'].isin(genres_multiple_dropdown)))].head(7),
                             y='artist_track',
                             x='popularity',
                             text_auto='.2s',
                             opacity=1,
                             orientation='h',
                             title='Most Popular Songs'
                             )
    bar_chart_songs.update_traces(textfont_color='white', textfont_size=12,
                                  textfont_family='Gotham-b',
                                  textangle=0, textposition="outside",
                                  cliponaxis=True, marker_color=cfg.COLORS['green'])
    bar_chart_songs.update_layout({
        'plot_bgcolor': cfg.COLORS['black'],
        'paper_bgcolor': cfg.COLORS['black'],
        'font_family': "Gotham-b",
        'font_color': "white",
        'font': {'size': 14},
        'xaxis': {'title': 'Song Popularity', 'visible': True, 'showticklabels': False, 'constraintoward': 'left'},
        'yaxis': {'title': None,
                  'visible': True,
                  'showticklabels': True,
                  'autorange': 'reversed',
                  'tickfont': dict(size=10)},
        'xaxis_showgrid': False,
        'yaxis_showgrid': False,
        'title_x': 0.5
    })
    bar_chart_songs.update_xaxes(cfg.X_AXES_STYLE)
    bar_chart_songs.update_yaxes(cfg.Y_AXES_STYLE)
    return bar_chart_songs


@app.callback([Output('scatter_plot_dance', 'figure'),
               Output('scatter_plot_valence', 'figure'),
               Output('scatter_plot_energy', 'figure'),
               Output('scatter_plot_tempo', 'figure')],
              [Input('select_years', 'value'),
               Input('genres_multiple_dropdown', 'value')])
def generate_graphs(select_years, genres_multiple_dropdown):
    characteristics = ['danceability', 'valence', 'energy', 'tempo']
    title_gr = ['Danceability/Popularity', 'Valence/Popularity', 'Energy/Popularity', 'Tempo/Popularity']
    df_filtered = df[(df['year'] >= select_years[0]) &
                     (df['year'] <= select_years[1]) &
                     (df['popularity'] > 10) &
                     ((df['genre_0'].isin(
                         genres_multiple_dropdown))
                      | (df['genre_1'].isin(
                                 genres_multiple_dropdown))
                      | (df['genre_2'].isin(
                                 genres_multiple_dropdown))
                      | (df['genre_3'].isin(
                                 genres_multiple_dropdown)))]

    def fstr(text, **kwargs):
        return eval(f"f'{text}'", kwargs)

    graphs = []
    for m, j in enumerate(characteristics):
        el = j[:3]
        user_input = r"fig_{element}"
        graphs.append(fstr(user_input, element=el))

        graphs[m] = px.scatter(df_filtered,
                               x='popularity',
                               y=characteristics[m],
                               title=title_gr[m])
        graphs[m].update_traces(textfont_color='white', textfont_size=5,
                                textposition='top left',
                                marker_color=cfg.COLORS['green'])
        graphs[m].update_layout({
            'plot_bgcolor': cfg.COLORS['black'],
            'paper_bgcolor': cfg.COLORS['black'],
            'font_family': "Gotham-b",
            'font_color': "white",
            'font': {'size': 14},
            'xaxis': {'visible': True, 'showticklabels': True},
            'yaxis': {'visible': True, 'showticklabels': True},
            'xaxis_showgrid': False,
            'yaxis_showgrid': False,
            'title_x': 0.5
        })
        graphs[m].update_xaxes(cfg.X_AXES_STYLE)
        graphs[m].update_yaxes(cfg.Y_AXES_STYLE)
    return graphs[0], graphs[1], graphs[2], graphs[3]
