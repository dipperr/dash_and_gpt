import dash
import openai
from dash import html, callback, Input, Output, State, dash_table, exceptions, ctx, dcc
import dash_bootstrap_components as dbc
import pandas as pd
from flask_caching import Cache
import atexit
from utils import ask_chatgpt
import time


dash.register_page(__name__, path='/assistente_analise')

pd.set_option('display.max_columns', 30)

cache = Cache(
    dash.get_app().server, config={
        'CACHE_TYPE': 'filesystem',
        'CACHE_DIR': 'C:\\Users\\luiz henrique\\Documents\\dash_and_chatgpt\\cache'
    }
)

layout = html.Div(children=[
    dbc.Card([
        dbc.CardBody([
            dbc.Row([
                dbc.Col([
                    dbc.Card([
                        dbc.CardBody([
                            dash_table.DataTable(
                                id='table_assistente',
                                page_action='none',
                                style_table={'height': '500px', 'overflowY': 'auto', 'overflowX': 'auto'}
                            )
                        ]),
                        dbc.CardHeader([html.Div(id='shape_table')])
                    ])
                ])
            ]),
            dbc.Row([
                dbc.Col([
                    dbc.Card([
                        dbc.CardHeader(['Prompt']),
                        dbc.CardBody([
                            dbc.Row([
                                dbc.Col([
                                    dbc.Textarea(
                                        placeholder='Digite Sua Duvida...', rows=8, id='text_area_input_assistente'
                                    )
                                ])
                            ]),
                            dbc.Row([
                                dbc.Col([
                                    dbc.Button(
                                        children=[html.I(className='bi bi-send-fill')], outline=True,
                                        color='primary', id='button_send_assistente'
                                    )
                                ])
                            ], style={'margin-top': '10px'})
                        ])
                    ], style={'height': '100%'}),
                ], md=6),
                dbc.Col([
                    dbc.Card([
                        dbc.CardHeader('Assistente'),
                        dcc.Loading(
                            type='circle',
                            children=dbc.CardBody(id='cardy_body_output_assistente', style={'height': '100%'}),
                            parent_className='loading'
                        )
                    ], style={'height': '100%'})
                ], md=6)
            ], style={'margin-top': '10px'})
        ])
    ]),
])


@cache.memoize(timeout=600)
def read_df():
    dframe = pd.read_csv(
        'C:\\Users\\luiz henrique\\Documents\\dash_and_chatgpt\\data\\dados_marketing_tratado.csv',
        sep=';',
        parse_dates=['Data Cadastro'],
        dayfirst=True
    )
    df_sample = dframe.sample(frac=0.03)

    return df_sample


@callback(
    [
        Output(component_id='table_assistente', component_property='data'),
        Output(component_id='table_assistente', component_property='columns')
    ],
    Input(component_id='route', component_property='pathname')
)
def func(path):
    if path == '/assistente_analise':
        df = read_df()
        columns = [
            {'id': c, 'name': c, 'deletable': True} for c in df.columns
        ]
        return df.to_dict(orient='records'), columns
    else:
        raise exceptions.PreventUpdate


@callback(
    Output(component_id='shape_table', component_property='children'),
    Input(component_id='table_assistente', component_property='data')
)
def func(data):
    _ = pd.DataFrame(data)
    return f'Total de Linhas: {_.shape[0]} Total de Colunas: {_.shape[1]}'


@callback(
    Output(component_id='button_send_assistente', component_property='disabled'),
    Input(component_id='text_area_input_assistente', component_property='value')
)
def func(value):
    if value:
        return False
    else:
        return True


@callback(
    Output(component_id='text_area_input_assistente', component_property='value'),
    Input(component_id='button_send_assistente', component_property='n_clicks')
)
def func(n_click):
    if n_click:
        return ''
    else:
        return ''


@callback(
    Output(component_id='cardy_body_output_assistente', component_property='children'),
    Input(component_id='button_send_assistente', component_property='n_clicks'),
    [
        State(component_id='text_area_input_assistente', component_property='value'),
        State(component_id='table_assistente', component_property='data'),
        State(component_id='table_assistente', component_property='columns')
    ]
)
def func(n_click, value, data, columns):
    if n_click:
        df = pd.DataFrame(data, columns=[column['name'] for column in columns])
        response = ask_chatgpt(value.replace('\n', ' '), df.to_csv(index=False))
        return dbc.Toast(
            [dbc.Textarea(rows=7, value=response, id='text_area_output_assistente')],
            header='Resposta',
            dismissable=True,
            is_open=True,
            id='toast_output_assistente',
            style={'width': '100%'}
        )
    else:
        return html.Div(children=[
            html.Img(src=dash.get_asset_url('robot.png'))
        ], style={
            'height': '100%',
            'display': 'flex',
            'justify-content': 'center',
            'align-items': 'center'
        })


@dash.get_app().callback(
    Output(
        component_id='cardy_body_output_assistente', component_property='children',
        allow_duplicate=True
    ),
    Input(component_id='toast_output_assistente', component_property='is_open'),
    prevent_initial_call=True
)
def func(is_open):
    if not is_open:
        return html.Div(children=[
            html.Img(src=dash.get_asset_url('robot.png'))
        ], style={
            'height': '100%',
            'display': 'flex',
            'justify-content': 'center',
            'align-items': 'center'
        })
    else:
        raise exceptions.PreventUpdate


@atexit.register
def clear_caching():
    cache.clear()
