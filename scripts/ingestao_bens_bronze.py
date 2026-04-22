import pandas as pd
from sqlalchemy import create_engine
import requests, zipfile, io, os, sys
from dotenv import load_dotenv

load_dotenv()
DB_URL = f"postgresql://{os.getenv('DB_USER')}:{os.getenv('DB_PASS')}@{os.getenv('DB_HOST')}:{os.getenv('DB_PORT')}/{os.getenv('DB_NAME')}"
URL_BENS = "https://cdn.tse.jus.br/estatistica/sead/odsele/bem_candidato/bem_candidato_2024.zip"

def ingestao_bens():
    print("⏳ Baixando dados de bens do TSE...")
    response = requests.get(URL_BENS, verify=False)
    with zipfile.ZipFile(io.BytesIO(response.content)) as z:
        csv_name = [f for f in z.namelist() if f.endswith('_BRASIL.csv')][0]
        # Lendo bens (SQ_CANDIDATO e VR_BEM_CANDIDATO são as chaves)
        df = pd.read_csv(z.open(csv_name), sep=';', encoding='latin-1', low_memory=False)
        
    engine = create_engine(DB_URL)
    print(f"📤 Carregando {len(df)} bens na bronze.bens_raw...")
    df.to_sql('bens_raw', engine, schema='bronze', if_exists='replace', index=False)
    print("✅ Ingestão de Bens finalizada!")

if __name__ == "__main__":
    ingestao_bens()