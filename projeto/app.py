from flask import Flask
from dash import Dash
import dash_bootstrap_components as dbc
from dash_bootstrap_templates import load_figure_template


load_figure_template('bootstrap')

server = Flask(__name__)

app = Dash(
    __name__,
    server=server,
    external_stylesheets=[dbc.themes.BOOTSTRAP, dbc.icons.BOOTSTRAP],
    use_pages=True,
    suppress_callback_exceptions=True
)
