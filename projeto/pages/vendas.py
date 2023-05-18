from dash import (
    html,
    Input,
    Output,
    State,
    dcc,
    callback,
    ctx,
    exceptions
)
import dash
import dash_bootstrap_components as dbc
import plotly.graph_objects as go
import pandas as pd
import numpy as np
import json
import logging

from utils import (
    response_modal_prompt_narrative,
    save_json_prompt,
    modal_historic_narrative,
    create_narrative,
    create_false_narrative
)


dash.register_page(__name__, path='/visao_pontos_vendas')

layout = html.Div(children=[
    dbc.Card([
        dbc.CardBody([
            dbc.Row([
                dbc.Col([
                    dbc.Card([
                        dbc.CardHeader([
                            dbc.Row([
                                dbc.Col([
                                    html.Label('Total Gasto em Diferentes Categorias por País')
                                ], md=10),
                                dbc.Col([
                                    dbc.DropdownMenu([
                                        dbc.DropdownMenuItem(
                                            'Criar Narrativa', n_clicks=0, id='create_narrative_gasto_categoria_pais'
                                        ),
                                        dbc.DropdownMenuItem(
                                            'Editar Prompt de Narrativa', n_clicks=0,
                                            id='edit_prompt_narrative_gasto_categoria_pais'
                                        ),
                                        dbc.DropdownMenuItem(
                                            'Historico de Narrativa', n_clicks=0,
                                            id='historico_narrative_gasto_categoria_pais'
                                        ),
                                        dbc.DropdownMenuItem(
                                            'Caixa de Narrativa', n_clicks=0, id='caixa_narrativa_gasto_categoria_pais'
                                        )
                                    ], label='Menu')
                                ], md=2)
                            ])
                        ]),
                        dbc.CardBody([
                            dcc.Graph(id='graph_gastos_pais')
                        ]),
                        dbc.CardFooter([
                            dcc.Loading(
                                type='dot',
                                children=[
                                    dbc.Toast(
                                        children=[
                                            dbc.Textarea(
                                                className="mb-3", size='md', rows=10,
                                                id='text_area_gasto_categoria_pais'
                                            )
                                        ],
                                        header='Narrativa', dismissable=True, style={'width': '100%'},
                                        is_open=False, id='toast_narrative_gasto_categoria_pais'
                                    )
                                ], color='#636EFA', style={'margin-top': '5px'}
                            )
                        ])
                    ])
                ])
            ]),
            dbc.Row([
                dbc.Col([
                    dbc.Card([
                        dbc.CardHeader([
                            dbc.Row([
                                dbc.Col([
                                    html.Label('Total Gasto por Ano e País')
                                ], md=10),
                                dbc.Col([
                                    dbc.DropdownMenu([
                                        dbc.DropdownMenuItem(
                                            'Criar Narrativa', n_clicks=0, id='create_narrative_gasto_ano_pais'
                                        ),
                                        dbc.DropdownMenuItem(
                                            'Editar Prompt de Narrativa', n_clicks=0,
                                            id='edit_prompt_narrative_gasto_ano_pais'
                                        ),
                                        dbc.DropdownMenuItem(
                                            'Historico de Narrativa', n_clicks=0,
                                            id='historico_narrative_gasto_ano_pais'
                                        ),
                                        dbc.DropdownMenuItem(
                                            'Caixa de Narrativa', n_clicks=0, id='caixa_narrativa_gasto_ano_pais'
                                        )
                                    ], label='Menu')
                                ], md=2)
                            ])
                        ]),
                        dbc.CardBody([
                            dcc.Graph(id='graph_gasto_ano_pais')
                        ]),
                        dbc.CardFooter([
                            dcc.Loading(
                                type='dot',
                                children=[
                                    dbc.Toast(
                                        children=[
                                            dbc.Textarea(
                                                className="mb-3", size='md', rows=10,
                                                id='text_area_gasto_ano_pais'
                                            )
                                        ],
                                        header='Narrativa', dismissable=True, style={'width': '100%'},
                                        is_open=False, id='toast_narrative_gasto_ano_pais'
                                    )
                                ], color='#636EFA', style={'margin-top': '5px'}
                            )
                        ])
                    ])
                ])
            ], style={'margin-top': '10px'})
        ])
    ]),
    dbc.Modal([
        dbc.ModalHeader('Editar Prompt da Narrativa'),
        dbc.ModalBody([
            dbc.Textarea(
                className="mb-3", placeholder="A Textarea", id='textarea_edit_prompt_narrative_gasto_categoria_pais',
                size='md', rows=3
            ),
            html.Div(id='table_edit_narrative_gasto_categoria_pais', style={'margin-top': '15px'}),
            html.Div(
                dbc.Button('Salvar', color='success', n_clicks=0, id='button_save_narrative_gasto_categoria_pais'),
                style={'margin-top': '15px'}
            )
        ]),
        dbc.ModalFooter([
            html.Div(id='alert_edit_narrative_gasto_categoria_pais')
        ], style={'justify-content': 'center'})
    ], id='modal_edit_narrative_gasto_categoria_pais', is_open=False, size='lg'),
    dbc.Modal([
        dbc.ModalHeader(dbc.ModalTitle('Historico de Narrativas')),
        dbc.ModalBody([html.Div(id='div_historico_gasto_categoria_pais')])
    ], id='modal_historico_narrativa_gasto_categoria_pais', is_open=False, size='lg'),
    dbc.Modal([
        dbc.ModalHeader('Editar Prompt da Narrativa'),
        dbc.ModalBody([
            dbc.Textarea(
                className="mb-3", placeholder="A Textarea", id='textarea_edit_prompt_narrative_gasto_ano_pais',
                size='md', rows=3
            ),
            html.Div(id='table_edit_narrative_gasto_ano_pais', style={'margin-top': '15px'}),
            html.Div(
                dbc.Button('Salvar', color='success', n_clicks=0, id='button_save_narrative_gasto_ano_pais'),
                style={'margin-top': '15px'}
            )
        ]),
        dbc.ModalFooter([
            html.Div(id='alert_edit_narrative_gasto_ano_pais')
        ], style={'justify-content': 'center'})
    ], id='modal_edit_narrative_gasto_ano_pais', is_open=False, size='lg'),
    dbc.Modal([
        dbc.ModalHeader(dbc.ModalTitle('Historico de Narrativas')),
        dbc.ModalBody([html.Div(id='div_historico_gasto_ano_pais')])
    ], id='modal_historico_narrativa_gasto_ano_pais', is_open=False, size='lg')
])


