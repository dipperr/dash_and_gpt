import dash
from dash import html, dcc, Input, Output, State, callback, exceptions, ctx
import dash_bootstrap_components as dbc
import plotly.graph_objects as go
import plotly.express as px
import pandas as pd
import numpy as np
import logging
import json

from utils import (
    response_modal_prompt_narrative,
    save_json_prompt,
    modal_historic_narrative,
    create_false_narrative,
    create_narrative,
    Graphs
)


dash.register_page(__name__, path='/visao_comportamento')


layout = html.Div(children=[
    dbc.Card([
        dbc.CardBody([
            dbc.Row([
                dbc.Col([
                    dbc.Card([
                        dbc.CardHeader([
                            dbc.Row([
                                dbc.Col([
                                    html.Label('Total de Gasto X Salário Anual')
                                ], md=10),
                                dbc.Col([
                                    dbc.DropdownMenu([
                                        dbc.DropdownMenuItem(
                                            'Criar Narrativa', n_clicks=0,
                                            id='create_narrative_gasto_salario_anual'
                                        ),
                                        dbc.DropdownMenuItem(
                                            'Editar Prompt de Narrativa', n_clicks=0,
                                            id='edit_prompt_narrative_gasto_salario_anual'
                                        ),
                                        dbc.DropdownMenuItem(
                                            'Historico de Narrativa', n_clicks=0,
                                            id='historico_narrative_salario_gasto_anual'
                                        ),
                                        dbc.DropdownMenuItem(
                                            'Caixa de Narrativa', n_clicks=0,
                                            id='caixa_narrativa_gasto_salario_anual'
                                        )
                                    ], label='Menu')
                                ], md=2)
                            ])
                        ]),
                        dbc.CardBody([
                            dbc.Row([
                                dbc.Col([dbc.RadioItems(
                                    options=[
                                        {'label': 'Linear', 'value': 0},
                                        {'label': 'Log', 'value': 1}
                                    ], value=0, inline=True, id='radio_linear_log'
                                )])
                            ]),
                            dbc.Row([
                                dbc.Col([dcc.Graph(id='graph_gasto_e_salario_anual')])
                            ], style={'margin-top': '10px'})
                        ]),
                        dbc.CardFooter([
                            dcc.Loading(
                                type='dot',
                                children=[
                                    dbc.Toast(
                                        children=[
                                            dbc.Textarea(
                                                className="mb-3", size='md', rows=10, id='text_area_gasto_salario_anual'
                                            )
                                        ],
                                        header='Narrativa', dismissable=True, style={'width': '100%'},
                                        is_open=False, id='toast_narrative_gasto_salario_anual'
                                    )
                                ], color='#636EFA', style={'margin-top': '5px'}
                            )
                        ])
                    ])
                ], md=6),
                dbc.Col([
                    dbc.Card([
                        dbc.CardHeader([
                            dbc.Row([
                                dbc.Col([
                                    html.Label('Total Gasto por Escolaridade e Estado Civil')
                                ], md=10),
                                dbc.Col([
                                    dbc.DropdownMenu([
                                        dbc.DropdownMenuItem(
                                            'Criar Narrativa', n_clicks=0, id='create_narrative_gasto_esco_civil'
                                        ),
                                        dbc.DropdownMenuItem(
                                            'Editar Prompt de Narrativa', n_clicks=0,
                                            id='edit_prompt_narrative_gasto_esco_civil'
                                        ),
                                        dbc.DropdownMenuItem(
                                            'Historico de Narrativa', n_clicks=0,
                                            id='historico_narrative_gasto_esco_civil'
                                        ),
                                        dbc.DropdownMenuItem(
                                            'Caixa de Narrativa', n_clicks=0, id='caixa_narrativa_gasto_esco_civil'
                                        )
                                    ], label='Menu')
                                ], md=2)
                            ])
                        ]),
                        dbc.CardBody([dcc.Graph(id='graph_gasto_escolaridade_civil')]),
                        dbc.CardFooter([
                            dcc.Loading(
                                type='dot',
                                children=[
                                    dbc.Toast(
                                        children=[
                                            dbc.Textarea(
                                                className="mb-3", size='md', rows=10, id='text_area_gasto_esco_civil'
                                            )
                                        ],
                                        header='Narrativa', dismissable=True, style={'width': '100%'},
                                        is_open=False, id='toast_narrative_gasto_esco_civil'
                                    )
                                ], color='#636EFA', style={'margin-top': '5px'}
                            )
                        ])
                    ])
                ], md=6)
            ]),
            dbc.Row([
                dbc.Col([
                    dbc.Card([
                        dbc.CardHeader([
                            dbc.Row([
                                dbc.Col([
                                    html.Label('Total Gasto X Filhos em Casa')
                                ], md=10),
                                dbc.Col([
                                    dbc.DropdownMenu([
                                        dbc.DropdownMenuItem(
                                            'Criar Narrativa', n_clicks=0, id='create_narrative_gasto_filhos_casa'
                                        ),
                                        dbc.DropdownMenuItem(
                                            'Editar Prompt de Narrativa', n_clicks=0,
                                            id='edit_prompt_narrative_gasto_filhos_casa'
                                        ),
                                        dbc.DropdownMenuItem(
                                            'Historico de Narrativa', n_clicks=0,
                                            id='historico_narrative_gasto_filhos_casa'
                                        ),
                                        dbc.DropdownMenuItem(
                                            'Caixa de Narrativa', n_clicks=0, id='caixa_narrativa_gasto_filhos_casa'
                                        )
                                    ], label='Menu')
                                ], md=2)
                            ])
                        ]),
                        dbc.CardBody([dcc.Graph(id='graph_total_gastos_filhos')]),
                        dbc.CardFooter([
                            dcc.Loading(
                                type='dot',
                                children=[
                                    dbc.Toast(
                                        children=[
                                            dbc.Textarea(
                                                className="mb-3", size='md', rows=10, id='text_area_gasto_filhos_casa'
                                            )
                                        ],
                                        header='Narrativa', dismissable=True, style={'width': '100%'},
                                        is_open=False, id='toast_narrative_gasto_filhos_casa'
                                    )
                                ], color='#636EFA', style={'margin-top': '5px'}
                            )
                        ])
                    ])
                ], md=6),
                dbc.Col([
                    dbc.Card([
                        dbc.CardHeader([
                            dbc.Row([
                                dbc.Col([
                                    html.Label('Total Gasto X Adolescentes em Casa')
                                ], md=10),
                                dbc.Col([
                                    dbc.DropdownMenu([
                                        dbc.DropdownMenuItem(
                                            'Criar Narrativa', n_clicks=0, id='create_narrative_gasto_adolescentes_casa'
                                        ),
                                        dbc.DropdownMenuItem(
                                            'Editar Prompt de Narrativa', n_clicks=0,
                                            id='edit_prompt_narrative_gasto_adolescentes_casa'
                                        ),
                                        dbc.DropdownMenuItem(
                                            'Historico de Narrativa', n_clicks=0,
                                            id='historico_narrative_gasto_adolescentes_casa'
                                        ),
                                        dbc.DropdownMenuItem(
                                            'Caixa de Narrativa', n_clicks=0,
                                            id='caixa_narrativa_gasto_adolescentes_casa'
                                        )
                                    ], label='Menu')
                                ], md=2)
                            ])
                        ]),
                        dbc.CardBody([dcc.Graph(id='graph_total_gasto_adolescente')]),
                        dbc.CardFooter([
                            dcc.Loading(
                                type='dot',
                                children=[
                                    dbc.Toast(
                                        children=[
                                            dbc.Textarea(
                                                className="mb-3", size='md', rows=10,
                                                id='text_area_gasto_adolescentes_casa'
                                            )
                                        ],
                                        header='Narrativa', dismissable=True, style={'width': '100%'},
                                        is_open=False, id='toast_narrative_gasto_adolescentes_casa'
                                    )
                                ], color='#636EFA', style={'margin-top': '5px'}
                            )
                        ])
                    ])
                ], md=6)
            ], style={'margin-top': '10px'})
        ])
    ]),
    dbc.Modal([
        dbc.ModalHeader('Editar Prompt da Narrativa'),
        dbc.ModalBody([
            dbc.Textarea(
                className="mb-3", placeholder="A Textarea", id='textarea_edit_prompt_narrative_gasto_salario_anual',
                size='md', rows=3
            ),
            html.Div(id='table_edit_narrative_gasto_salario_anual', style={'margin-top': '15px'}),
            html.Div(
                dbc.Button('Salvar', color='success', n_clicks=0, id='button_save_narrative_gasto_salario_anual'),
                style={'margin-top': '15px'}
            )
        ]),
        dbc.ModalFooter([
            html.Div(id='alert_edit_narrative_gasto_salario_anual')
        ], style={'justify-content': 'center'})
    ], id='modal_edit_narrative_gasto_salario_anual', is_open=False, size='lg'),
    dbc.Modal([
        dbc.ModalHeader(dbc.ModalTitle('Historico de Narrativas')),
        dbc.ModalBody([html.Div(id='div_historico_gasto_salario_anual')])
    ], id='modal_historico_narrativa_gasto_salario_anual', is_open=False, size='lg'),
    dbc.Modal([
        dbc.ModalHeader('Editar Prompt da Narrativa'),
        dbc.ModalBody([
            dbc.Textarea(
                className="mb-3", placeholder="A Textarea", id='textarea_edit_prompt_narrative_gasto_esco_civil',
                size='md', rows=3
            ),
            html.Div(id='table_edit_narrative_gasto_esco_civil', style={'margin-top': '15px'}),
            html.Div(
                dbc.Button('Salvar', color='success', n_clicks=0, id='button_save_narrative_gasto_esco_civil'),
                style={'margin-top': '15px'}
            )
        ]),
        dbc.ModalFooter([
            html.Div(id='alert_edit_narrative_gasto_esco_civil')
        ], style={'justify-content': 'center'})
    ], id='modal_edit_narrative_gasto_esco_civil', is_open=False, size='lg'),
    dbc.Modal([
        dbc.ModalHeader(dbc.ModalTitle('Historico de Narrativas')),
        dbc.ModalBody([html.Div(id='div_historico_gasto_esco_civil')])
    ], id='modal_historico_narrativa_gasto_esco_civil', is_open=False, size='lg'),
    dbc.Modal([
        dbc.ModalHeader('Editar Prompt da Narrativa'),
        dbc.ModalBody([
            dbc.Textarea(
                className="mb-3", placeholder="A Textarea", id='textarea_edit_prompt_narrative_gasto_filhos_casa',
                size='md', rows=3
            ),
            html.Div(id='table_edit_narrative_gasto_filhos_casa', style={'margin-top': '15px'}),
            html.Div(
                dbc.Button('Salvar', color='success', n_clicks=0, id='button_save_narrative_gasto_filhos_casa'),
                style={'margin-top': '15px'}
            )
        ]),
        dbc.ModalFooter([
            html.Div(id='alert_edit_narrative_gasto_filhos_casa')
        ], style={'justify-content': 'center'})
    ], id='modal_edit_narrative_gasto_filhos_casa', is_open=False, size='lg'),
    dbc.Modal([
        dbc.ModalHeader(dbc.ModalTitle('Historico de Narrativas')),
        dbc.ModalBody([html.Div(id='div_historico_gasto_filhos_casa')])
    ], id='modal_historico_narrativa_gasto_filhos_casa', is_open=False, size='lg'),
    dbc.Modal([
        dbc.ModalHeader('Editar Prompt da Narrativa'),
        dbc.ModalBody([
            dbc.Textarea(
                className="mb-3", placeholder="A Textarea", id='textarea_edit_prompt_narrative_gasto_adolescentes_casa',
                size='md', rows=3
            ),
            html.Div(id='table_edit_narrative_gasto_adolescentes_casa', style={'margin-top': '15px'}),
            html.Div(
                dbc.Button('Salvar', color='success', n_clicks=0, id='button_save_narrative_gasto_adolescentes_casa'),
                style={'margin-top': '15px'}
            )
        ]),
        dbc.ModalFooter([
            html.Div(id='alert_edit_narrative_gasto_adolescentes_casa')
        ], style={'justify-content': 'center'})
    ], id='modal_edit_narrative_gasto_adolescentes_casa', is_open=False, size='lg'),
    dbc.Modal([
        dbc.ModalHeader(dbc.ModalTitle('Historico de Narrativas')),
        dbc.ModalBody([html.Div(id='div_historico_gasto_adolescentes_casa')])
    ], id='modal_historico_narrativa_gasto_adolescentes_casa', is_open=False, size='lg')
])

