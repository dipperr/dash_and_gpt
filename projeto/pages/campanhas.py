from dash import (
    html,
    dcc,
    callback,
    Input,
    Output,
    State,
    dash_table,
    ctx,
    exceptions
)
import dash
import dash_bootstrap_components as dbc
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import json
import logging

from utils import (
    create_narrative,
    create_false_narrative,
    response_modal_prompt_narrative,
    save_json_prompt,
    modal_historic_narrative,
    Graphs
)


dash.register_page(__name__, path='/visao_campanhas')

layout = html.Div(children=[
    dbc.Card([
        dbc.CardBody([
            dbc.Row([
                dbc.Col([
                    dbc.Card([
                        dbc.CardHeader([
                            dbc.Row([
                                dbc.Col([
                                    html.Label('Efetividade da Campanha X Números de Filhos')
                                ], md=10),
                                dbc.Col([
                                    dbc.DropdownMenu([
                                        dbc.DropdownMenuItem(
                                            'Criar Narrativa', n_clicks=0, id='create_narrative_campanha_filhos'
                                        ),
                                        dbc.DropdownMenuItem(
                                            'Editar Prompt de Narrativa', n_clicks=0,
                                            id='edit_prompt_narrative_campanha_filhos'
                                        ),
                                        dbc.DropdownMenuItem(
                                            'Historico de Narrativa', n_clicks=0,
                                            id='historico_narrative_campanha_filhos'
                                        ),
                                        dbc.DropdownMenuItem(
                                            'Caixa de Narrativa', n_clicks=0, id='caixa_narrativa_campanha_filhos'
                                        )
                                    ], label='Menu')
                                ], md=2)
                            ])
                        ]),
                        dbc.CardBody([dcc.Graph(id='graph_efetividade_campanha_filhos')]),
                        dbc.CardFooter([
                            dcc.Loading(
                                type='dot',
                                children=[
                                    dbc.Toast(
                                        children=[
                                            dbc.Textarea(
                                                className="mb-3", size='md', rows=10,
                                                id='text_area_campanha_filhos'
                                            )
                                        ],
                                        header='Narrativa', dismissable=True, style={'width': '100%'},
                                        is_open=False, id='toast_narrative_campanha_filhos'
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
                                    html.Label('Resultado das Campanhas X Média de Salário Anual')
                                ], md=10),
                                dbc.Col([
                                    dbc.DropdownMenu([
                                        dbc.DropdownMenuItem(
                                            'Criar Narrativa', n_clicks=0, id='create_narrative_campanha_salario'
                                        ),
                                        dbc.DropdownMenuItem(
                                            'Editar Prompt de Narrativa', n_clicks=0,
                                            id='edit_prompt_narrative_campanha_salario'
                                        ),
                                        dbc.DropdownMenuItem(
                                            'Historico de Narrativa', n_clicks=0,
                                            id='historico_narrative_campanha_salario'
                                        ),
                                        dbc.DropdownMenuItem(
                                            'Caixa de Narrativa', n_clicks=0, id='caixa_narrativa_campanha_salario'
                                        )
                                    ], label='Menu')
                                ], md=2)
                            ])
                        ]),
                        dbc.CardBody([dcc.Graph(id='graph_media_salario_campanha')]),
                        dbc.CardFooter([
                            dcc.Loading(
                                type='dot',
                                children=[
                                    dbc.Toast(
                                        children=[
                                            dbc.Textarea(
                                                className="mb-3", size='md', rows=10,
                                                id='text_area_campanha_salario'
                                            )
                                        ],
                                        header='Narrativa', dismissable=True, style={'width': '100%'},
                                        is_open=False, id='toast_narrative_campanha_salario'
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
                                    dbc.DropdownMenu([
                                        dbc.DropdownMenuItem(
                                            'Criar Narrativa', n_clicks=0, id='create_narrative_campanha_table'
                                        ),
                                        dbc.DropdownMenuItem(
                                            'Editar Prompt de Narrativa', n_clicks=0,
                                            id='edit_prompt_narrative_campanha_table'
                                        ),
                                        dbc.DropdownMenuItem(
                                            'Historico de Narrativa', n_clicks=0,
                                            id='historico_narrative_campanha_table'
                                        ),
                                        dbc.DropdownMenuItem(
                                            'Caixa de Narrativa', n_clicks=0, id='caixa_narrativa_campanha_table'
                                        )
                                    ], label='Menu')
                                ], md=2)
                            ], justify='end')
                        ]),
                        dbc.CardBody([
                            html.Div(id='table_visitas_web_site'),
                            dash_table.DataTable(
                                style_table={'height': '350px', 'overflowY': 'auto'},
                                style_header={'textAlign': 'center'},
                                style_cell={'textAlign': 'left', 'fontWeight': 'bold'},
                                merge_duplicate_headers=True, page_action = 'none',
                                id='table_visitas_web_site'
                            )
                        ]),
                        dbc.CardFooter([
                            dcc.Loading(
                                type='dot',
                                children=[
                                    dbc.Toast(
                                        children=[
                                            dbc.Textarea(
                                                className="mb-3", size='md', rows=10,
                                                id='text_area_campanha_table'
                                            )
                                        ],
                                        header='Narrativa', dismissable=True, style={'width': '100%'},
                                        is_open=False, id='toast_narrative_campanha_table'
                                    )
                                ], color='#636EFA', style={'margin-top': '5px'}
                            )
                        ])
                    ])
                ], md=8),
                dbc.Col([
                    dbc.Card([
                        dbc.CardHeader([
                            dbc.Row([
                                dbc.Col([
                                    html.Label('Resultado das Campanhas de Marketing')
                                ], md=9),
                                dbc.Col([
                                    dbc.DropdownMenu([
                                        dbc.DropdownMenuItem(
                                            'Criar Narrativa', n_clicks=0, id='create_narrative_campanha_marketing'
                                        ),
                                        dbc.DropdownMenuItem(
                                            'Editar Prompt de Narrativa', n_clicks=0,
                                            id='edit_prompt_narrative_campanha_marketing'
                                        ),
                                        dbc.DropdownMenuItem(
                                            'Historico de Narrativa', n_clicks=0,
                                            id='historico_narrative_campanha_marketing'
                                        ),
                                        dbc.DropdownMenuItem(
                                            'Caixa de Narrativa', n_clicks=0, id='caixa_narrativa_campanha_marketing'
                                        )
                                    ], label='Menu')
                                ], md=3)
                            ])
                        ]),
                        dbc.CardBody([dcc.Graph(id='graph_resultado_campanha')]),
                        dbc.CardFooter([
                            dcc.Loading(
                                type='dot',
                                children=[
                                    dbc.Toast(
                                        children=[
                                            dbc.Textarea(
                                                className="mb-3", size='md', rows=10,
                                                id='text_area_campanha_marketing'
                                            )
                                        ],
                                        header='Narrativa', dismissable=True, style={'width': '100%'},
                                        is_open=False, id='toast_narrative_campanha_marketing'
                                    )
                                ], color='#636EFA', style={'margin-top': '5px'}
                            )
                        ])
                    ])
                ], md=4)
            ], style={'margin-top': '10px'})
        ])
    ]),
    dbc.Modal([
        dbc.ModalHeader('Editar Prompt da Narrativa'),
        dbc.ModalBody([
            dbc.Textarea(
                className="mb-3", placeholder="A Textarea", id='textarea_edit_prompt_narrative_campanha_filhos',
                size='md', rows=3
            ),
            html.Div(id='table_edit_narrative_campanha_filhos', style={'margin-top': '15px'}),
            html.Div(
                dbc.Button('Salvar', color='success', n_clicks=0, id='button_save_narrative_campanha_filhos'),
                style={'margin-top': '15px'}
            )
        ]),
        dbc.ModalFooter([
            html.Div(id='alert_edit_narrative_campanha_filhos')
        ], style={'justify-content': 'center'})
    ], id='modal_edit_narrative_campanha_filhos', is_open=False, size='lg'),
    dbc.Modal([
        dbc.ModalHeader(dbc.ModalTitle('Historico de Narrativas')),
        dbc.ModalBody([html.Div(id='div_historico_campanha_filhos')])
    ], id='modal_historico_narrativa_campanha_filhos', is_open=False, size='lg'),
    dbc.Modal([
        dbc.ModalHeader('Editar Prompt da Narrativa'),
        dbc.ModalBody([
            dbc.Textarea(
                className="mb-3", placeholder="A Textarea", id='textarea_edit_prompt_narrative_campanha_salario',
                size='md', rows=3
            ),
            html.Div(id='table_edit_narrative_campanha_salario', style={'margin-top': '15px'}),
            html.Div(
                dbc.Button('Salvar', color='success', n_clicks=0, id='button_save_narrative_campanha_salario'),
                style={'margin-top': '15px'}
            )
        ]),
        dbc.ModalFooter([
            html.Div(id='alert_edit_narrative_campanha_salario')
        ], style={'justify-content': 'center'})
    ], id='modal_edit_narrative_campanha_salario', is_open=False, size='lg'),
    dbc.Modal([
        dbc.ModalHeader(dbc.ModalTitle('Historico de Narrativas')),
        dbc.ModalBody([html.Div(id='div_historico_campanha_salario')])
    ], id='modal_historico_narrativa_campanha_salario', is_open=False, size='lg'),
    dbc.Modal([
        dbc.ModalHeader('Editar Prompt da Narrativa'),
        dbc.ModalBody([
            dbc.Textarea(
                className="mb-3", placeholder="A Textarea", id='textarea_edit_prompt_narrative_campanha_table',
                size='md', rows=3
            ),
            html.Div(id='table_edit_narrative_campanha_table', style={'margin-top': '15px'}),
            html.Div(
                dbc.Button('Salvar', color='success', n_clicks=0, id='button_save_narrative_campanha_table'),
                style={'margin-top': '15px'}
            )
        ]),
        dbc.ModalFooter([
            html.Div(id='alert_edit_narrative_campanha_table')
        ], style={'justify-content': 'center'})
    ], id='modal_edit_narrative_campanha_table', is_open=False, size='lg'),
    dbc.Modal([
        dbc.ModalHeader(dbc.ModalTitle('Historico de Narrativas')),
        dbc.ModalBody([html.Div(id='div_historico_campanha_table')])
    ], id='modal_historico_narrativa_campanha_table', is_open=False, size='lg'),
    dbc.Modal([
        dbc.ModalHeader('Editar Prompt da Narrativa'),
        dbc.ModalBody([
            dbc.Textarea(
                className="mb-3", placeholder="A Textarea", id='textarea_edit_prompt_narrative_campanha_marketing',
                size='md', rows=3
            ),
            html.Div(id='table_edit_narrative_campanha_marketing', style={'margin-top': '15px'}),
            html.Div(
                dbc.Button('Salvar', color='success', n_clicks=0, id='button_save_narrative_campanha_marketing'),
                style={'margin-top': '15px'}
            )
        ]),
        dbc.ModalFooter([
            html.Div(id='alert_edit_narrative_campanha_marketing')
        ], style={'justify-content': 'center'})
    ], id='modal_edit_narrative_campanha_marketing', is_open=False, size='lg'),
    dbc.Modal([
        dbc.ModalHeader(dbc.ModalTitle('Historico de Narrativas')),
        dbc.ModalBody([html.Div(id='div_historico_campanha_marketing')])
    ], id='modal_historico_narrativa_campanha_marketing', is_open=False, size='lg')
])