# ----------------------------------------------------------Gráficos----------------------------------------------------


@callback(
    Output(component_id='graph_gastos_pais', component_property='figure'),
    Input(component_id='data_marketing', component_property='data')
)
def func(data_marketing):
    dframe = pd.read_json(data_marketing, orient='split')
    _ = dframe.groupby(by='Pais').agg({k: np.sum for k in dframe.filter(regex='^Gasto').columns})
    fig = go.Figure()

    for g in _.columns:
        fig.add_trace(go.Bar(name=g.split(' ')[-1], x=_.index, y=_[g]))

    fig.update_layout(
        margin=dict(l=0, r=0, t=0, b=0), legend=dict(orientation='h', yanchor='top', y=1.09, xanchor='left', x=0),
        xaxis={'categoryorder': 'total descending'}, height=350
    )

    return fig


@callback(
    Output(component_id='graph_gasto_ano_pais', component_property='figure'),
    Input(component_id='data_marketing', component_property='data')
)
def func(data_marketing):
    dframe = pd.read_json(data_marketing, orient='split')
    _ = dframe.groupby(by=['Pais', 'Ano Cadastro']).agg({'Total Gasto': np.sum})
    fig = go.Figure()

    for pais in _.index.get_level_values('Pais').unique():
        fig.add_trace(
            go.Scatter(mode='lines+markers', name=pais, x=_.loc[pais].index,
                       y=_.loc[pais]['Total Gasto'])
        )
    fig.update_layout(
        margin=dict(l=0, r=0, t=0, b=0), legend=dict(orientation='h', yanchor='top', y=1.09, xanchor='left', x=0),
        height=350
    )

    return fig


# ------------------------------------------------------Narrativa-------------------------------------------------------


# -----------------------------------------Total Gasto em Diferentes Categorias por Pais--------------------------------


