import dash
from dash import dcc, html, Input, Output, callback
import dash_bootstrap_components as dbc

from data import death_df
import graphs

dash.register_page(__name__, path = '/deaths')

layout = dbc.Container([
    dbc.Row([
        dbc.Col([
            dcc.Dropdown(id = 'year_dropdown',
                         options = death_df['Year'].unique(),
                         placeholder = 'Select a year to update the map',
                         className = 'dropdown'),
            html.H4(children = 'Total air pollution deaths per 100.000 inhabitants'),
            html.H5(id = 'year_id', children = f'{death_df["Year"].max()}'),
            dcc.Graph(id = 'death_map_graph',
                      figure = graphs.colormap(df = death_df[death_df["Year"] == death_df["Year"].max()],
                                               df_loc = 'Code',
                                               hover_title = 'Entity',
                                               color = 'Air pollution (total) (deaths per 100,000)'),
                      className = 'graph')]),
        dbc.Col([
            dcc.Dropdown(id = 'line_dropdown',
                         options = death_df.columns[3:6],
                         multi = True,
                         placeholder = 'Select a variable to update the line graph',
                         className = 'dropdown'),
            html.H4(id = 'line_header',
                        children = 'Pollution deaths through the years'),
            html.H5(id = 'country_id', children = 'Papua New Guinea'),
            dcc.Graph(id = 'line_graph',
                      figure = graphs.linegraph(df = death_df[death_df['Entity'] == 'Papua New Guinea'],
                                                x = 'Year',
                                                y = ['Indoor air pollution (deaths per 100,000)',
                                                     'Outdoor particulate matter (deaths per 100,000)',
                                                     'Outdoor ozone pollution (deaths per 100,000)']))])]),
    html.Link(rel = 'stylesheet', href = 'styles.css')
])

@callback(
    Output('death_map_graph', 'figure'),
    Output('year_id', 'children'),
    Input('year_dropdown', 'value'))

def update_map(sel_year):
    
    if not sel_year:
        return dash.no_update
    
    dff = death_df[death_df['Year'] == sel_year]
    
    fig = graphs.colormap(
        df = dff,
        df_loc = 'Code', 
        hover_title = 'Entity',
        color = 'Air pollution (total) (deaths per 100,000)')
    
    return fig, f'{sel_year}'

@callback(
    Output('line_graph', 'figure'),
    Output('country_id', 'children'),
    Input('death_map_graph', 'clickData'),
    Input('line_dropdown', 'value'))

def update_line_map(data, value_list):
    
    if not data:
        
        if not value_list:
            return dash.no_update
        
        fig = graphs.linegraph(
        df = death_df[death_df['Entity'] == 'Papua New Guinea'],
        x = 'Year',
        y = value_list)
        
        return fig, 'Papua New Guinea'
        
    country = data['points'][0]['customdata'][0]
    dff = death_df[death_df['Entity'] == country]
    
    fig = graphs.linegraph(
        df = dff,
        x = 'Year',
        y = ['Indoor air pollution (deaths per 100,000)',
            'Outdoor particulate matter (deaths per 100,000)',
            'Outdoor ozone pollution (deaths per 100,000)'])
    
    if not value_list:
    
        return fig, f'{country}'
    
    fig = graphs.linegraph(
        df = dff,
        x = 'Year',
        y = value_list)
    
    return fig, f'{country}'