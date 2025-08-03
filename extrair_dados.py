import requests
import pandas as pd
from sqlalchemy import create_engine

# Configuração do Banco de Dados PostgreSQL
DATABASE_URL = "postgresql://"
engine = create_engine(DATABASE_URL)

# Dicionário com os indicadores do BCB e suas tabelas
indicadores_bcb = {
    "IBC-Br": {
        "codigo": 24363,
        "tabela": "bcb_ibc_br",
        "coluna": "ibc_br",
        "url": "https://api.bcb.gov.br/dados/serie/bcdata.sgs.24363/dados?formato=json"
    },
    "Endividamento_Familias": {
        "codigo": 20577,
        "tabela": "bcb_endividamento_familias",
        "coluna": "endividamento",
        "url": "https://api.bcb.gov.br/dados/serie/bcdata.sgs.20577/dados?formato=json"
    },
    "Provisao_Credito": {
        "codigo": 13666,
        "tabela": "bcb_provisao_credito",
        "coluna": "provisao_percentual",
        "url": "https://api.bcb.gov.br/dados/serie/bcdata.sgs.13666/dados?formato=json"
    },
    "Taxa_Juros_Credito": {
        "codigo": 25485,
        "tabela": "bcb_taxa_juros_credito",
        "coluna": "taxa_juros",
        "url": "https://api.bcb.gov.br/dados/serie/bcdata.sgs.25485/dados?formato=json"
    },
    "Saldo_Credito_Total": {
        "codigo": 20539,
        "tabela": "bcb_saldo_credito_total",
        "coluna": "saldo_credito",
        "url": "https://api.bcb.gov.br/dados/serie/bcdata.sgs.20539/dados?formato=json"
    },
    "Taxa_Inadimplencia": {
        "codigo": 21099,
        "tabela": "bcb_taxa_inadimplencia",
        "coluna": "inadimplencia",
        "url": "https://api.bcb.gov.br/dados/serie/bcdata.sgs.21099/dados?formato=json"
    },
    "Taxa_SELIC": {
        "codigo": 11,
        "tabela": "bcb_taxa_selic",
        "coluna": "taxa_selic",
        "url": "https://api.bcb.gov.br/dados/serie/bcdata.sgs.11/dados?formato=json"
    },
    "IPCA": {
        "codigo": 433,
        "tabela": "bcb_ipca",
        "coluna": "ipca",
        "url": "https://api.bcb.gov.br/dados/serie/bcdata.sgs.433/dados?formato=json"
    },
    "Cotacao_Dolar": {
        "codigo": 1,
        "tabela": "bcb_cotacao_dolar",
        "coluna": "cotacao_dolar",
        "url": "https://api.bcb.gov.br/dados/serie/bcdata.sgs.1/dados?formato=json"
    }
}

# Loop para buscar e salvar os dados de cada indicador
for nome, info in indicadores_bcb.items():
    print(f"📥 Buscando dados de {nome}...")

    response = requests.get(info["url"])

    if response.status_code == 200:
        try:
            dados = response.json()
            df = pd.DataFrame(dados)
            df.rename(columns={"data": "data", "valor": info["coluna"]}, inplace=True)

            # Converter data para formato compatível com o PostgreSQL
            df["data"] = pd.to_datetime(df["data"], format="%d/%m/%Y", errors="coerce")

            # Remover valores nulos e duplicatas
            df.dropna(subset=["data"], inplace=True)
            df.drop_duplicates(subset=["data"], keep="last", inplace=True)

            # Verificar e remover dados já existentes no banco
            with engine.connect() as conn:
                existing_dates = pd.read_sql(f"SELECT data FROM {info['tabela']}", conn)
                df = df[~df["data"].isin(existing_dates["data"])]

            # Salvar no banco de dados
            df.to_sql(info["tabela"], engine, if_exists="append", index=False)
            print(f"✅ Dados de {nome} salvos na tabela {info['tabela']}!")

        except Exception as e:
            print(f"❌ Erro ao processar {nome}: {e}")
    else:
        print(f"❌ Erro ao buscar {nome}: {response.status_code} - API pode estar fora do ar.")