# --------------------------------------------------------Gráficos------------------------------------------------------


# Gráfico total gasto x sálario anual
@callback(
    Output(component_id='graph_gasto_e_salario_anual', component_property='figure'),
    [
        Input(component_id='data_marketing', component_property='data'),
        Input(component_id='radio_linear_log', component_property='value')
    ]
)
def func(data_marketing, value):
    dframe = pd.read_json(data_marketing, orient='split', convert_dates=['Data Cadastro'])
    fig = go.Figure()

    if not value:
        fig.add_trace(go.Scatter(x=dframe['Salario Anual'], y=dframe['Total Gasto'], mode='markers'))
    else:
        fig.add_trace(
            go.Scatter(x=np.log(dframe['Salario Anual']), y=np.log(dframe['Total Gasto']), mode='markers')
        )

    fig.update_layout(height=350, margin=dict(l=0, r=0, t=0, b=0))
    fig.update_xaxes(title='Salário Anual')
    return fig


# Gráfico gasto por escolaridade e estado civil
@callback(
    Output(component_id='graph_gasto_escolaridade_civil', component_property='figure'),
    Input(component_id='data_marketing', component_property='data')
)
def func(data_marketing):
    dframe = pd.read_json(data_marketing, orient='split', convert_dates=['Data Cadastro'])
    fig = px.treemap(
        dframe, path=[px.Constant("Total Gasto"), 'Estado Civil', 'Escolaridade'], values='Total Gasto',
    )
    fig.update_layout(height=385, margin=dict(l=0, r=0, t=20, b=0))
    fig.update_traces(root_color="lightgrey")
    return fig


