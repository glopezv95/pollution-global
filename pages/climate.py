import dash
from dash import dcc, html, Input, Output, callback, dash_table
import dash_bootstrap_components as dbc

from data import climate_df
import graphs

dash.register_page(__name__, path = '/')

layout = dbc.Container([
    dbc.Row([
        dcc.Dropdown(id = 'climate_dropdown',
                              options = climate_df.columns[7:-10],
                              placeholder = 'Select a variable to update the map',
                              className = 'dropdown'),
        dbc.Col([
            html.H4(children = 'Air quality 08/2023 - 10/2023 (mean)'),
            html.H5(id = 'climate_map_id', children = 'O3'),
            dcc.Graph(id = 'climate_map_graph',
                      figure = graphs.colormap(df = climate_df\
                          .groupby('Code')[climate_df.columns[7:-10]].mean().reset_index(),
                                               df_loc = 'Code',
                                               hover_title = 'Code',
                                               color = 'O3'),
                      className = 'graph')]),
        dbc.Col([
            html.H4(children = 'Climate variables distribution (Z normalized)'),
            html.H5(id = 'climate_vars_id', children = 'ARE'),
            dcc.Graph(id = 'climate_box',
                      figure = graphs.boxplot(df = climate_df[climate_df['Code'] == 'ARE'],
                                              y = climate_df.columns[-7:-1],
                                              custom = 'date'))
            
])])])

@callback(
    Output('climate_map_graph', 'figure'),
    Output('climate_map_id', 'children'),
    Input('climate_dropdown', 'value'))

def update_map(sel_climate):
    
    if not sel_climate:
        return dash.no_update
    
    map = graphs.colormap(
        df = climate_df.groupby('Code')[climate_df.columns[7:-10]].mean().reset_index(),
        df_loc = 'Code', 
        hover_title = 'Code',
        color = sel_climate)
    
    return map, sel_climate

@callback(
    Output('climate_box', 'figure'),
    Output('climate_vars_id', 'children'),
    Input('climate_map_graph', 'clickData'))

def update_line_map(data):
    
    if not data:
        return dash.no_update
        
    country = data['points'][0]['customdata'][0]
    dff = climate_df[climate_df['Code'] == country]
    
    fig = graphs.boxplot(df = climate_df[climate_df['Code'] == country],
                         y = climate_df.columns[-7:-1],
                         custom = 'date')
    
    return fig, country