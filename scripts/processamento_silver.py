import pandas as pd
from sqlalchemy import create_engine, text
import os
from dotenv import load_dotenv

load_dotenv()
DB_URL = f"postgresql://{os.getenv('DB_USER')}:{os.getenv('DB_PASS')}@{os.getenv('DB_HOST')}:{os.getenv('DB_PORT')}/{os.getenv('DB_NAME')}"

def refatorar_camada_silver():
    engine = create_engine(DB_URL)
    print("🚀 Iniciando processamento Silver...")
    
    with engine.connect() as conn:
        print("📥 Lendo dados da Bronze...")
        df_bens = pd.read_sql('SELECT * FROM bronze.bens_raw', conn)
        df_cand = pd.read_sql('SELECT * FROM bronze.candidatos_raw', conn)

    # Padronização para minúsculo
    df_bens.columns = [col.lower() for col in df_bens.columns]
    df_cand.columns = [col.lower() for col in df_cand.columns]
    
    # Limpeza monetária
    print("🧹 Limpando valores monetários...")
    df_bens['vr_bem_candidato'] = df_bens['vr_bem_candidato'].apply(
        lambda x: float(str(x).replace('.', '').replace(',', '.')) if pd.notna(x) and x != '' else 0.0
    )

    # O JOIN CRUCIAL: Trocamos 'sg_uf' por 'sg_ue' conforme identificado no banco
    print("🔗 Realizando Join entre Bens e Candidatos (usando sg_ue)...")
    df_silver = pd.merge(
        df_bens, 
        df_cand[['sq_candidato', 'nm_candidato', 'sg_partido', 'sg_ue', 'ds_cargo']], 
        on='sq_candidato', 
        how='left'
    )

    # Padronização: Renomeia 'sg_ue' para 'sg_uf' para manter a compatibilidade com a Gold
    df_silver = df_silver.rename(columns={'sg_ue': 'sg_uf'})

    # Marcação de Outliers (Acima de 500 Milhões)
    df_silver['is_outlier'] = df_silver['vr_bem_candidato'] > 500_000_000

    with engine.connect() as conn:
        conn.execute(text("CREATE SCHEMA IF NOT EXISTS silver;"))
        conn.commit()
    
    print("📤 Gravando tabela silver.candidatos_bens...")
    df_silver.to_sql('candidatos_bens', engine, schema='silver', if_exists='replace', index=False)
    print("✅ Silver concluída com sucesso (Coluna sg_uf normalizada)!")

if __name__ == "__main__":
    refatorar_camada_silver()