# Gráfico gasto x filhos em casa
@callback(
    Output(component_id='graph_total_gastos_filhos', component_property='figure'),
    Input(component_id='data_marketing', component_property='data')
)
def func(data_marketing):
    dframe = pd.read_json(
        data_marketing, orient='split', convert_dates=['Data Cadastro'], dtype={'Filhos em Casa': str}
    )
    _ = dframe.groupby(by=['Filhos em Casa'], as_index=False).agg({'Total Gasto': np.sum})
    fig = Graphs.Bar(_['Filhos em Casa'], _['Total Gasto'])
    return fig


# Gráfico gasto x adolescentes em casa
@callback(
    Output(component_id='graph_total_gasto_adolescente', component_property='figure'),
    Input(component_id='data_marketing', component_property='data')
)
def func(data_marketing):
    dframe = pd.read_json(
        data_marketing, orient='split', convert_dates=['Data Cadastro'], dtype={'Adolescentes em Casa': str}
    )
    _ = dframe.groupby(by=['Adolescentes em Casa'], as_index=False).agg({'Total Gasto': np.sum})

    fig = Graphs.Bar(_['Adolescentes em Casa'], _['Total Gasto'])
    return fig

# --------------------------------------------------------------Narrativa-----------------------------------------------

# --------------------------------------------------------Total Gasto X Salario Anual-----------------------------------


