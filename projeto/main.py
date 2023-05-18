import dash
from dash import html, dcc, callback, Input, Output, State, exceptions
import dash_bootstrap_components as dbc
import pandas as pd
import json
import os

from utils import (
    ask_chatgpt,
    relatorio
)
from app import app


def sidebar():
    return dbc.Card([
        dbc.CardHeader([dbc.Label('DashBoard Analítico')]),
        dbc.CardBody([
            dbc.Nav([
                dbc.NavItem(dbc.NavLink('Visão Cliente', href='/', active='exact', n_clicks=0, id='cliente_nav')),
                dbc.NavItem(dbc.NavLink('Visão Comportamento', href='/visao_comportamento', active='exact')),
                dbc.NavItem(dbc.NavLink('Visão Campanhas', href='/visao_campanhas', active='exact')),
                dbc.NavItem(dbc.NavLink('Visão Pontos de Venda', href='/visao_pontos_vendas', active='exact')),
                dbc.DropdownMenu(
                    label='Opções',
                    children=[
                        dbc.DropdownMenuItem('ChatGpt', id='open_chatgpt', n_clicks=0),
                        dbc.DropdownMenuItem('Criar Relatório', id='criar_relatorio', n_clicks=0),
                        dbc.DropdownMenuItem('Assistente', href='/assistente_analise')
                    ], nav=True
                )
            ], vertical='md', pills=True)
        ]),
        dbc.CardFooter(
            dbc.Row([
                dbc.Col([dbc.Label('Versão 1.0')]),
                dbc.Col([html.Div(id='teste_sidebar')])
            ])
        )
    ], style={'height': '100%'})


app.layout = html.Div([
    dcc.Store(
        id='persistence_toast',
        data=json.dumps(
            {
                "Visao Clientes": {
                    "Total de Clientes Por Escolaridade": False,
                    "Total de Clientes Por Estado Civil":  False,
                    "Total de Clientes Por Pais": False,
                    "Total de Clientes Por Filhos": False
                },
                "Visao Comportamento": {
                    "Total Gasto x Salario Anual": False,
                    "Total Gasto Por Escolaridade e Estado Civil": False,
                    "Total Gasto x Filhos em Casa": False,
                    "Total Gasto x Adolescentes em Casa": False
                },
                "Visao Campanhas": {
                    "Efetividade da Campanha x Numeros de Filhos": False,
                    "Efetividade da Campanha x Media Salarial": False,
                    "Campanha Table": False,
                    "Resultado das Campanhas de Marketing": False
                },
                "Visao Pontos de Vendas": {
                    "Total Gasto em Diferentes Categorias por Pais": False,
                    "Total Gasto por Ano e Pais": False
                }
            }
        )
    ),
    dcc.Store(
        id='persistence_narrative',
        data=json.dumps(
            {
                "Visao Clientes": {
                    "Total de Clientes Por Escolaridade": None,
                    "Total de Clientes Por Estado Civil": None,
                    "Total de Clientes Por Pais": None,
                    "Total de Clientes Por Filhos": None
                },
                "Visao Comportamento": {
                    "Total Gasto x Salario Anual": None,
                    "Total Gasto Por Escolaridade e Estado Civil": None,
                    "Total Gasto x Filhos em Casa": None,
                    "Total Gasto x Adolescentes em Casa": None
                },
                "Visao Campanhas": {
                    "Efetividade da Campanha x Numeros de Filhos": None,
                    "Efetividade da Campanha x Media Salarial": None,
                    "Campanha Table": None,
                    "Resultado das Campanhas de Marketing": None
                },
                "Visao Pontos de Vendas": {
                    "Total Gasto em Diferentes Categorias por Pais": None,
                    "Total Gasto por Ano e Pais": None
                }
            }
        )
    ),
    dcc.Store(
        id='persistence_figure',
        data=json.dumps(
            {
                "Visao Clientes": {
                    "Total de Clientes Por Escolaridade": {},
                    "Total de Clientes Por Estado Civil": {},
                    "Total de Clientes Por Pais": {},
                    "Total de Clientes Por Filhos": {}
                },
                "Visao Comportamento": {
                    "Total Gasto x Salario Anual": {},
                    "Total Gasto Por Escolaridade e Estado Civil": {},
                    "Total Gasto x Filhos em Casa": {},
                    "Total Gasto x Adolescentes em Casa": {}
                },
                "Visao Campanhas": {
                    "Efetividade da Campanha x Numeros de Filhos": {},
                    "Efetividade da Campanha x Media Salarial": {},
                    "Campanha Table": {},
                    "Resultado das Campanhas de Marketing": {}
                },
                "Visao Pontos de Vendas": {
                    "Total Gasto em Diferentes Categorias por Pais": None,
                    "Total Gasto por Ano e Pais": None
                }
            }
        )
    ),
    dcc.Location(id='route'),
    dcc.Store(
        id='data_marketing',
        data=pd.read_csv(
            '.\\data\\dados_marketing_tratado.csv', sep=';', parse_dates=['Data Cadastro'], dayfirst=True
        ).to_json(date_format='iso', orient='split')
    ),
    dbc.Row([
        dbc.Col([sidebar()], md=2),
        dbc.Col([dash.page_container], md=10)
    ]),
    dbc.Modal([
        dbc.ModalHeader(dbc.ModalTitle('ChatGpt')),
        dbc.ModalBody([
            dbc.Row([
                dbc.Col([dbc.Textarea(placeholder='Me faça uma pergunta...', id='input_chatgpt')], md=10),
                dbc.Col([dbc.Button(
                    children=[html.I(className='bi bi-send-fill')], outline=True, n_clicks=0, className='me-2',
                    color='primary', id='button_chatgpt'
                )
                ], md=2)
            ]),
            dbc.Row([
                dbc.Col([
                    dcc.Loading(
                        type='dot',
                        children=[
                            dbc.Toast(
                                [dbc.Textarea(id='response_chatgpt', className="mb-3", size='md', rows=10)],
                                id='toast_chatgpt', header='ChatGpt', dismissable=True,
                                is_open=False, style={'width': '100%'}
                            )
                        ], color='#636EFA'
                    )
                ])
            ], style={'margin-top': '20px'})
        ])
    ], id='modal_chatgpt', is_open=False),
    dcc.Loading(
        type='circle',
        fullscreen=True,
        children=[
            dbc.Modal([
                dbc.ModalHeader(''),
                dbc.ModalBody([
                    html.Div(id='div_alert_relatorio')
                ])
            ], id='modal_alert_relatorio', is_open=False)
        ]
    )
])


