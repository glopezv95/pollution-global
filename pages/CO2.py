import dash
from dash import dcc, html, Input, Output, callback
import dash_bootstrap_components as dbc

from data import co2_df
import graphs

dash.register_page(__name__, path = '/co2')

layout = dbc.Container([
    dbc.Row([
        dcc.Dropdown(id = 'co2_year_dropdown',
                         options = co2_df['Year'].unique(),
                         placeholder = 'Select a year to update the map',
                         className = 'dropdown'),
        dbc.Col([
            html.H4(children = 'CO2 Concentrations (mean)'),
            html.H5(id = 'co2_year_id', children = f'{co2_df["Year"].max()}'),
            dcc.Graph(id = 'co2_map_graph',
                      figure = graphs.colormap(df = co2_df[co2_df["Year"] == co2_df["Year"].max()],
                                               df_loc = 'Code',
                                               hover_title = 'Country Name',
                                               color = 'CO2'),
                      className = 'graph')]),
        dbc.Col([
            html.H4(id = 'co2_line_header',
                        children = 'CO2 concentrations through the years'),
            html.H5(id = 'co2_country_id', children = 'Qatar'),
            dcc.Graph(id = 'co2_line_graph',
                      figure = graphs.linegraph(df = co2_df[co2_df['Country Name'] == 'Qatar'],
                                                x = 'Year',
                                                y = 'CO2'))])]),
    html.Link(rel = 'stylesheet', href = 'styles.css')
])

@callback(
    Output('co2_map_graph', 'figure'),
    Output('co2_year_id', 'children'),
    Input('co2_year_dropdown', 'value'))

def update_map(sel_year):
    
    if not sel_year:
        return dash.no_update
    
    dff = co2_df[co2_df['Year'] == sel_year]
    
    fig = graphs.colormap(
        df = dff,
        df_loc = 'Code', 
        hover_title = 'Country Name',
        color = 'CO2')
    
    return fig, f'{sel_year}'

@callback(
    Output('co2_line_graph', 'figure'),
    Output('co2_country_id', 'children'),
    Input('co2_map_graph', 'clickData'))

def update_line_map(data):
    
    if not data:
        return dash.no_update
        
    country = data['points'][0]['customdata'][0]
    dff = co2_df[co2_df['Country Name'] == country]
    
    fig = graphs.linegraph(
        df = dff,
        x = 'Year',
        y = 'CO2')
    
    return fig, f'{country}'