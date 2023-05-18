import dash
from dash import dcc, callback, Input, Output, State, exceptions, ctx
import locale

from utils import *


locale.setlocale(locale.LC_ALL, '')

dash.register_page(__name__, path='/')


layout = html.Div(children=[
    dbc.Card([
        dbc.CardHeader([
            dbc.Row([
                dbc.Col([
                    dbc.Tabs(
                        [
                            dbc.Tab(label='Todos', tab_id='tab_todos_paises')
                        ] +
                        [
                            dbc.Tab(label=pais, tab_id='tab_' + pais)
                            for pais in ['Argentina', 'Alemanha', 'Brasil', 'Chile', 'Espanha', 'Estados Unidos', 'Portugal']
                        ], id='tab_paises', active_tab='tab_todos_paises'
                    )
                ], xl=11, lg=10, md=10)
            ])
        ]),
        dbc.CardBody([
            dbc.Row([
                dbc.Col([
                    dbc.Card([
                        dbc.CardHeader('Total de Clientes'),
                        dbc.CardBody([html.Label(id='info_total_cliente')])
                    ])
                ], md=2),
                dbc.Col([
                    dbc.Card([
                        dbc.CardHeader('Média de Sálario'),
                        dbc.CardBody([html.Label(id='info_media_salario')])
                    ])
                ], md=2),
                dbc.Col([
                    dbc.Card([
                        dbc.CardHeader('Compras na Web'),
                        dbc.CardBody([html.Label(id='info_compras_web')])
                    ])
                ], md=2),
                dbc.Col([
                    dbc.Card([
                        dbc.CardHeader('Compras na Loja'),
                        dbc.CardBody([html.Label(id='info_compras_loja')])
                    ])
                ], md=2),
                dbc.Col([
                    dbc.Card([
                        dbc.CardHeader('Compras Via Catalago'),
                        dbc.CardBody([html.Label(id='info_compras_catalogo')])
                    ])
                ], md=2),
                dbc.Col([
                    dbc.Card([
                        dbc.CardHeader('Compras Com Desconto'),
                        dbc.CardBody([html.Label(id='info_compras_desconto')])
                    ])
                ], md=2)
            ]),
            dbc.Row([
                dbc.Col([
                    dbc.Card([
                        dbc.CardHeader([
                            dbc.Row([
                                dbc.Col([
                                    html.Label('Total de Clientes por Escolaridade')
                                ], md=10),
                                dbc.Col([
                                    dbc.DropdownMenu([
                                        dbc.DropdownMenuItem(
                                            'Criar Narrativa', id='create_narrative_total_escolaridade', n_clicks=0
                                        ),
                                        dbc.DropdownMenuItem(
                                            'Editar Prompt de Narrativa',
                                            id='edit_prompt_narrative_total_escolaridade', n_clicks=0
                                        ),
                                        dbc.DropdownMenuItem(
                                            'Historico de Narrativa', id='historico_narrative_total_escolaridade',
                                            n_clicks=0
                                        ),
                                        dbc.DropdownMenuItem(
                                            'Caixa de Narrativa', id='caixa_narrativa_total_escolaridade',
                                            n_clicks=0
                                        )
                                    ], label='Menu')
                                ], md=2)
                            ])
                        ]),
                        dbc.CardBody([dcc.Graph(id='graph_total_escolaridade')]),
                        dbc.CardFooter([
                            dcc.Loading(
                                type='dot',
                                children=[
                                    dbc.Toast(
                                        children=[
                                            dbc.Textarea(
                                                className="mb-3", size='md', rows=10, id='text_area_escolaridade'
                                            )
                                        ],
                                        header='Narrativa', dismissable=True, style={'width': '100%'},
                                        is_open=False, id='toast_narrative_escolaridade'
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
                                dbc.Col([dbc.Label('Total de Clientes por Estado Civil')], md=10),
                                dbc.Col([
                                    dbc.DropdownMenu([
                                        dbc.DropdownMenuItem(
                                            'Criar Narrativa', id='create_narrative_total_civil', n_clicks=0
                                        ),
                                        dbc.DropdownMenuItem(
                                            'Editar Prompt de Narrativa',
                                            id='edit_prompt_narrative_total_civil', n_clicks=0
                                        ),
                                        dbc.DropdownMenuItem(
                                            'Historico de Narrativa', id='historico_narrative_total_civil',
                                            n_clicks=0
                                        ),
                                        dbc.DropdownMenuItem(
                                            'Caixa de Narrativa', id='caixa_narrativa_total_civil',
                                            n_clicks=0
                                        )
                                    ], label='Menu')
                                ], md=2)
                            ])
                        ]),
                        dbc.CardBody([dcc.Graph(id='graph_clientes_total_civil')]),
                        dbc.CardFooter([
                            dcc.Loading(
                                type='dot',
                                children=[
                                    dbc.Toast(
                                        children=[
                                            dbc.Textarea(
                                                className="mb-3", size='md', rows=10, id='text_area_total_civil'
                                            )
                                        ],
                                        header='Narrativa', dismissable=True, style={'width': '100%'}, is_open=False,
                                        id='toast_narrative_total_civil'
                                    )
                                ], color='#636EFA', style={'margin-top': '5px'}
                            )
                        ])
                    ])
                ], md=6)
            ], style={'margin-top': '10px'}),
            dbc.Row([
                dbc.Col([
                    dbc.Card([
                        dbc.CardHeader([
                            dbc.Row([
                                dbc.Col([dbc.Label('Total de Clientes por País')], md=10),
                                dbc.Col([
                                    dbc.DropdownMenu([
                                        dbc.DropdownMenuItem(
                                            'Criar Narrativa', id='create_narrative_total_pais', n_clicks=0
                                        ),
                                        dbc.DropdownMenuItem(
                                            'Editar Prompt de Narrativa',
                                            id='edit_prompt_narrative_total_pais', n_clicks=0
                                        ),
                                        dbc.DropdownMenuItem(
                                            'Historico de Narrativa', id='historico_narrative_total_pais',
                                            n_clicks=0
                                        ),
                                        dbc.DropdownMenuItem(
                                            'Caixa de Narrativa', id='caixa_narrativa_total_pais',
                                            n_clicks=0
                                        )
                                    ], label='Menu')
                                ], md=2)
                            ])
                        ]),
                        dbc.CardBody([dcc.Graph(id='graph_clientes_total_pais')]),
                        dbc.CardFooter([
                            dcc.Loading(
                                type='dot',
                                children=[
                                    dbc.Toast(
                                        children=[
                                            dbc.Textarea(
                                                className="mb-3", size='md', rows=10, id='text_area_total_pais'
                                            )
                                        ],
                                        header='Narrativa', dismissable=True, style={'width': '100%'}, is_open=False,
                                        id='toast_narrative_total_pais'
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
                                dbc.Col([dbc.Label('Total de Clientes por Filhos em Casa')], md=10),
                                dbc.Col([
                                    dbc.DropdownMenu([
                                        dbc.DropdownMenuItem(
                                            'Criar Narrativa', id='create_narrative_total_filhos', n_clicks=0
                                        ),
                                        dbc.DropdownMenuItem(
                                            'Editar Prompt de Narrativa',
                                            id='edit_prompt_narrative_total_filhos', n_clicks=0
                                        ),
                                        dbc.DropdownMenuItem(
                                            'Historico de Narrativa', id='historico_narrative_total_filhos',
                                            n_clicks=0
                                        ),
                                        dbc.DropdownMenuItem(
                                            'Caixa de Narrativa', id='caixa_narrativa_total_filhos',
                                            n_clicks=0
                                        )
                                    ], label='Menu')
                                ], md=2)
                            ])
                        ]),
                        dbc.CardBody(dcc.Graph(id='graph_clientes_total_filhos')),
                        dbc.CardFooter([
                            dcc.Loading(
                                type='dot',
                                children=[
                                    dbc.Toast(
                                        children=[
                                            dbc.Textarea(
                                                className="mb-3", size='md', rows=10, id='text_area_total_filhos'
                                            )
                                        ],
                                        header='Narrativa', dismissable=True, style={'width': '100%'}, is_open=False,
                                        id='toast_narrative_total_filhos'
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
                className="mb-3", placeholder="A Textarea", id='textarea_edit_prompt_narrative_total_escolaridade',
                size='md', rows=3
            ),
            html.Div(id='table_edit_narrative_total_escolaridade', style={'margin-top': '15px'}),
            html.Div(
                dbc.Button('Salvar', color='success', n_clicks=0, id='button_save_narrative_total_escolaridade'),
                style={'margin-top': '15px'}
            )
        ]),
        dbc.ModalFooter([
            html.Div(id='alert_edit_narrative_total_escolaridade')
        ], style={'justify-content': 'center'})
    ], id='modal_edit_narrative_total_escolaridade', is_open=False, size='lg'),
    dbc.Modal([
        dbc.ModalHeader(dbc.ModalTitle('Historico de Narrativas')),
        dbc.ModalBody([html.Div(id='div_historico_total_escolaridade')])
    ], id='modal_historico_narrativa_total_escolaridade', is_open=False, size='lg'),
    dbc.Modal([
        dbc.ModalHeader('Editar Prompt da Narrativa'),
        dbc.ModalBody([
            dbc.Textarea(
                className="mb-3", placeholder="A Textarea", id='textarea_edit_prompt_narrative_total_civil',
                size='md', rows=3
            ),
            html.Div(id='table_edit_narrative_total_civil', style={'margin-top': '15px'}),
            html.Div(
                dbc.Button('Salvar', color='success', n_clicks=0, id='button_save_narrative_total_civil'),
                style={'margin-top': '15px'}
            )
        ]),
        dbc.ModalFooter([
            html.Div(id='alert_edit_narrative_total_civil')
        ], style={'justify-content': 'center'})
    ], id='modal_edit_narrative_total_civil', is_open=False, size='lg'),
    dbc.Modal([
        dbc.ModalHeader('Historico de Narrativas'),
        dbc.ModalBody([html.Div(id='div_historico_total_civil')])
    ], id='modal_historico_narrativa_total_civil', is_open=False, size='lg'),
    dbc.Modal([
        dbc.ModalHeader('Editar Prompt da Narrativa'),
        dbc.ModalBody([
            dbc.Textarea(
                className="mb-3", placeholder="A Textarea", id='textarea_edit_prompt_narrative_total_pais',
                size='md', rows=3
            ),
            html.Div(id='table_edit_narrative_total_pais', style={'margin-top': '15px'}),
            html.Div(
                dbc.Button('Salvar', color='success', n_clicks=0, id='button_save_narrative_total_pais'),
                style={'margin-top': '15px'}
            )
        ]),
        dbc.ModalFooter([
            html.Div(id='alert_edit_narrative_total_pais')
        ], style={'justify-content': 'center'})
    ], id='modal_edit_narrative_total_pais', is_open=False, size='lg'),
    dbc.Modal([
        dbc.ModalHeader('Historico de Narrativas'),
        dbc.ModalBody([html.Div(id='div_historico_total_pais')])
    ], id='modal_historico_narrativa_total_pais', is_open=False, size='lg'),
    dbc.Modal([
        dbc.ModalHeader('Editar Prompt da Narrativa'),
        dbc.ModalBody([
            dbc.Textarea(
                className="mb-3", placeholder="A Textarea", id='textarea_edit_prompt_narrative_total_filhos',
                size='md', rows=3
            ),
            html.Div(id='table_edit_narrative_total_filhos', style={'margin-top': '15px'}),
            html.Div(
                dbc.Button('Salvar', color='success', n_clicks=0, id='button_save_narrative_total_filhos'),
                style={'margin-top': '15px'}
            )
        ]),
        dbc.ModalFooter([
            html.Div(id='alert_edit_narrative_total_filhos')
        ], style={'justify-content': 'center'})
    ], id='modal_edit_narrative_total_filhos', is_open=False, size='lg'),
    dbc.Modal([
        dbc.ModalHeader('Historico de Narrativas'),
        dbc.ModalBody([html.Div(id='div_historico_total_filhos')])
    ], id='modal_historico_narrativa_total_filhos', is_open=False, size='lg')
])


# Cards de Indicadores
@callback(
    [
        Output(component_id='info_total_cliente', component_property='children'),
        Output(component_id='info_media_salario', component_property='children'),
        Output(component_id='info_compras_web', component_property='children'),
        Output(component_id='info_compras_loja', component_property='children'),
        Output(component_id='info_compras_catalogo', component_property='children'),
        Output(component_id='info_compras_desconto', component_property='children')
    ],
    Input(component_id='tab_paises', component_property='active_tab'),
    State(component_id='data_marketing', component_property='data')
)
def func(active_tab, data):
    dframe = read_df_and_select_pais(data, active_tab)
    return [
        locale.format_string('%d', dframe['ID'].count(), grouping=True),
        'R$ ' + locale.format_string('%.2f', round(dframe['Salario Anual'].mean(), 2), grouping=True),
        locale.format_string('%d', dframe['Numero de Compras na Web'].sum(), grouping=True),
        locale.format_string('%d', dframe['Numero de Compras na Loja'].sum(), grouping=True),
        locale.format_string('%d', dframe['Numero de Compras via Catalogo'].sum(), grouping=True),
        locale.format_string('%d', dframe['Numero de Compras com Desconto'].sum(), grouping=True)
    ]

# -----------------------------------------------------Gráficos---------------------------------------------------------


# Gráfico clientes por escolaridade
@callback(
    Output(component_id='graph_total_escolaridade', component_property='figure'),
    Input(component_id='tab_paises', component_property='active_tab'),
    State(component_id='data_marketing', component_property='data')
)
def func(active_tab, data):
    dframe = read_df_and_select_pais(data, active_tab)
    _ = (
        dframe.groupby(by=['Escolaridade'], as_index=False).agg({'ID': 'count'})
        .rename(mapper={'ID': 'Total de Clientes'}, axis=1)
    )

    return Graphs.Bar(_['Escolaridade'], _['Total de Clientes'], text=_['Total de Clientes'], height=300)


# Gráfico clientes por estado civil
@callback(
    Output(component_id='graph_clientes_total_civil', component_property='figure'),
    Input(component_id='tab_paises', component_property='active_tab'),
    State(component_id='data_marketing', component_property='data')
)
def func(active_tab, data):
    dframe = read_df_and_select_pais(data, active_tab)

    _ = (
        dframe.groupby(by=['Estado Civil'], as_index=False).agg({'ID': 'count'})
        .rename(mapper={'ID': 'Total de Clientes'}, axis=1)
    )
    return Graphs.Bar(_['Estado Civil'], _['Total de Clientes'], text=_['Total de Clientes'], height=300)


@callback(
    Output(component_id='graph_clientes_total_pais', component_property='figure'),
    Input(component_id='data_marketing', component_property='data')
)
def func(data):
    dframe = pd.read_json(data, orient='split', convert_dates=['Data Cadastro'])

    _ = (
        dframe.groupby(by=['Pais'], as_index=False).agg({'ID': 'count'})
        .rename(mapper={'ID': 'Total de Clientes'}, axis=1)
    )
    _['Pais'] = _['Pais'].apply(lambda x: x if x != 'Estados Unidos' else 'EUA')
    return Graphs.BarH(_['Total de Clientes'], _['Pais'], text=_['Total de Clientes'], height=300)


@callback(
    Output(component_id='graph_clientes_total_filhos', component_property='figure'),
    Input(component_id='tab_paises', component_property='active_tab'),
    State(component_id='data_marketing', component_property='data')
)
def func(active_tab, data):
    dframe = read_df_and_select_pais(data, active_tab)
    _ = (
        dframe.groupby(by=['Filhos em Casa'], as_index=False).agg({'ID': 'count'})
        .rename(mapper={'ID': 'Total de Clientes'}, axis=1)
    )
    return Graphs.Bar(_['Filhos em Casa'], _['Total de Clientes'], text=_['Total de Clientes'], height=300)

# ------------------------------------------------------Narrativa-------------------------------------------------------

# -----------------------------------------------Clientes Por Escolaridade----------------------------------------------


# Criação da narrativa
@callback(
    [
        Output(component_id='text_area_escolaridade', component_property='value'),
        Output(component_id='toast_narrative_escolaridade', component_property='is_open')
    ],
    [
        Input(component_id='create_narrative_total_escolaridade', component_property='n_clicks'),
        Input(component_id='caixa_narrativa_total_escolaridade', component_property='n_clicks')
    ],
    [
        State(component_id='tab_paises', component_property='active_tab'),
        State(component_id='data_marketing', component_property='data'),
        State(component_id='persistence_narrative', component_property='data'),
        State(component_id='persistence_toast', component_property='data')
    ]
)
def func(n1, n2, active_tab, data_marketing, d_narrative, d_toast):
    data_narrative = json.loads(d_narrative)
    data_toast = json.loads(d_toast)
    if ctx.triggered_id == 'create_narrative_total_escolaridade':
        dframe = read_df_and_select_pais(data_marketing, active_tab)

        _ = (
            dframe.groupby(by=['Escolaridade'], as_index=False).agg({'ID': 'count'})
            .rename(mapper={'ID': 'Total de Clientes'}, axis=1)
        )
        _['Porcentagem de Clientes'] = (_['Total de Clientes'] / dframe.shape[0]) * 100
        _ = _.round(decimals=2)
        narrative = create_narrative(_.to_csv(index=False), 'total de clientes por escolaridade')
        # narrative = create_false_narrative('total de clientes por escolaridade')
        return narrative, True
    elif ctx.triggered_id == 'caixa_narrativa_total_escolaridade':
        return '', True
    elif data_toast['Visao Clientes']['Total de Clientes Por Escolaridade']:
        value = data_narrative['Visao Clientes']['Total de Clientes Por Escolaridade']
        return value, True
    else:
        raise exceptions.PreventUpdate


# cria o modal de edição de prompt da narrativa
@callback(
    [
        Output(component_id='modal_edit_narrative_total_escolaridade', component_property='is_open'),
        Output(component_id='textarea_edit_prompt_narrative_total_escolaridade', component_property='value'),
        Output(component_id='table_edit_narrative_total_escolaridade', component_property='children')
    ],
    Input(component_id='edit_prompt_narrative_total_escolaridade', component_property='n_clicks'),
    [
        State(component_id='tab_paises', component_property='active_tab'),
        State(component_id='data_marketing', component_property='data')
    ]
)
def func(n_click, active_tab, data):
    if n_click:
        dframe = read_df_and_select_pais(data, active_tab)

        _ = (
            dframe.groupby(by=['Escolaridade'], as_index=False).agg({'ID': 'count'})
            .rename(mapper={'ID': 'Total de Clientes'}, axis=1)
        )

        try:
            response = response_modal_prompt_narrative(_, 'total de clientes por escolaridade')
        except Exception:
            logging.exception('Não foi possivel ler o arquivo que armazena o prompt')
            raise exceptions.PreventUpdate
        else:
            return response
    else:
        raise exceptions.PreventUpdate


# Salva o arquivo json com o prompt
@callback(
    Output(component_id='alert_edit_narrative_total_escolaridade', component_property='children'),
    Input(component_id='button_save_narrative_total_escolaridade', component_property='n_clicks'),
    State(component_id='textarea_edit_prompt_narrative_total_escolaridade', component_property='value')
)
def func(n_click, value):
    if n_click:
        return save_json_prompt('total de clientes por escolaridade', value)
    else:
        raise exceptions.PreventUpdate


# Modal historico de narrativas
@callback(
    [
        Output(component_id='modal_historico_narrativa_total_escolaridade', component_property='is_open'),
        Output(component_id='div_historico_total_escolaridade', component_property='children')
    ],
    Input(component_id='historico_narrative_total_escolaridade', component_property='n_clicks')
)
def fun(n_click):
    if n_click:
        try:
            response = modal_historic_narrative('total de clientes por escolaridade')
        except Exception:
            logging.exception('Houve um erro ao tentar acessar o historico!')
            raise exceptions.PreventUpdate
        else:
            return response
    else:
        raise exceptions.PreventUpdate

# -------------------------------------------------Clientes por Estado Civil--------------------------------------------


# Criação da narrativa
@callback(
    [
        Output(component_id='text_area_total_civil', component_property='value'),
        Output(component_id='toast_narrative_total_civil', component_property='is_open')
    ],
    [
        Input(component_id='create_narrative_total_civil', component_property='n_clicks'),
        Input(component_id='caixa_narrativa_total_civil', component_property='n_clicks')
    ],
    [
        State(component_id='tab_paises', component_property='active_tab'),
        State(component_id='data_marketing', component_property='data'),
        State(component_id='persistence_narrative', component_property='data'),
        State(component_id='persistence_toast', component_property='data')
    ]
)
def func(n1, n2, active_tab, data_marketing, d_narrative, d_toast):
    data_narrative = json.loads(d_narrative)
    data_toast = json.loads(d_toast)
    if ctx.triggered_id == 'create_narrative_total_civil':
        dframe = read_df_and_select_pais(data_marketing, active_tab)

        _ = (
            dframe.groupby(by=['Estado Civil'], as_index=False).agg({'ID': 'count'})
            .rename(mapper={'ID': 'Total de Clientes'}, axis=1)
        )
        _['Porcentagem de Clientes'] = (_['Total de Clientes'] / dframe.shape[0]) * 100
        _ = _.round(decimals=2)

        narrative = create_narrative(_.to_csv(index=False), 'total de clientes por estado civil')
        # narrative = create_false_narrative('total de clientes por estado civil')
        return narrative, True
    elif ctx.triggered_id == 'caixa_narrativa_total_civil':
        return '', True
    elif data_toast['Visao Clientes']['Total de Clientes Por Estado Civil']:
        value = data_narrative['Visao Clientes']['Total de Clientes Por Estado Civil']
        return value, True
    else:
        raise exceptions.PreventUpdate


# cria o modal de edição de prompt da narrativa
@callback(
    [
        Output(component_id='modal_edit_narrative_total_civil', component_property='is_open'),
        Output(component_id='textarea_edit_prompt_narrative_total_civil', component_property='value'),
        Output(component_id='table_edit_narrative_total_civil', component_property='children')
    ],
    Input(component_id='edit_prompt_narrative_total_civil', component_property='n_clicks'),
    [
        State(component_id='tab_paises', component_property='active_tab'),
        State(component_id='data_marketing', component_property='data')
    ]
)
def func(n_click, active_tab, data):
    if n_click:
        dframe = read_df_and_select_pais(data, active_tab)

        _ = (
            dframe.groupby(by=['Estado Civil'], as_index=False).agg({'ID': 'count'})
            .rename(mapper={'ID': 'Total de Clientes'}, axis=1)
        )

        try:
            response = response_modal_prompt_narrative(_, 'total de clientes por estado civil')
        except Exception:
            logging.exception('Não foi possivel ler o arquivo que armazena o prompt')
            raise exceptions.PreventUpdate
        else:
            return response
    else:
        raise exceptions.PreventUpdate


# Salva o arquivo json com o prompt
@callback(
    Output(component_id='alert_edit_narrative_total_civil', component_property='children'),
    Input(component_id='button_save_narrative_total_civil', component_property='n_clicks'),
    State(component_id='textarea_edit_prompt_narrative_total_civil', component_property='value')
)
def func(n_click, value):
    if n_click:
        return save_json_prompt('total de clientes por estado civil', value)
    else:
        raise exceptions.PreventUpdate


# Modal historico de narrativas
@callback(
    [
        Output(component_id='modal_historico_narrativa_total_civil', component_property='is_open'),
        Output(component_id='div_historico_total_civil', component_property='children')
    ],
    Input(component_id='historico_narrative_total_civil', component_property='n_clicks')
)
def fun(n_click):
    if n_click:
        try:
            response = modal_historic_narrative('total de clientes por estado civil')
        except Exception:
            logging.exception('Houve um erro ao tentar acessar o historico!')
            raise exceptions.PreventUpdate
        else:
            return response
    else:
        raise exceptions.PreventUpdate

# -------------------------------------------------Clientes por Pais----------------------------------------------------


# Criação da narrativa
@callback(
    [
        Output(component_id='text_area_total_pais', component_property='value'),
        Output(component_id='toast_narrative_total_pais', component_property='is_open')
    ],
    [
        Input(component_id='create_narrative_total_pais', component_property='n_clicks'),
        Input(component_id='caixa_narrativa_total_pais', component_property='n_clicks')
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
    if ctx.triggered_id == 'create_narrative_total_pais':
        dframe = pd.read_json(data_marketing, orient='split', convert_dates=['Data Cadastro'])

        _ = (
            dframe.groupby(by=['Pais'], as_index=False).agg({'ID': 'count'})
            .rename(mapper={'ID': 'Total de Clientes'}, axis=1)
        )
        _['Porcentagem de Clientes'] = (_['Total de Clientes'] / dframe.shape[0]) * 100
        _ = _.round(decimals=2)
        narrative = create_narrative(_.to_csv(index=False), 'total de clientes por pais')
        # narrative = create_false_narrative('total de clientes por pais')
        return narrative, True
    elif ctx.triggered_id == 'caixa_narrativa_total_pais':
        return '', True
    elif data_toast['Visao Clientes']['Total de Clientes Por Pais']:
        value = data_narrative['Visao Clientes']['Total de Clientes Por Pais']
        return value, True
    else:
        raise exceptions.PreventUpdate


# cria o modal de edição de prompt da narrativa
@callback(
    [
        Output(component_id='modal_edit_narrative_total_pais', component_property='is_open'),
        Output(component_id='textarea_edit_prompt_narrative_total_pais', component_property='value'),
        Output(component_id='table_edit_narrative_total_pais', component_property='children')
    ],
    Input(component_id='edit_prompt_narrative_total_pais', component_property='n_clicks'),
    State(component_id='data_marketing', component_property='data')
)
def func(n_click, data):
    if n_click:
        dframe = pd.read_json(data, orient='split', convert_dates=['Data Cadastro'])

        _ = (
            dframe.groupby(by=['Pais'], as_index=False).agg({'ID': 'count'})
            .rename(mapper={'ID': 'Total de Clientes'}, axis=1)
        )

        try:
            response = response_modal_prompt_narrative(_, 'total de clientes por pais')
        except Exception:
            logging.exception('Não foi possivel ler o arquivo que armazena o prompt')
            raise exceptions.PreventUpdate
        else:
            return response
    else:
        raise exceptions.PreventUpdate


# Salva o arquivo json com o prompt
@callback(
    Output(component_id='alert_edit_narrative_total_pais', component_property='children'),
    Input(component_id='button_save_narrative_total_pais', component_property='n_clicks'),
    State(component_id='textarea_edit_prompt_narrative_total_pais', component_property='value')
)
def func(n_click, value):
    if n_click:
        return save_json_prompt('total de clientes por pais', value)
    else:
        raise exceptions.PreventUpdate


# Modal historico de narrativas
@callback(
    [
        Output(component_id='modal_historico_narrativa_total_pais', component_property='is_open'),
        Output(component_id='div_historico_total_pais', component_property='children')
    ],
    Input(component_id='historico_narrative_total_pais', component_property='n_clicks')
)
def fun(n_click):
    if n_click:
        try:
            response = modal_historic_narrative('total de clientes por pais')
        except Exception:
            logging.exception('Houve um erro ao tentar acessar o historico!')
            raise exceptions.PreventUpdate
        else:
            return response
    else:
        raise exceptions.PreventUpdate


# -------------------------------------------------Clientes por filhos--------------------------------------------------
# Criação da narrativa
@callback(
    [
        Output(component_id='text_area_total_filhos', component_property='value'),
        Output(component_id='toast_narrative_total_filhos', component_property='is_open')
    ],
    [
        Input(component_id='create_narrative_total_filhos', component_property='n_clicks'),
        Input(component_id='caixa_narrativa_total_filhos', component_property='n_clicks')
    ],
    [
        State(component_id='tab_paises', component_property='active_tab'),
        State(component_id='data_marketing', component_property='data'),
        State(component_id='persistence_narrative', component_property='data'),
        State(component_id='persistence_toast', component_property='data')
    ]
)
def func(n1, n2, active_tab, data_marketing, d_narrative, d_toast):
    data_narrative = json.loads(d_narrative)
    data_toast = json.loads(d_toast)
    if ctx.triggered_id == 'create_narrative_total_filhos':
        dframe = read_df_and_select_pais(data_marketing, active_tab)

        _ = (
            dframe.groupby(by=['Filhos em Casa'], as_index=False).agg({'ID': 'count'})
            .rename(mapper={'ID': 'Total de Clientes'}, axis=1)
        )
        _['Porcentagem de Clientes'] = (_['Total de Clientes'] / dframe.shape[0]) * 100
        _ = _.round(decimals=2)
        narrative = create_narrative(_.to_csv(index=False), 'total de clientes por filhos em casa')
        # narrative = create_false_narrative('total de clientes por filhos em casa')
        return narrative, True
    elif ctx.triggered_id == 'caixa_narrativa_total_filhos':
        return '', True
    elif data_toast['Visao Clientes']['Total de Clientes Por Filhos']:
        value = data_narrative['Visao Clientes']['Total de Clientes Por Filhos']
        return value, True
    else:
        raise exceptions.PreventUpdate


# cria o modal de edição de prompt da narrativa
@callback(
    [
        Output(component_id='modal_edit_narrative_total_filhos', component_property='is_open'),
        Output(component_id='textarea_edit_prompt_narrative_total_filhos', component_property='value'),
        Output(component_id='table_edit_narrative_total_filhos', component_property='children')
    ],
    Input(component_id='edit_prompt_narrative_total_filhos', component_property='n_clicks'),
    [
        State(component_id='tab_paises', component_property='active_tab'),
        State(component_id='data_marketing', component_property='data')
    ]
)
def func(n_click, active_tab, data):
    if n_click:
        dframe = read_df_and_select_pais(data, active_tab)

        _ = (
            dframe.groupby(by=['Filhos em Casa'], as_index=False).agg({'ID': 'count'})
            .rename(mapper={'ID': 'Total de Clientes'}, axis=1)
        )

        try:
            response = response_modal_prompt_narrative(_, 'total de clientes por filhos em casa')
        except Exception:
            logging.exception('Não foi possivel ler o arquivo que armazena o prompt')
            raise exceptions.PreventUpdate
        else:
            return response
    else:
        raise exceptions.PreventUpdate


# Salva o arquivo json com o prompt
@callback(
    Output(component_id='alert_edit_narrative_total_filhos', component_property='children'),
    Input(component_id='button_save_narrative_total_filhos', component_property='n_clicks'),
    State(component_id='textarea_edit_prompt_narrative_total_filhos', component_property='value')
)
def func(n_click, value):
    if n_click:
        return save_json_prompt('total de clientes por filhos em casa', value)
    else:
        raise exceptions.PreventUpdate


# Modal historico de narrativas
@callback(
    [
        Output(component_id='modal_historico_narrativa_total_filhos', component_property='is_open'),
        Output(component_id='div_historico_total_filhos', component_property='children')
    ],
    Input(component_id='historico_narrative_total_filhos', component_property='n_clicks')
)
def fun(n_click):
    if n_click:
        try:
            response = modal_historic_narrative('total de clientes por filhos em casa')
        except Exception:
            logging.exception('Houve um erro ao tentar acessar o historico!')
            raise exceptions.PreventUpdate
        else:
            return response
    else:
        raise exceptions.PreventUpdate

# ----------------------------------------------------Persistence Toast-------------------------------------------------


@callback(
    Output(component_id='persistence_toast', component_property='data'),
    [
        Input(component_id='toast_narrative_escolaridade', component_property='is_open'),
        Input(component_id='toast_narrative_total_civil', component_property='is_open'),
        Input(component_id='toast_narrative_total_pais', component_property='is_open'),
        Input(component_id='toast_narrative_total_filhos', component_property='is_open')
    ],
    State(component_id='persistence_toast', component_property='data')
)
def func(open_e, open_c, open_p, open_f, data):
    data_toast = json.loads(data)
    if ctx.triggered_id == 'toast_narrative_escolaridade':
        data_toast['Visao Clientes']['Total de Clientes Por Escolaridade'] = open_e
    elif ctx.triggered_id == 'toast_narrative_total_civil':
        data_toast['Visao Clientes']['Total de Clientes Por Estado Civil'] = open_c
    elif ctx.triggered_id == 'toast_narrative_total_pais':
        data_toast['Visao Clientes']['Total de Clientes Por Pais'] = open_p
    elif ctx.triggered_id == 'toast_narrative_total_filhos':
        data_toast['Visao Clientes']['Total de Clientes Por Filhos'] = open_f

    return json.dumps(data_toast)


# ---------------------------------------------------Persistence Figure-------------------------------------------------

@callback(
    Output(component_id='persistence_figure', component_property='data'),
    [
        Input(component_id='graph_total_escolaridade', component_property='figure'),
        Input(component_id='graph_clientes_total_civil', component_property='figure'),
        Input(component_id='graph_clientes_total_pais', component_property='figure'),
        Input(component_id='graph_clientes_total_filhos', component_property='figure')
    ],
    State(component_id='persistence_figure', component_property='data')
)
def func(fig1, fig2, fig3, fig4, data):
    data_figure = json.loads(data)
    data_figure['Visao Clientes']['Total de Clientes Por Escolaridade'] = fig1
    data_figure['Visao Clientes']['Total de Clientes Por Estado Civil'] = fig2
    data_figure['Visao Clientes']['Total de Clientes Por Pais'] = fig3
    data_figure['Visao Clientes']['Total de Clientes Por Filhos'] = fig4

    return json.dumps(data_figure)


# ---------------------------------------------------Persistence Narrative----------------------------------------------


@callback(
    Output(component_id='persistence_narrative', component_property='data'),
    [
        Input(component_id='text_area_escolaridade', component_property='value'),
        Input(component_id='text_area_total_civil', component_property='value'),
        Input(component_id='text_area_total_pais', component_property='value'),
        Input(component_id='text_area_total_filhos', component_property='value')
    ],
    State(component_id='persistence_narrative', component_property='data')
)
def func(value_e, value_c, value_p, value_f, data):
    data_narrative = json.loads(data)
    if ctx.triggered_id == 'text_area_escolaridade':
        data_narrative['Visao Clientes']['Total de Clientes Por Escolaridade'] = value_e
    elif ctx.triggered_id == 'text_area_total_civil':
        data_narrative['Visao Clientes']['Total de Clientes Por Estado Civil'] = value_c
    elif ctx.triggered_id == 'text_area_total_pais':
        data_narrative['Visao Clientes']['Total de Clientes Por Pais'] = value_p
    elif ctx.triggered_id == 'text_area_total_filhos':
        data_narrative['Visao Clientes']['Total de Clientes Por Filhos'] = value_f
    return json.dumps(data_narrative)