# Criação da narrativa
@callback(
    [
        Output(component_id='text_area_gasto_categoria_pais', component_property='value'),
        Output(component_id='toast_narrative_gasto_categoria_pais', component_property='is_open')
    ],
    [
        Input(component_id='create_narrative_gasto_categoria_pais', component_property='n_clicks'),
        Input(component_id='caixa_narrativa_gasto_categoria_pais', component_property='n_clicks')
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
    if ctx.triggered_id == 'create_narrative_gasto_categoria_pais':
        dframe = pd.read_json(data_marketing, orient='split')

        _ = dframe.groupby(by='Pais', as_index=False).agg({k: np.sum for k in dframe.filter(regex='^Gasto').columns})
        for c in _.columns[1:]:
            _.insert(
                loc=_.columns.get_loc(c) + 1,
                column='Percentual ' + c,
                value=(_[c] / dframe['Total Gasto'].sum()) * 100
            )
        _ = _.round(decimals=2)
        narrative = create_narrative(_.to_csv(index=False), 'total gasto em diferentes categorias por pais')
        # narrative = create_false_narrative('total gasto em diferentes categorias por pais')
        return narrative, True
    elif ctx.triggered_id == 'caixa_narrativa_gasto_categoria_pais':
        return '', True
    elif data_toast['Visao Pontos de Vendas']['Total Gasto em Diferentes Categorias por Pais']:
        value = data_narrative['Visao Pontos de Vendas']['Total Gasto em Diferentes Categorias por Pais']
        return value, True
    else:
        raise exceptions.PreventUpdate


# Cria o modal de edição de narrativa
@callback(
    [
        Output(component_id='modal_edit_narrative_gasto_categoria_pais', component_property='is_open'),
        Output(component_id='textarea_edit_prompt_narrative_gasto_categoria_pais', component_property='value'),
        Output(component_id='table_edit_narrative_gasto_categoria_pais', component_property='children')
    ],
    Input(component_id='edit_prompt_narrative_gasto_categoria_pais', component_property='n_clicks'),
    State(component_id='data_marketing', component_property='data')
)
def func(n_click, data_marketing):
    if n_click:
        dframe = pd.read_json(data_marketing, orient='split')
        _ = dframe.groupby(by='Pais', as_index=False).agg({k: np.sum for k in dframe.filter(regex='^Gasto').columns})

        try:
            response = response_modal_prompt_narrative(_, 'total gasto em diferentes categorias por pais')
        except Exception as msg:
            logging.exception(msg)
            raise exceptions.PreventUpdate
        else:
            return response
    else:
        raise exceptions.PreventUpdate


# Salva o arquivo json com o prompt
@callback(
    Output(component_id='alert_edit_narrative_gasto_categoria_pais', component_property='children'),
    Input(component_id='button_save_narrative_gasto_categoria_pais', component_property='n_clicks'),
    State(component_id='textarea_edit_prompt_narrative_gasto_categoria_pais', component_property='value')
)
def func(n_click, value):
    if n_click:
        return save_json_prompt('total gasto em diferentes categorias por pais', value)
    else:
        raise exceptions.PreventUpdate


# Modal historico de narrativas
@callback(
    [
        Output(component_id='modal_historico_narrativa_gasto_categoria_pais', component_property='is_open'),
        Output(component_id='div_historico_gasto_categoria_pais', component_property='children')
    ],
    Input(component_id='historico_narrative_gasto_categoria_pais', component_property='n_clicks')
)
def fun(n_click):
    if n_click:
        try:
            response = modal_historic_narrative('total gasto em diferentes categorias por pais')
        except Exception as msg:
            logging.exception(msg)
            raise exceptions.PreventUpdate
        else:
            return response
    else:
        raise exceptions.PreventUpdate


# ----------------------------------------------Total Gasto por Ano e Pais----------------------------------------------


# Criação da narrativa
@callback(
    [
        Output(component_id='text_area_gasto_ano_pais', component_property='value'),
        Output(component_id='toast_narrative_gasto_ano_pais', component_property='is_open')
    ],
    [
        Input(component_id='create_narrative_gasto_ano_pais', component_property='n_clicks'),
        Input(component_id='caixa_narrativa_gasto_ano_pais', component_property='n_clicks')
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
    if ctx.triggered_id == 'create_narrative_gasto_ano_pais':
        dframe = pd.read_json(data_marketing, orient='split')

        _ = dframe.groupby(by=['Pais', 'Ano Cadastro'], as_index=False).agg({'Total Gasto': np.sum})
        _['Percentual Total Gasto'] = (_['Total Gasto'] / _['Total Gasto'].sum()) * 100
        _ = _.round(decimals=2)

        narrative = create_narrative(_.to_csv(index=False), 'total gasto por ano e pais')
        # narrative = create_false_narrative('total gasto por ano e pais')
        return narrative, True
    elif ctx.triggered_id == 'caixa_narrativa_gasto_ano_pais':
        return '', True
    elif data_toast['Visao Pontos de Vendas']['Total Gasto por Ano e Pais']:
        value = data_narrative['Visao Pontos de Vendas']['Total Gasto por Ano e Pais']
        return value, True
    else:
        raise exceptions.PreventUpdate


# Cria o modal de edição de narrativa
@callback(
    [
        Output(component_id='modal_edit_narrative_gasto_ano_pais', component_property='is_open'),
        Output(component_id='textarea_edit_prompt_narrative_gasto_ano_pais', component_property='value'),
        Output(component_id='table_edit_narrative_gasto_ano_pais', component_property='children')
    ],
    Input(component_id='edit_prompt_narrative_gasto_ano_pais', component_property='n_clicks'),
    State(component_id='data_marketing', component_property='data')
)
def func(n_click, data_marketing):
    if n_click:
        dframe = pd.read_json(data_marketing, orient='split')
        _ = dframe.groupby(by=['Pais', 'Ano Cadastro'], as_index=False).agg({'Total Gasto': np.sum})

        try:
            response = response_modal_prompt_narrative(_, 'total gasto por ano e pais')
        except Exception as msg:
            logging.exception(msg)
            raise exceptions.PreventUpdate
        else:
            return response
    else:
        raise exceptions.PreventUpdate


# Salva o arquivo json com o prompt
@callback(
    Output(component_id='alert_edit_narrative_gasto_ano_pais', component_property='children'),
    Input(component_id='button_save_narrative_gasto_ano_pais', component_property='n_clicks'),
    State(component_id='textarea_edit_prompt_narrative_gasto_ano_pais', component_property='value')
)
def func(n_click, value):
    if n_click:
        return save_json_prompt('total gasto por ano e pais', value)
    else:
        raise exceptions.PreventUpdate


# Modal historico de narrativas
@callback(
    [
        Output(component_id='modal_historico_narrativa_gasto_ano_pais', component_property='is_open'),
        Output(component_id='div_historico_gasto_ano_pais', component_property='children')
    ],
    Input(component_id='historico_narrative_gasto_ano_pais', component_property='n_clicks')
)
def fun(n_click):
    if n_click:
        try:
            response = modal_historic_narrative('total gasto por ano e pais')
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
        Input(component_id='toast_narrative_gasto_categoria_pais', component_property='is_open'),
        Input(component_id='toast_narrative_gasto_ano_pais', component_property='is_open')
    ],
    State(component_id='persistence_toast', component_property='data'),
    prevent_initial_call=True
)
def func(open_gc, open_ga, data):
    data_toast = json.loads(data)
    if ctx.triggered_id == 'toast_narrative_gasto_categoria_pais':
        data_toast['Visao Pontos de Vendas']['Total Gasto em Diferentes Categorias por Pais'] = open_gc
    elif ctx.triggered_id == 'toast_narrative_gasto_ano_pais':
        data_toast['Visao Pontos de Vendas']['Total Gasto por Ano e Pais'] = open_ga

    return json.dumps(data_toast)


# --------------------------------------------------Persistence Narrative-----------------------------------------------


@dash.get_app().callback(
    Output(component_id='persistence_narrative', component_property='data', allow_duplicate=True),
    [
        Input(component_id='text_area_gasto_categoria_pais', component_property='value'),
        Input(component_id='text_area_gasto_ano_pais', component_property='value')
    ],
    State(component_id='persistence_narrative', component_property='data'),
    prevent_initial_call=True
)
def func(value_gc, value_ga, data):
    data_narrative = json.loads(data)
    if ctx.triggered_id == 'text_area_gasto_categoria_pais':
        data_narrative['Visao Pontos de Vendas']['Total Gasto em Diferentes Categorias por Pais'] = value_gc
    elif ctx.triggered_id == 'text_area_gasto_ano_pais':
        data_narrative['Visao Pontos de Vendas']['Total Gasto por Ano e Pais'] = value_ga

    return json.dumps(data_narrative)


# ---------------------------------------------------Persistence Figure-------------------------------------------------

@dash.get_app().callback(
    Output(component_id='persistence_figure', component_property='data', allow_duplicate=True),
    [
        Input(component_id='graph_gastos_pais', component_property='figure'),
        Input(component_id='graph_gasto_ano_pais', component_property='figure')
    ],
    State(component_id='persistence_figure', component_property='data'),
    prevent_initial_call=True
)
def func(fig1, fig2, data):
    data_figure = json.loads(data)
    data_figure['Visao Pontos de Vendas']['Total Gasto em Diferentes Categorias por Pais'] = fig1
    data_figure['Visao Pontos de Vendas']['Total Gasto por Ano e Pais'] = fig2

    return json.dumps(data_figure)