# ------------------------------------------------------Gráficos--------------------------------------------------------


# Gráfico efetividade da campanha x numeros de filhos
@callback(
    Output(component_id='graph_efetividade_campanha_filhos', component_property='figure'),
    Input(component_id='data_marketing', component_property='data')
)
def func(data_marketing):
    dframe = pd.read_json(
        data_marketing, orient='split', convert_dates=['Data Cadastro'], dtype={'Filhos em Casa': str}
    )

    fig = go.Figure()
    for label in ('Não', 'Sim'):
        _ = (
            dframe.query(f"Comprou == '{label}'").groupby(by='Filhos em Casa', as_index=False)
            .agg({'ID': 'count'})
            .rename(mapper={'ID': 'Total'}, axis=1)
        )
        fig.add_trace(go.Bar(name=label, x=_['Filhos em Casa'], y=_['Total']))
    fig.update_layout(
        barmode='group', margin=dict(l=0, r=0, t=0, b=0), height=350,
        legend=dict(orientation='h', yanchor='bottom', y=1.02, xanchor='left')
    )
    return fig


# Gráfico resultado das campanhas x média de salário anual
@callback(
    Output(component_id='graph_media_salario_campanha', component_property='figure'),
    Input(component_id='data_marketing', component_property='data')
)
def func(data_marketing):
    dframe = pd.read_json(data_marketing, orient='split', convert_dates=['Data Cadastro'])
    _ = dframe.groupby(by='Comprou', as_index=False).agg({'Salario Anual': np.mean}).round(decimals=2)

    fig = Graphs.Bar(_['Comprou'], _['Salario Anual'])

    return fig


