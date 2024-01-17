import dash
from dash import Dash, html
import dash_bootstrap_components as dbc

app = dash.Dash(__name__, external_stylesheets = [dbc.themes.BOOTSTRAP],
                use_pages = True)

dash.page_registry.values()

app.layout = dbc.Container([
    
    html.H1('Global environmental variables'),
    
    dbc.Nav(className = 'nav',
            children = [
                dbc.NavItem(dbc.NavLink('Climate variables',
                                        href = '/',
                                        active = 'exact')),
                dbc.NavItem(dbc.NavLink('CO2 distribution',
                                        href = '/co2',
                                        active = 'exact')),
                dbc.NavItem(dbc.NavLink('Deaths by pollution',
                                        href = '/deaths',
                                        active = 'exact'))],
            justified = True,
            pills = True),
    
    dash.page_container
    ])

if __name__ == '__main__':
    app.run(debug = True)