import pandas as pd
import json
import plotly
import plotly.express as px

with open('data/geo_countries/data/countries.geojson', 'r') as geojson_file:
    geojson_data = json.load(geojson_file)

def colormap(df:pd.DataFrame, df_loc:str, hover_title:str, color:str):

    custom_color_scale = ['rgb(248, 244, 236)', 'black']
    
    map = px.choropleth(
        data_frame = df,
        geojson = geojson_data,
        locations = df_loc,
        featureidkey = 'properties.ISO_A3',
        color = color,
        scope = 'world',
        custom_data = hover_title,
        color_continuous_scale = custom_color_scale,
        range_color = (df[color].min(), df[color].max()))
    
    map.update_traces(
        hovertemplate = '%{customdata}: %{z}')
    
    map.update_coloraxes(
        colorbar_title = None,
        colorbar_orientation = 'h',
        colorbar_len = 1,
        colorbar_thickness = 5,
        colorbar_yanchor = 'bottom',
        colorbar_y = 0,
        colorbar_tickfont_color = 'rgb(248, 244, 236)')
    
    map.update_layout(
        margin = dict(b = 2, t = 2, l = 5, r = 5),
        geo = dict(showframe = False,
                   bgcolor="rgb(62, 50, 50)"),
        paper_bgcolor="rgba(0, 0, 0, 0)")
    
    return map

def linegraph(df:pd.DataFrame, x:str, y:str|list):
    
    line = px.line(
        data_frame = df,
        x = x,
        y = y,
        color_discrete_sequence = plotly.colors.qualitative.Antique_r,
        log_y = True,
        markers = True)
    
    line.update_traces(
        hovertemplate = 'Year %{x}: %{y}',
        showlegend = False)
    
    line.update_layout(
        plot_bgcolor = "rgb(62, 50, 50)",
        paper_bgcolor = "rgb(62, 50, 50)",
        xaxis_title = None)
    
    line.update_yaxes(title = None,
                      gridcolor = 'black',
                      gridwidth = .5,
                      tickfont_color = 'rgb(248, 244, 236)')
    
    line.update_xaxes(showline = True,
                     tickfont_color = 'rgb(248, 244, 236)',
                     showgrid = False)
    
    return line

def boxplot(df:pd.DataFrame, y:str|list, custom:str):
    
    box = px.box(
        data_frame = df,
        y = y,
        color_discrete_sequence = ['rgb(248, 244, 236)'],
        custom_data = custom,
        points = 'all')
    
    box.update_traces(showlegend = False, hovertemplate = '%{customdata}: %{y}')
    
    box.update_layout(
        plot_bgcolor="rgba(0, 0, 0, 0)",
        paper_bgcolor="rgba(0, 0, 0, 0)")
    
    box.update_yaxes(title = None,
                     gridcolor = 'black',
                     gridwidth = .5,
                     tickfont_color = 'rgb(248, 244, 236)')
    box.update_xaxes(title = None,
                     showline = True,
                     tickfont_color = 'rgb(248, 244, 236)')
    
    return box