# Tabela
@callback(
    [
        Output(component_id='table_visitas_web_site', component_property='columns'),
        Output(component_id='table_visitas_web_site', component_property='data')
    ],
    Input(component_id='data_marketing', component_property='data')
)
def func(data_marketing):
    dframe = pd.read_json(data_marketing, orient='split', convert_dates=['Data Cadastro'])

    array_visitas = (
        dframe.groupby(by=['Comprou', 'Estado Civil', 'Pais', 'Escolaridade'])
        .agg({'Numero Visitas WebSite Mes': np.sum})
        .unstack('Escolaridade')
        .reset_index()
        .to_numpy(na_value=0)
    )
    visitas = pd.DataFrame(
        array_visitas,
        columns=['Comprou', 'Estado Civil', 'Pais', 'Curso Superior', 'Doutorado', 'Mestrado', 'Primeiro Grau', 'Segundo Grau']
    )
    columns = [
        {'name': ['', 'Comprou'], 'id': 'Comprou'},
        {'name': ['', 'Estado Civil'], 'id': 'Estado Civil'},
        {'name': ['', 'Pais'], 'id': 'Pais'},
        {'name': ['Escolaridade', 'Curso Superior'], 'id': 'Curso Superior'},
        {'name': ['Escolaridade', 'Doutorado'], 'id': 'Doutorado'},
        {'name': ['Escolaridade', 'Mestrado'], 'id': 'Mestrado'},
        {
            'name': ['Escolaridade', 'Primeiro Grau'],
            'id': 'Primeiro Grau',
            'format': {'nully': {'': 0, None: 0}}
        },
        {'name': ['Escolaridade', 'Segundo Grau'], 'id': 'Segundo Grau'}
    ]
    data = visitas.to_dict(orient='records')

    return columns, data


