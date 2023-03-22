import pandas as pd
import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import plotly.express as px

df = pd.read_csv('C:/Users/caiom/C0D3S/Web_Scraping/empresas.csv')

external_stylesheets = ['styles.css']
app = dash.Dash(__name__, external_stylesheets=external_stylesheets)


app.layout = html.Div([
    html.H1('Dashboard de Empresas'),
    html.Div([
        dcc.Graph(id='grafico_estado'),
        dcc.Graph(id='grafico_faturamento'),
        dcc.Dropdown(
    id='dropdown_empresas',
    options=[
            {'label': '500 Maiores Empresas', 'value': 500},
            {'label': '250 Maiores Empresas', 'value': 250},
            {'label': '50 Maiores Empresas', 'value': 50}
            ],
            value=500
        ),
        dcc.Dropdown(
            id='dropdown_comparativo',
            options=[{'label': x, 'value': x} for x in df['nome'].unique()],
            multi=True
        ),
        dcc.Graph(id='grafico_comparativo')
    ])
])

@app.callback(
    Output('grafico_estado', 'figure'),
    Input('dropdown_empresas', 'value')
)
def update_grafico_estado(n):
    if not isinstance(n, int) or n < 1 or n > len(df):
        raise ValueError('Valor inválido para o número de empresas')
    df_estado = df.groupby('estado').sum().sort_values('estado', ascending=False).reset_index()
    df_estado = df_estado[:n]
    fig = px.bar(df_estado, x='estado', y='faturamento', color='estado', title=f'Top Estados por Faturamento')

    return fig


@app.callback(
Output('grafico_faturamento', 'figure'),
Input('dropdown_empresas', 'value')
)
def update_grafico_faturamento(n):
    df_faturamento = df.sort_values('faturamento', ascending=True)
    df_faturamento = df_faturamento[:n]
    fig = px.bar(df_faturamento, x='nome', y='faturamento', color='estado', title=f'Top {n} Empresas por Faturamento')

    return fig

@app.callback(
Output('grafico_comparativo', 'figure'),
Input('dropdown_comparativo', 'value')
)
def update_grafico_comparativo(empresas):
    if len(empresas) != 2:
        raise ValueError('Selecione 2 empresas para comparar')
    df_empresas = df[df['nome'].isin(empresas)].sort_values('faturamento', ascending=True)
    fig = px.bar(df_empresas, x='nome', y='faturamento', color='setor', title=f'Comparativo de Faturamento das Empresas {empresas[0]} e {empresas[1]}')
    return fig

if __name__ == '__main__':
    app.run_server(debug=True)