# Criação da narrativa
@callback(
    [
        Output(component_id='text_area_gasto_salario_anual', component_property='value'),
        Output(component_id='toast_narrative_gasto_salario_anual', component_property='is_open')
    ],
    [
        Input(component_id='create_narrative_gasto_salario_anual', component_property='n_clicks'),
        Input(component_id='caixa_narrativa_gasto_salario_anual', component_property='n_clicks')
    ],
    [
        State(component_id='data_marketing', component_property='data'),
        State(component_id='persistence_narrative', component_property='data'),
        State(component_id='persistence_toast', component_property='data')
    ]
)
def func(n1, n2, data_marketing, d_narrative, d_toast):
    data_narrative = json.loads(d_narrative)
    data_toast = json.loads(d_toast)
    if ctx.triggered_id == 'create_narrative_gasto_salario_anual':

        mapper = {
            'count': 'Total de Ocorrências',
            'mean': 'Média',
            'std': 'Desvio Padrão',
            'min': 'Valor Minimo',
            '25%': 'Primeiro Quartil',
            '50%': 'Mediana',
            '75%': 'Terceiro Quartil',
            'max': 'Valor Máximo'
        }

        dframe = pd.read_json(data_marketing, orient='split')

        estats = dframe.loc[:, ['Salario Anual', 'Total Gasto']].describe().rename(mapper=mapper, axis=0).to_csv()
        corr = dframe.loc[:, ['Salario Anual', 'Total Gasto']].corr().to_csv()
        dados = 'estatisticas descritivas:\n\n' + estats + 'grau de correlação entre as variáveis:\n\n' + corr

        narrative = create_narrative(dados, 'total gasto x salario anual')
        # narrative = create_false_narrative('total gasto x salario anual')
        return narrative, True
    elif ctx.triggered_id == 'caixa_narrativa_gasto_salario_anual':
        return '', True
    elif data_toast['Visao Comportamento']['Total Gasto x Salario Anual']:
        value = data_narrative['Visao Comportamento']['Total Gasto x Salario Anual']
        return value, True
    else:
        raise exceptions.PreventUpdate