# Gráfico resultado das campanhas de marketing
@callback(
    Output(component_id='graph_resultado_campanha', component_property='figure'),
    Input(component_id='data_marketing', component_property='data')
)
def func(data_marketing):
    dframe = pd.read_json(data_marketing, orient='split', convert_dates=['Data Cadastro'])
    _ = dframe.groupby(by='Comprou', as_index=False).agg({'ID': 'count'}).rename(mapper={'ID': 'Total'}, axis=1)
    fig = go.Figure(data=[go.Pie(labels=_['Comprou'], values=_['Total'])])
    fig.update_layout(height=350, margin=dict(l=30, r=30, t=30, b=30))
    return fig


# ---------------------------------------------------------Narrativa----------------------------------------------------

# ---------------------------------------Efetividade da Campanha x Números de Filhos------------------------------------


# Criação da narrativa
@callback(
    [
        Output(component_id='text_area_campanha_filhos', component_property='value'),
        Output(component_id='toast_narrative_campanha_filhos', component_property='is_open')
    ],
    [
        Input(component_id='create_narrative_campanha_filhos', component_property='n_clicks'),
        Input(component_id='caixa_narrativa_campanha_filhos', component_property='n_clicks')
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
    if ctx.triggered_id == 'create_narrative_campanha_filhos':
        dframe = pd.read_json(data_marketing, orient='split')

        _ = (
            dframe.groupby(by=['Filhos em Casa', 'Comprou'], as_index=False).agg({'ID': 'count'})
            .rename(mapper={'ID': 'Total'}, axis=1)
        )
        _['Porcentagem Total'] = (_['Total'] / _['Total'].sum()) * 100
        _ = _.round(decimals=2)
        narrative = create_narrative(_.to_csv(index=False), 'efetividade da campanha x numeros de filhos')
        # narrative = create_false_narrative('efetividade da campanha x numeros de filhos')
        return narrative, True
    elif ctx.triggered_id == 'caixa_narrativa_campanha_filhos':
        return '', True
    elif data_toast['Visao Campanhas']['Efetividade da Campanha x Numeros de Filhos']:
        value = data_narrative['Visao Campanhas']['Efetividade da Campanha x Numeros de Filhos']
        return value, True
    else:
        raise exceptions.PreventUpdate


# Cria o modal de edição de narrativa
@callback(
    [
        Output(component_id='modal_edit_narrative_campanha_filhos', component_property='is_open'),
        Output(component_id='textarea_edit_prompt_narrative_campanha_filhos', component_property='value'),
        Output(component_id='table_edit_narrative_campanha_filhos', component_property='children')
    ],
    Input(component_id='edit_prompt_narrative_campanha_filhos', component_property='n_clicks'),
    State(component_id='data_marketing', component_property='data')
)
def func(n_click, data_marketing):
    if n_click:
        dframe = pd.read_json(data_marketing, orient='split')
        _ = (
            dframe.groupby(by=['Filhos em Casa', 'Comprou'], as_index=False).agg({'ID': 'count'})
            .rename(mapper={'ID': 'Total'}, axis=1)
        )

        try:
            response = response_modal_prompt_narrative(_, 'efetividade da campanha x numeros de filhos')
        except Exception as msg:
            logging.exception(msg)
            raise exceptions.PreventUpdate
        else:
            return response
    else:
        raise exceptions.PreventUpdate


# Salva o arquivo json com o prompt
@callback(
    Output(component_id='alert_edit_narrative_campanha_filhos', component_property='children'),
    Input(component_id='button_save_narrative_campanha_filhos', component_property='n_clicks'),
    State(component_id='textarea_edit_prompt_narrative_campanha_filhos', component_property='value')
)
def func(n_click, value):
    if n_click:
        return save_json_prompt('efetividade da campanha x numeros de filhos', value)
    else:
        raise exceptions.PreventUpdate


# Modal historico de narrativas
@callback(
    [
        Output(component_id='modal_historico_narrativa_campanha_filhos', component_property='is_open'),
        Output(component_id='div_historico_campanha_filhos', component_property='children')
    ],
    Input(component_id='historico_narrative_campanha_filhos', component_property='n_clicks')
)
def fun(n_click):
    if n_click:
        try:
            response = modal_historic_narrative('efetividade da campanha x numeros de filhos')
        except Exception as msg:
            logging.exception(msg)
            raise exceptions.PreventUpdate
        else:
            return response
    else:
        raise exceptions.PreventUpdate


# -----------------------------------Media de Salario Anual x Resultado das Campanhas-----------------------------------


# Criação da narrativa
@callback(
    [
        Output(component_id='text_area_campanha_salario', component_property='value'),
        Output(component_id='toast_narrative_campanha_salario', component_property='is_open')
    ],
    [
        Input(component_id='create_narrative_campanha_salario', component_property='n_clicks'),
        Input(component_id='caixa_narrativa_campanha_salario', component_property='n_clicks')
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
    if ctx.triggered_id == 'create_narrative_campanha_salario':
        dframe = pd.read_json(data_marketing, orient='split')

        _ = (
            dframe.groupby(by='Comprou', as_index=False).agg({'Salario Anual': np.mean})
            .rename(mapper={'Salario Anual': 'Media Salario Anual'}, axis=1)
            .round(decimals=2)
        )
        narrative = create_narrative(_.to_csv(index=False), 'efetividade da campanha x media salarial')
        # narrative = create_false_narrative('efetividade da campanha x media salarial')
        return narrative, True
    elif ctx.triggered_id == 'caixa_narrativa_campanha_salario':
        return '', True
    elif data_toast['Visao Campanhas']['Efetividade da Campanha x Media Salarial']:
        value = data_narrative['Visao Campanhas']['Efetividade da Campanha x Media Salarial']
        return value, True
    else:
        raise exceptions.PreventUpdate


# Cria o modal de edição de narrativa
@callback(
    [
        Output(component_id='modal_edit_narrative_campanha_salario', component_property='is_open'),
        Output(component_id='textarea_edit_prompt_narrative_campanha_salario', component_property='value'),
        Output(component_id='table_edit_narrative_campanha_salario', component_property='children')
    ],
    Input(component_id='edit_prompt_narrative_campanha_salario', component_property='n_clicks'),
    State(component_id='data_marketing', component_property='data')
)
def func(n_click, data_marketing):
    if n_click:
        dframe = pd.read_json(data_marketing, orient='split')
        _ = (
            dframe.groupby(by='Comprou', as_index=False).agg({'Salario Anual': np.mean})
            .rename(mapper={'Salario Anual': 'Media Salario Anual'}, axis=1)
            .round(decimals=2)
        )

        try:
            response = response_modal_prompt_narrative(_, 'efetividade da campanha x media salarial')
        except Exception as msg:
            logging.exception(msg)
            raise exceptions.PreventUpdate
        else:
            return response
    else:
        raise exceptions.PreventUpdate


# Salva o arquivo json com o prompt
@callback(
    Output(component_id='alert_edit_narrative_campanha_salario', component_property='children'),
    Input(component_id='button_save_narrative_campanha_salario', component_property='n_clicks'),
    State(component_id='textarea_edit_prompt_narrative_campanha_salario', component_property='value')
)
def func(n_click, value):
    if n_click:
        return save_json_prompt('efetividade da campanha x media salarial', value)
    else:
        raise exceptions.PreventUpdate


# Modal historico de narrativas
@callback(
    [
        Output(component_id='modal_historico_narrativa_campanha_salario', component_property='is_open'),
        Output(component_id='div_historico_campanha_salario', component_property='children')
    ],
    Input(component_id='historico_narrative_campanha_salario', component_property='n_clicks')
)
def fun(n_click):
    if n_click:
        try:
            response = modal_historic_narrative('efetividade da campanha x media salarial')
        except Exception as msg:
            logging.exception(msg)
            raise exceptions.PreventUpdate
        else:
            return response
    else:
        raise exceptions.PreventUpdate


# ----------------------------------------------------------Tabela------------------------------------------------------

# Criação da narrativa
@callback(
    [
        Output(component_id='text_area_campanha_table', component_property='value'),
        Output(component_id='toast_narrative_campanha_table', component_property='is_open')
    ],
    [
        Input(component_id='create_narrative_campanha_table', component_property='n_clicks'),
        Input(component_id='caixa_narrativa_campanha_table', component_property='n_clicks')
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
    if ctx.triggered_id == 'create_narrative_campanha_table':
        dframe = pd.read_json(data_marketing, orient='split')

        _ = (
            dframe.groupby(by=['Comprou', 'Estado Civil', 'Pais', 'Escolaridade'], as_index=False)
            .agg({'Numero Visitas WebSite Mes': np.sum})
        )
        s = _['Numero Visitas WebSite Mes'].sum()
        _['Porcentagem Numero Visitas WebSite Mes'] = (_['Numero Visitas WebSite Mes'] / s) * 100
        _ = _.round(decimals=2)

        narrative = create_narrative(_.to_csv(index=False), 'campanha table')
        # narrative = create_false_narrative('campanha table')
        return narrative, True
    elif ctx.triggered_id == 'caixa_narrativa_campanha_table':
        return '', True
    elif data_toast['Visao Campanhas']['Campanha Table']:
        value = data_narrative['Visao Campanhas']['Campanha Table']
        return value, True
    else:
        raise exceptions.PreventUpdate


# Cria o modal de edição de narrativa
@callback(
    [
        Output(component_id='modal_edit_narrative_campanha_table', component_property='is_open'),
        Output(component_id='textarea_edit_prompt_narrative_campanha_table', component_property='value'),
        Output(component_id='table_edit_narrative_campanha_table', component_property='children')
    ],
    Input(component_id='edit_prompt_narrative_campanha_table', component_property='n_clicks'),
    State(component_id='data_marketing', component_property='data')
)
def func(n_click, data_marketing):
    if n_click:
        dframe = pd.read_json(data_marketing, orient='split')
        _ = (
            dframe.groupby(by=['Comprou', 'Estado Civil', 'Pais', 'Escolaridade'], as_index=False)
            .agg({'Numero Visitas WebSite Mes': np.sum})
        )

        try:
            response = response_modal_prompt_narrative(_, 'campanha table')
        except Exception as msg:
            logging.exception(msg)
            raise exceptions.PreventUpdate
        else:
            return response
    else:
        raise exceptions.PreventUpdate


# Salva o arquivo json com o prompt
@callback(
    Output(component_id='alert_edit_narrative_campanha_table', component_property='children'),
    Input(component_id='button_save_narrative_campanha_table', component_property='n_clicks'),
    State(component_id='textarea_edit_prompt_narrative_campanha_table', component_property='value')
)
def func(n_click, value):
    if n_click:
        return save_json_prompt('campanha table', value)
    else:
        raise exceptions.PreventUpdate


# Modal historico de narrativas
@callback(
    [
        Output(component_id='modal_historico_narrativa_campanha_table', component_property='is_open'),
        Output(component_id='div_historico_campanha_table', component_property='children')
    ],
    Input(component_id='historico_narrative_campanha_table', component_property='n_clicks')
)
def fun(n_click):
    if n_click:
        try:
            response = modal_historic_narrative('campanha table')
        except Exception as msg:
            logging.exception(msg)
            raise exceptions.PreventUpdate
        else:
            return response
    else:
        raise exceptions.PreventUpdate


# -----------------------------------------Resultado das Campanhas de Marketing-----------------------------------------


# Criação da narrativa
@callback(
    [
        Output(component_id='text_area_campanha_marketing', component_property='value'),
        Output(component_id='toast_narrative_campanha_marketing', component_property='is_open')
    ],
    [
        Input(component_id='create_narrative_campanha_marketing', component_property='n_clicks'),
        Input(component_id='caixa_narrativa_campanha_marketing', component_property='n_clicks')
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
    if ctx.triggered_id == 'create_narrative_campanha_marketing':
        dframe = pd.read_json(data_marketing, orient='split')

        _ = (
            dframe.groupby(by='Comprou', as_index=False).agg({'ID': 'count'})
            .rename(mapper={'ID': 'Total'}, axis=1)
        )
        _['Porcentagem Total'] = (_['Total'] / _['Total'].sum()) * 100
        _ = _.round(decimals=2)
        narrative = create_narrative(_.to_csv(index=False), 'resultado das campanhas de marketing')
        # narrative = create_false_narrative('resultado das campanhas de marketing')
        return narrative, True
    elif ctx.triggered_id == 'caixa_narrativa_campanha_marketing':
        return '', True
    elif data_toast['Visao Campanhas']['Resultado das Campanhas de Marketing']:
        value = data_narrative['Visao Campanhas']['Resultado das Campanhas de Marketing']
        return value, True
    else:
        raise exceptions.PreventUpdate


# Cria o modal de edição de narrativa
@callback(
    [
        Output(component_id='modal_edit_narrative_campanha_marketing', component_property='is_open'),
        Output(component_id='textarea_edit_prompt_narrative_campanha_marketing', component_property='value'),
        Output(component_id='table_edit_narrative_campanha_marketing', component_property='children')
    ],
    Input(component_id='edit_prompt_narrative_campanha_marketing', component_property='n_clicks'),
    State(component_id='data_marketing', component_property='data')
)
def func(n_click, data_marketing):
    if n_click:
        dframe = pd.read_json(data_marketing, orient='split')
        _ = (
            dframe.groupby(by='Comprou', as_index=False).agg({'ID': 'count'})
            .rename(mapper={'ID': 'Total'}, axis=1)
        )

        try:
            response = response_modal_prompt_narrative(_, 'resultado das campanhas de marketing')
        except Exception as msg:
            logging.exception(msg)
            raise exceptions.PreventUpdate
        else:
            return response
    else:
        raise exceptions.PreventUpdate


# Salva o arquivo json com o prompt
@callback(
    Output(component_id='alert_edit_narrative_campanha_marketing', component_property='children'),
    Input(component_id='button_save_narrative_campanha_marketing', component_property='n_clicks'),
    State(component_id='textarea_edit_prompt_narrative_campanha_marketing', component_property='value')
)
def func(n_click, value):
    if n_click:
        return save_json_prompt('resultado das campanhas de marketing', value)
    else:
        raise exceptions.PreventUpdate


# Modal historico de narrativas
@callback(
    [
        Output(component_id='modal_historico_narrativa_campanha_marketing', component_property='is_open'),
        Output(component_id='div_historico_campanha_marketing', component_property='children')
    ],
    Input(component_id='historico_narrative_campanha_marketing', component_property='n_clicks')
)
def fun(n_click):
    if n_click:
        try:
            response = modal_historic_narrative('resultado das campanhas de marketing')
        except Exception as msg:
            logging.exception(msg)
            raise exceptions.PreventUpdate
        else:
            return response
    else:
        raise exceptions.PreventUpdate

# ---------------------------------------------------Persistence Toast--------------------------------------------------


@dash.get_app().callback(
    Output(component_id='persistence_toast', component_property='data', allow_duplicate=True),
    [
        Input(component_id='toast_narrative_campanha_filhos', component_property='is_open'),
        Input(component_id='toast_narrative_campanha_salario', component_property='is_open'),
        Input(component_id='toast_narrative_campanha_table', component_property='is_open'),
        Input(component_id='toast_narrative_campanha_marketing', component_property='is_open')
    ],
    State(component_id='persistence_toast', component_property='data'),
    prevent_initial_call=True
)
def func(open_cf, open_cs, open_ct, open_cm, data):
    data_toast = json.loads(data)
    if ctx.triggered_id == 'toast_narrative_campanha_filhos':
        data_toast['Visao Campanhas']['Efetividade da Campanha x Numeros de Filhos'] = open_cf
    elif ctx.triggered_id == 'toast_narrative_campanha_salario':
        data_toast['Visao Campanhas']['Efetividade da Campanha x Media Salarial'] = open_cs
    elif ctx.triggered_id == 'toast_narrative_campanha_table':
        data_toast['Visao Campanhas']['Campanha Table'] = open_ct
    elif ctx.triggered_id == 'toast_narrative_campanha_marketing':
        data_toast['Visao Campanhas']['Resultado das Campanhas de Marketing'] = open_cm

    return json.dumps(data_toast)


# --------------------------------------------------Persistence Narrative-----------------------------------------------


@dash.get_app().callback(
    Output(component_id='persistence_narrative', component_property='data', allow_duplicate=True),
    [
        Input(component_id='text_area_campanha_filhos', component_property='value'),
        Input(component_id='text_area_campanha_salario', component_property='value'),
        Input(component_id='text_area_campanha_table', component_property='value'),
        Input(component_id='text_area_campanha_marketing', component_property='value')
    ],
    State(component_id='persistence_narrative', component_property='data'),
    prevent_initial_call=True
)
def func(value_cf, value_cs, value_ct, value_cm, data):
    data_narrative = json.loads(data)
    if ctx.triggered_id == 'text_area_campanha_filhos':
        data_narrative['Visao Campanhas']['Efetividade da Campanha x Numeros de Filhos'] = value_cf
    elif ctx.triggered_id == 'text_area_campanha_salario':
        data_narrative['Visao Campanhas']['Efetividade da Campanha x Media Salarial'] = value_cs
    elif ctx.triggered_id == 'text_area_campanha_table':
        data_narrative['Visao Campanhas']['Campanha Table'] = value_ct
    elif ctx.triggered_id == 'text_area_campanha_marketing':
        data_narrative['Visao Campanhas']['Resultado das Campanhas de Marketing'] = value_cm

    return json.dumps(data_narrative)


# ---------------------------------------------------Persistence Figure-------------------------------------------------

@dash.get_app().callback(
    Output(component_id='persistence_figure', component_property='data', allow_duplicate=True),
    [
        Input(component_id='graph_efetividade_campanha_filhos', component_property='figure'),
        Input(component_id='graph_media_salario_campanha', component_property='figure'),
        Input(component_id='graph_resultado_campanha', component_property='figure'),
        Input(component_id='table_visitas_web_site', component_property='columns'),
        Input(component_id='table_visitas_web_site', component_property='data')
    ],
    State(component_id='persistence_figure', component_property='data'),
    prevent_initial_call=True
)
def func(fig1, fig2, fig3, cols, t_data, data):
    data_figure = json.loads(data)
    data_figure['Visao Campanhas']['Efetividade da Campanha x Numeros de Filhos'] = fig1
    data_figure['Visao Campanhas']['Efetividade da Campanha x Media Salarial'] = fig2
    data_figure['Visao Campanhas']['Resultado das Campanhas de Marketing'] = fig3
    data_figure['Visao Campanhas']['Campanha Table'] = {
        "Columns": [i['name'] for i in cols],
        "Values": [list(i.values()) for i in t_data]
    }

    return json.dumps(data_figure)

