import dash
from dash import dcc, html, Input, Output, callback, dash_table
import dash_bootstrap_components as dbc

from data import weather_df
import graphs

dash.register_page(__name__, path = '/')

layout = dbc.Container([
    dbc.Row([
        dcc.Dropdown(id = 'weather_dropdown',
                              options = weather_df.columns[7:-10],
                              placeholder = 'Select a variable to update the map',
                              className = 'dropdown'),
        dbc.Col([
            html.H4(children = 'Air quality 08/2023 - 10/2023 (mean)'),
            html.H5(id = 'weather_map_id', children = 'O3'),
            dcc.Graph(id = 'weather_map_graph',
                      figure = graphs.colormap(df = weather_df\
                          .groupby('Code')[weather_df.columns[7:-10]].mean().reset_index(),
                                               df_loc = 'Code',
                                               hover_title = 'Code',
                                               color = 'O3'),
                      className = 'graph')]),
        dbc.Col([
            html.H4(children = 'Weather variables distribution (Z normalized)'),
            html.H5(id = 'weather_vars_id', children = 'ARE'),
            dcc.Graph(id = 'weather_box',
                      figure = graphs.boxplot(df = weather_df[weather_df['Code'] == 'ARE'],
                                              y = weather_df.columns[-7:-1],
                                              custom = 'date'))
            
])])])

@callback(
    Output('weather_map_graph', 'figure'),
    Output('weather_map_id', 'children'),
    Input('weather_dropdown', 'value'))

def update_map(sel_weather):
    
    if not sel_weather:
        return dash.no_update
    
    map = graphs.colormap(
        df = weather_df.groupby('Code')[weather_df.columns[7:-10]].mean().reset_index(),
        df_loc = 'Code', 
        hover_title = 'Code',
        color = sel_weather)
    
    return map, sel_weather

@callback(
    Output('weather_box', 'figure'),
    Output('weather_vars_id', 'children'),
    Input('weather_map_graph', 'clickData'))

def update_line_map(data):
    
    if not data:
        return dash.no_update
        
    country = data['points'][0]['customdata'][0]
    dff = weather_df[weather_df['Code'] == country]
    
    fig = graphs.boxplot(df = weather_df[weather_df['Code'] == country],
                         y = weather_df.columns[-7:-1],
                         custom = 'date')
    
    return fig, country