# Cria o modal de edição de narrativa
@callback(
    [
        Output(component_id='modal_edit_narrative_gasto_salario_anual', component_property='is_open'),
        Output(component_id='textarea_edit_prompt_narrative_gasto_salario_anual', component_property='value'),
        Output(component_id='table_edit_narrative_gasto_salario_anual', component_property='children')
    ],
    Input(component_id='edit_prompt_narrative_gasto_salario_anual', component_property='n_clicks'),
    State(component_id='data_marketing', component_property='data')
)
def func(n_click, data_marketing):
    if n_click:
        dframe = pd.read_json(data_marketing, orient='split')
        _ = dframe.loc[:, ['Salario Anual', 'Total Gasto']].sample(100)

        try:
            response = response_modal_prompt_narrative(_, 'total gasto x salario anual')
        except Exception as msg:
            logging.exception(msg)
            raise exceptions.PreventUpdate
        else:
            return response
    else:
        raise exceptions.PreventUpdate


# Salva o arquivo json com o prompt
@callback(
    Output(component_id='alert_edit_narrative_gasto_salario_anual', component_property='children'),
    Input(component_id='button_save_narrative_gasto_salario_anual', component_property='n_clicks'),
    State(component_id='textarea_edit_prompt_narrative_gasto_salario_anual', component_property='value')
)
def func(n_click, value):
    if n_click:
        return save_json_prompt('total gasto x salario anual', value)
    else:
        raise exceptions.PreventUpdate


# Modal historico de narrativas
@callback(
    [
        Output(component_id='modal_historico_narrativa_gasto_salario_anual', component_property='is_open'),
        Output(component_id='div_historico_gasto_salario_anual', component_property='children')
    ],
    Input(component_id='historico_narrative_salario_gasto_anual', component_property='n_clicks')
)
def fun(n_click):
    if n_click:
        try:
            response = modal_historic_narrative('total gasto x salario anual')
        except Exception as msg:
            logging.exception(msg)
            raise exceptions.PreventUpdate
        else:
            return response
    else:
        raise exceptions.PreventUpdate


# ----------------------------------------Total Gasto Por Escolaridade e Estado Civil-----------------------------------


# Criação da narrativa
@callback(
    [
        Output(component_id='text_area_gasto_esco_civil', component_property='value'),
        Output(component_id='toast_narrative_gasto_esco_civil', component_property='is_open')
    ],
    [
        Input(component_id='create_narrative_gasto_esco_civil', component_property='n_clicks'),
        Input(component_id='caixa_narrativa_gasto_esco_civil', component_property='n_clicks')
    ],
    [
        State(component_id='data_marketing', component_property='data'),
        State(component_id='persistence_narrative', component_property='data'),
        State(component_id='persistence_toast', component_property='data')
    ]
)
def func(n1, n2, data_marketing, d_narrative, d_toast):
    data_narrative = json.loads(d_narrative)
    data_toast = json.loads(d_toast)
    if ctx.triggered_id == 'create_narrative_gasto_esco_civil':
        dframe = pd.read_json(data_marketing, orient='split')

        _ = dframe.groupby(by=['Estado Civil', 'Escolaridade'], as_index=False).agg({'Total Gasto': np.sum})
        _['Porcentagem Total Gasto'] = (_['Total Gasto'] / _['Total Gasto'].sum()) * 100
        _ = _.round(decimals=2)
        narrative = create_narrative(_.to_csv(index=False), 'total gasto por escolaridade e estado civil')
        # narrative = create_false_narrative('total gasto por escolaridade e estado civil')
        return narrative, True
    elif ctx.triggered_id == 'caixa_narrativa_gasto_esco_civil':
        return '', True
    elif data_toast['Visao Comportamento']['Total Gasto Por Escolaridade e Estado Civil']:
        value = data_narrative['Visao Comportamento']['Total Gasto Por Escolaridade e Estado Civil']
        return value, True
    else:
        raise exceptions.PreventUpdate


# Cria o modal de edição de narrativa
@callback(
    [
        Output(component_id='modal_edit_narrative_gasto_esco_civil', component_property='is_open'),
        Output(component_id='textarea_edit_prompt_narrative_gasto_esco_civil', component_property='value'),
        Output(component_id='table_edit_narrative_gasto_esco_civil', component_property='children')
    ],
    Input(component_id='edit_prompt_narrative_gasto_esco_civil', component_property='n_clicks'),
    State(component_id='data_marketing', component_property='data')
)
def func(n_click, data_marketing):
    if n_click:
        dframe = pd.read_json(data_marketing, orient='split')
        _ = dframe.groupby(by=['Estado Civil', 'Escolaridade'], as_index=False).agg({'Total Gasto': np.sum})

        try:
            response = response_modal_prompt_narrative(_, 'total gasto por escolaridade e estado civil')
        except Exception as msg:
            logging.exception(msg)
            raise exceptions.PreventUpdate
        else:
            return response
    else:
        raise exceptions.PreventUpdate


