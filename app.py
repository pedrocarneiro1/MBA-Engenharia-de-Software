import dash
from dash import dcc, html
import plotly.express as px
import pandas as pd
from sqlalchemy import create_engine

# Conectar ao PostgreSQL
DATABASE_URL = "postgresql://pedro:senha_segura@localhost:5432/credito_db"
engine = create_engine(DATABASE_URL)

# Query para carregar os dados da View no PostgreSQL
query = "SELECT * FROM vw_credito_macro"
df = pd.read_sql(query, engine)

# 🔹 Corrigindo a conversão da coluna "data" para datetime
df["data"] = pd.to_datetime(df["data"], errors="coerce")

# Normalizar dados para melhor visualização
df["saldo_credito"] /= 1e6  # Representar em milhões
df["ibc_br"] /= 1e6  # Representar em milhões
df["cotacao_dolar"] /= 10  # Ajuste visualização

# Converter colunas para float
cols_para_converter = ["taxa_juros", "ipca", "inadimplencia", "taxa_selic", "ibc_br", "endividamento", "provisao_percentual", "cotacao_dolar"]
df[cols_para_converter] = df[cols_para_converter].apply(pd.to_numeric, errors='coerce')

# Filtragem de períodos para melhorar a leitura
df_credito = df[df["data"].dt.year >= 2011]
df_inflacao = df[df["data"].dt.year >= 1995]
df_provisao = df[df["data"].dt.year >= 2011]

def criar_grafico_credito_inflacao(df):
    return px.line(df, x="data", y=["taxa_juros", "ipca"],
                   title="Evolução da Taxa de Juros e Inflação (A partir de 1995)",
                   labels={"taxa_juros": "Taxa de Juros (%)", "ipca": "IPCA (%)"})

def criar_grafico_inadimplencia(df):
    fig = px.line(df, x="data", y=["inadimplencia", "taxa_selic", "cotacao_dolar", "provisao_percentual"],
                   title="Fatores que Influenciam a Inadimplência (A partir de 2011)",
                   labels={"inadimplencia": "Inadimplência (%)", "taxa_selic": "Taxa Selic (%)", "cotacao_dolar": "Cotação do Dólar", "provisao_percentual": "Provisão (%)"})
    fig.add_vrect(x0="2015-01-01", x1="2016-12-01", fillcolor="gray", opacity=0.3, label_text="Recessão 2015-16")
    fig.add_vrect(x0="2020-01-01", x1="2020-12-01", fillcolor="gray", opacity=0.3, label_text="Pandemia 2020")
    return fig

def criar_grafico_provisao(df):
    return px.line(df, x="data", y=["taxa_juros", "provisao_percentual"],
                   title="Evolução da Taxa de Juros e Provisões (A partir de 2011)",
                   labels={"taxa_juros": "Taxa de Juros (%)", "provisao_percentual": "Provisão (%)"})

# Inicializar o aplicativo Dash
app = dash.Dash(__name__)

# Layout do Dashboard
app.layout = html.Div(children=[
    html.H1("Dashboard de Crédito e Indicadores Macroeconômicos", style={'textAlign': 'center'}),

    # Dropdown para selecionar período de análise
    html.Label("Selecione o Período:"),
    dcc.RangeSlider(
        id='ano-slider',
        min=df["data"].dt.year.min(),
        max=df["data"].dt.year.max(),
        marks={int(ano): str(ano) for ano in df["data"].dt.year.unique()},
        value=[df["data"].dt.year.min(), df["data"].dt.year.max()]
    ),

    # Gráficos
    dcc.Graph(id='grafico-credito-inflacao'),
    html.P("Análise: O gráfico mostra a relação entre a taxa de juros e a inflação ao longo do tempo, destacando momentos de alta de juros e seus impactos na economia."),
    
    dcc.Graph(id='grafico-inadimplencia'),
    html.P("Análise: Este gráfico evidencia fatores que influenciam a inadimplência, como taxa Selic, dólar e provisões, destacando períodos de crise."),
    
    dcc.Graph(id='grafico-provisao'),
    html.P("Análise: A relação entre taxa de juros e provisões bancárias ao longo do tempo, buscando padrões de ajuste de risco."),
])

# Callbacks para atualizar os gráficos dinamicamente
@app.callback(
    [dash.Output('grafico-credito-inflacao', 'figure'),
     dash.Output('grafico-inadimplencia', 'figure'),
     dash.Output('grafico-provisao', 'figure')],
    [dash.Input('ano-slider', 'value')]
)
def atualizar_graficos(anos):
    df_filtrado = df[(df["data"].dt.year >= anos[0]) & (df["data"].dt.year <= anos[1])]
    df_credito_filtrado = df_credito[(df_credito["data"].dt.year >= anos[0]) & (df_credito["data"].dt.year <= anos[1])]
    df_inflacao_filtrado = df_inflacao[(df_inflacao["data"].dt.year >= anos[0]) & (df_inflacao["data"].dt.year <= anos[1])]
    df_provisao_filtrado = df_provisao[(df_provisao["data"].dt.year >= anos[0]) & (df_provisao["data"].dt.year <= anos[1])]
    return (criar_grafico_credito_inflacao(df_inflacao_filtrado),
            criar_grafico_inadimplencia(df_credito_filtrado),
            criar_grafico_provisao(df_provisao_filtrado))

# Rodar o aplicativo no servidor local
if __name__ == '__main__':
    app.run_server(debug=True)