# Controle do Modal do Prompt Chatgpt
@callback(
    Output(component_id='modal_chatgpt', component_property='is_open'),
    Input(component_id='open_chatgpt', component_property='n_clicks'),
    State(component_id='modal_chatgpt', component_property='is_open')
)
def func(n_click, is_open):
    if n_click:
        return not is_open
    return is_open


# habilita ou desabilidade o input do chatgpt de acordo com o valor
@callback(
    Output(component_id='button_chatgpt', component_property='disabled'),
    Input(component_id='input_chatgpt', component_property='value')
)
def func(input_chat):
    if input_chat:
        return False
    else:
        return True


# gera a resposta da pergunta ao ChatGpt
@callback(
    [
        Output(component_id='toast_chatgpt', component_property='is_open'),
        Output(component_id='response_chatgpt', component_property='value')
    ],
    Input(component_id='button_chatgpt', component_property='n_clicks'),
    State(component_id='input_chatgpt', component_property='value')
)
def func(n, value):
    if n:
        return True, ask_chatgpt(value.strip().replace('\n', ' '), None)
    else:
        raise exceptions.PreventUpdate


# Limpa o input do prompt do ChatGpt
@callback(
    Output(component_id='input_chatgpt', component_property='value'),
    Input(component_id='button_chatgpt', component_property='n_clicks')
)
def func(n_clicks):
    if n_clicks:
        return ''
    else:
        return ''


@callback(
    [
        Output(component_id='modal_alert_relatorio', component_property='is_open'),
        Output(component_id='div_alert_relatorio', component_property='children')
    ],
    Input(component_id='criar_relatorio', component_property='n_clicks'),
    [
        State(component_id='persistence_figure', component_property='data'),
        State(component_id='persistence_narrative', component_property='data')
    ]
)
def func(n, data1, data2):
    if n:
        try:

            doc = relatorio(data1, data2)

            doc.save(os.path.join('.', 'relatorios', 'doc_teste.docx'))
        except Exception as e:
            print(e)
            alert = dbc.Alert([
                html.I(className='bi bi-exclamation-triangle-fill me-2'), 'Houve um Erro ao Gerar o Relatório'
            ], color='warning')
            return True, alert
        else:
            alert = dbc.Alert([
                html.I(className='bi bi-check-square-fill me-2'), 'Relatório Gerado com Sucesso'
            ], color='success')
            return True, alert
    else:
        raise exceptions.PreventUpdate


if __name__ == '__main__':
    app.run_server(debug=True, port=8040)