# Salva o arquivo json com o prompt
@callback(
    Output(component_id='alert_edit_narrative_gasto_esco_civil', component_property='children'),
    Input(component_id='button_save_narrative_gasto_esco_civil', component_property='n_clicks'),
    State(component_id='textarea_edit_prompt_narrative_gasto_esco_civil', component_property='value')
)
def func(n_click, value):
    if n_click:
        return save_json_prompt('total gasto por escolaridade e estado civil', value)
    else:
        raise exceptions.PreventUpdate


# Modal historico de narrativas
@callback(
    [
        Output(component_id='modal_historico_narrativa_gasto_esco_civil', component_property='is_open'),
        Output(component_id='div_historico_gasto_esco_civil', component_property='children')
    ],
    Input(component_id='historico_narrative_gasto_esco_civil', component_property='n_clicks')
)
def fun(n_click):
    if n_click:
        try:
            response = modal_historic_narrative('total gasto por escolaridade e estado civil')
        except Exception as msg:
            logging.exception(msg)
            raise exceptions.PreventUpdate
        else:
            return response
    else:
        raise exceptions.PreventUpdate


# ---------------------------------------------Total Gasto x Filhos em Casa---------------------------------------------


# Criação da narrativa
@callback(
    [
        Output(component_id='text_area_gasto_filhos_casa', component_property='value'),
        Output(component_id='toast_narrative_gasto_filhos_casa', component_property='is_open')
    ],
    [
        Input(component_id='create_narrative_gasto_filhos_casa', component_property='n_clicks'),
        Input(component_id='caixa_narrativa_gasto_filhos_casa', component_property='n_clicks')
    ],
    [
        State(component_id='data_marketing', component_property='data'),
        State(component_id='persistence_narrative', component_property='data'),
        State(component_id='persistence_toast', component_property='data')
    ]
)
def func(n1, n2, data_marketing, d_narrative, d_toast):
    data_narrative = json.loads(d_narrative)
    data_toast = json.loads(d_toast)
    if ctx.triggered_id == 'create_narrative_gasto_filhos_casa':
        dframe = pd.read_json(data_marketing, orient='split')

        _ = dframe.groupby(by='Filhos em Casa', as_index=False).agg({'Total Gasto': np.sum})
        _['Porcentagem Total Gasto'] = (_['Total Gasto'] / _['Total Gasto'].sum()) * 100
        _ = _.round(decimals=2)
        narrative = create_narrative(_.to_csv(index=False), 'total gasto x filhos em casa')
        # narrative = create_false_narrative('total gasto x filhos em casa')
        return narrative, True
    elif ctx.triggered_id == 'caixa_narrativa_gasto_filhos_casa':
        return '', True
    elif data_toast['Visao Comportamento']['Total Gasto x Filhos em Casa']:
        value = data_narrative['Visao Comportamento']['Total Gasto x Filhos em Casa']
        return value, True
    else:
        raise exceptions.PreventUpdate


# Modal historico de narrativas
@callback(
    [
        Output(component_id='modal_historico_narrativa_gasto_filhos_casa', component_property='is_open'),
        Output(component_id='div_historico_gasto_filhos_casa', component_property='children')
    ],
    Input(component_id='historico_narrative_gasto_filhos_casa', component_property='n_clicks')
)
def fun(n_click):
    if n_click:
        try:
            response = modal_historic_narrative('total gasto x filhos em casa')
        except Exception as msg:
            logging.exception(msg)
            raise exceptions.PreventUpdate
        else:
            return response
    else:
        raise exceptions.PreventUpdate


# Cria o modal de edição de narrativa
@callback(
    [
        Output(component_id='modal_edit_narrative_gasto_filhos_casa', component_property='is_open'),
        Output(component_id='textarea_edit_prompt_narrative_gasto_filhos_casa', component_property='value'),
        Output(component_id='table_edit_narrative_gasto_filhos_casa', component_property='children')
    ],
    Input(component_id='edit_prompt_narrative_gasto_filhos_casa', component_property='n_clicks'),
    State(component_id='data_marketing', component_property='data')
)
def func(n_click, data_marketing):
    if n_click:
        dframe = pd.read_json(data_marketing, orient='split')
        _ = dframe.groupby(by='Filhos em Casa', as_index=False).agg({'Total Gasto': np.sum})

        try:
            response = response_modal_prompt_narrative(_, 'total gasto x filhos em casa')
        except Exception as msg:
            logging.exception(msg)
            raise exceptions.PreventUpdate
        else:
            return response
    else:
        raise exceptions.PreventUpdate


