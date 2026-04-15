import pandas as pd
from sqlalchemy import create_engine, text
import requests
import zipfile
import io
import os
import sys
from dotenv import load_dotenv

# 1. Carregar configurações de segurança
load_dotenv()

# ADICIONE ESTAS LINHAS PARA DEBUG:
print(f"DEBUG - Usuário: '{os.getenv('DB_USER')}'")
print(f"DEBUG - Senha: '{os.getenv('DB_PASS')}'")

USER = os.getenv('DB_USER')
PASS = os.getenv('DB_PASS')
HOST = os.getenv('DB_HOST')
PORT = os.getenv('DB_PORT')
NAME = os.getenv('DB_NAME')

DB_URL = f"postgresql://{USER}:{PASS}@{HOST}:{PORT}/{NAME}"
URL_TSE = "https://cdn.tse.jus.br/estatistica/sead/odsele/consulta_cand/consulta_cand_2024.zip"

def baixar_e_ler_tse(url):
    """Faz o download do ZIP e extrai o CSV do Brasil."""
    print(f"⏳ Baixando dados do TSE: {url}...")
    # verify=False para evitar erros de certificado em sites gov
    response = requests.get(url, verify=False)
    
    with zipfile.ZipFile(io.BytesIO(response.content)) as z:
        # Busca o arquivo que termina com _BRASIL.csv
        csv_name = [f for f in z.namelist() if f.endswith('_BRASIL.csv')][0]
        print(f"📂 Lendo arquivo: {csv_name}")
        
        # O encoding latin-1 é crucial para arquivos do TSE
        return pd.read_csv(z.open(csv_name), sep=';', encoding='latin-1', low_memory=False)

def carregar_no_banco(df, engine):
    """Cria o schema e carrega os dados na camada Bronze."""
    print("🏗️ Preparando banco de dados (Schema Bronze)...")
    with engine.connect() as conn:
        conn.execute(text("CREATE SCHEMA IF NOT EXISTS bronze;"))
        conn.commit()

    print(f"📤 Carregando {len(df)} registros na tabela bronze.candidatos_raw...")
    df.to_sql('candidatos_raw', engine, schema='bronze', if_exists='replace', index=False)
    print("✅ Camada BRONZE atualizada com sucesso!")

if __name__ == "__main__":
    try:
        # Criar motor de conexão
        engine = create_engine(DB_URL)
        
        # Executar ETL
        df_dados = baixar_e_ler_tse(URL_TSE)
        carregar_no_banco(df_dados, engine)
        
    except Exception as e:
        print(f"❌ Erro crítico na Ingestão Bronze: {e}")
        sys.exit(1)