# Salva o arquivo json com o prompt
@callback(
    Output(component_id='alert_edit_narrative_gasto_filhos_casa', component_property='children'),
    Input(component_id='button_save_narrative_gasto_filhos_casa', component_property='n_clicks'),
    State(component_id='textarea_edit_prompt_narrative_gasto_filhos_casa', component_property='value')
)
def func(n_click, value):
    if n_click:
        return save_json_prompt('total gasto x filhos em casa', value)
    else:
        raise exceptions.PreventUpdate


# --------------------------------------------Total Gasto x Adolescentes em Casa----------------------------------------


# Criação da narrativa
@callback(
    [
        Output(component_id='text_area_gasto_adolescentes_casa', component_property='value'),
        Output(component_id='toast_narrative_gasto_adolescentes_casa', component_property='is_open')
    ],
    [
        Input(component_id='create_narrative_gasto_adolescentes_casa', component_property='n_clicks'),
        Input(component_id='caixa_narrativa_gasto_adolescentes_casa', component_property='n_clicks')
    ],
    [
        State(component_id='data_marketing', component_property='data'),
        State(component_id='persistence_narrative', component_property='data'),
        State(component_id='persistence_toast', component_property='data')
    ]
)
def func(n1, n2, data_marketing, d_narrative, d_toast):
    data_narrative = json.loads(d_narrative)
    data_toast = json.loads(d_toast)
    if ctx.triggered_id == 'create_narrative_gasto_adolescentes_casa':
        dframe = pd.read_json(data_marketing, orient='split')

        _ = dframe.groupby(by='Adolescentes em Casa', as_index=False).agg({'Total Gasto': np.sum})
        _['Porcentagem Total Gasto'] = (_['Total Gasto'] / _['Total Gasto'].sum()) * 100
        _ = _.round(decimals=2)
        narrative = create_narrative(_.to_csv(index=False), 'total gasto x adolescentes em casa')
        # narrative = create_false_narrative('total gasto x adolescentes em casa')
        return narrative, True
    elif ctx.triggered_id == 'caixa_narrativa_gasto_adolescentes_casa':
        return '', True
    elif data_toast['Visao Comportamento']['Total Gasto x Adolescentes em Casa']:
        value = data_narrative['Visao Comportamento']['Total Gasto x Adolescentes em Casa']
        return value, True
    else:
        raise exceptions.PreventUpdate


# Modal historico de narrativas
@callback(
    [
        Output(component_id='modal_historico_narrativa_gasto_adolescentes_casa', component_property='is_open'),
        Output(component_id='div_historico_gasto_adolescentes_casa', component_property='children')
    ],
    Input(component_id='historico_narrative_gasto_adolescentes_casa', component_property='n_clicks')
)
def fun(n_click):
    if n_click:
        try:
            response = modal_historic_narrative('total gasto x adolescentes em casa')
        except Exception as msg:
            logging.exception(msg)
            raise exceptions.PreventUpdate
        else:
            return response
    else:
        raise exceptions.PreventUpdate


# Cria o modal de edição de narrativa
@callback(
    [
        Output(component_id='modal_edit_narrative_gasto_adolescentes_casa', component_property='is_open'),
        Output(component_id='textarea_edit_prompt_narrative_gasto_adolescentes_casa', component_property='value'),
        Output(component_id='table_edit_narrative_gasto_adolescentes_casa', component_property='children')
    ],
    Input(component_id='edit_prompt_narrative_gasto_adolescentes_casa', component_property='n_clicks'),
    State(component_id='data_marketing', component_property='data')
)
def func(n_click, data_marketing):
    if n_click:
        dframe = pd.read_json(data_marketing, orient='split')
        _ = dframe.groupby(by='Adolescentes em Casa', as_index=False).agg({'Total Gasto': np.sum})

        try:
            response = response_modal_prompt_narrative(_, 'total gasto x adolescentes em casa')
        except Exception as msg:
            logging.exception(msg)
            raise exceptions.PreventUpdate
        else:
            return response
    else:
        raise exceptions.PreventUpdate


# Salva o arquivo json com o prompt
@callback(
    Output(component_id='alert_edit_narrative_gasto_adolescentes_casa', component_property='children'),
    Input(component_id='button_save_narrative_gasto_adolescentes_casa', component_property='n_clicks'),
    State(component_id='textarea_edit_prompt_narrative_gasto_adolescentes_casa', component_property='value')
)
def func(n_click, value):
    if n_click:
        return save_json_prompt('total gasto x adolescentes em casa', value)
    else:
        raise exceptions.PreventUpdate


# --------------------------------------------------Persistence Toast---------------------------------------------------


@dash.get_app().callback(
    Output(component_id='persistence_toast', component_property='data', allow_duplicate=True),
    [
        Input(component_id='toast_narrative_gasto_salario_anual', component_property='is_open'),
        Input(component_id='toast_narrative_gasto_esco_civil', component_property='is_open'),
        Input(component_id='toast_narrative_gasto_filhos_casa', component_property='is_open'),
        Input(component_id='toast_narrative_gasto_adolescentes_casa', component_property='is_open')
    ],
    State(component_id='persistence_toast', component_property='data'),
    prevent_initial_call=True
)
def func(open_sa, open_ec, open_fc, open_ac, data):
    data_toast = json.loads(data)
    if ctx.triggered_id == 'toast_narrative_gasto_salario_anual':
        data_toast['Visao Comportamento']['Total Gasto x Salario Anual'] = open_sa
    elif ctx.triggered_id == 'toast_narrative_gasto_esco_civil':
        data_toast['Visao Comportamento']['Total Gasto Por Escolaridade e Estado Civil'] = open_ec
    elif ctx.triggered_id == 'toast_narrative_gasto_filhos_casa':
        data_toast['Visao Comportamento']['Total Gasto x Filhos em Casa'] = open_fc
    elif ctx.triggered_id == 'toast_narrative_gasto_adolescentes_casa':
        data_toast['Visao Comportamento']['Total Gasto x Adolescentes em Casa'] = open_ac
    return json.dumps(data_toast)


# -------------------------------------------------Persistence Narrative------------------------------------------------


@dash.get_app().callback(
    Output(component_id='persistence_narrative', component_property='data', allow_duplicate=True),
    [
        Input(component_id='text_area_gasto_salario_anual', component_property='value'),
        Input(component_id='text_area_gasto_esco_civil', component_property='value'),
        Input(component_id='text_area_gasto_filhos_casa', component_property='value'),
        Input(component_id='text_area_gasto_adolescentes_casa', component_property='value')
    ],
    State(component_id='persistence_narrative', component_property='data'),
    prevent_initial_call=True
)
def func(value_sa, value_ec, value_fc, value_ac, data):
    data_narrative = json.loads(data)
    if ctx.triggered_id == 'text_area_gasto_salario_anual':
        data_narrative['Visao Comportamento']['Total Gasto x Salario Anual'] = value_sa
    elif ctx.triggered_id == 'text_area_gasto_esco_civil':
        data_narrative['Visao Comportamento']['Total Gasto Por Escolaridade e Estado Civil'] = value_ec
    elif ctx.triggered_id == 'text_area_gasto_filhos_casa':
        data_narrative['Visao Comportamento']['Total Gasto x Filhos em Casa'] = value_fc
    elif ctx.triggered_id == 'text_area_gasto_adolescentes_casa':
        data_narrative['Visao Comportamento']['Total Gasto x Adolescentes em Casa'] = value_ac
    return json.dumps(data_narrative)


# ---------------------------------------------------Persistence Figure-------------------------------------------------

@dash.get_app().callback(
    Output(component_id='persistence_figure', component_property='data', allow_duplicate=True),
    [
        Input(component_id='graph_gasto_e_salario_anual', component_property='figure'),
        Input(component_id='graph_gasto_escolaridade_civil', component_property='figure'),
        Input(component_id='graph_total_gastos_filhos', component_property='figure'),
        Input(component_id='graph_total_gasto_adolescente', component_property='figure')
    ],
    State(component_id='persistence_figure', component_property='data'),
    prevent_initial_call=True
)
def func(fig1, fig2, fig3, fig4, data):
    data_figure = json.loads(data)
    data_figure['Visao Comportamento']['Total Gasto x Salario Anual'] = fig1
    data_figure['Visao Comportamento']['Total Gasto Por Escolaridade e Estado Civil'] = fig2
    data_figure['Visao Comportamento']['Total Gasto x Filhos em Casa'] = fig3
    data_figure['Visao Comportamento']['Total Gasto x Adolescentes em Casa'] = fig4

    return json.dumps(data_figure)
