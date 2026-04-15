import pandas as pd
from sqlalchemy import create_engine, text
import os
from dotenv import load_dotenv

load_dotenv()
DB_URL = f"postgresql://{os.getenv('DB_USER')}:{os.getenv('DB_PASS')}@{os.getenv('DB_HOST')}:{os.getenv('DB_PORT')}/{os.getenv('DB_NAME')}"

def gerar_camada_gold():
    engine = create_engine(DB_URL)
    
    print("📥 Extraindo dados da Silver para processar a Gold...")
    # Lemos as colunas que a Silver preparou
    query = "SELECT * FROM silver.candidatos_bens"
    
    try:
        df = pd.read_sql(query, engine)
    except Exception as e:
        print(f"❌ Erro ao ler a Camada Silver: {e}")
        return

    # Normaliza nomes de colunas para minúsculo
    df.columns = [col.lower() for col in df.columns]
    
    print(f"✅ Colunas detectadas: {list(df.columns)}")

    # 1. Filtra dados FIÉIS (Ranking) e ANOMALIAS (Auditoria)
    df_fiel = df[df['is_outlier'] == False].copy()
    df_erros = df[df['is_outlier'] == True].copy()
    
    # 2. Agrupamento do Ranking Principal
    colunas_agrup = ['sq_candidato', 'nm_candidato', 'sg_partido', 'sg_uf', 'ds_cargo']
    
    print("⚖️ Agrupando patrimônio por candidato...")
    df_gold = df_fiel.groupby(colunas_agrup).agg({
        'vr_bem_candidato': 'sum'
    }).reset_index()

    # 3. Renomeação final para o BI
    df_gold = df_gold.rename(columns={'vr_bem_candidato': 'patrimonio_total'})
    df_gold['grande_patrimonio'] = df_gold['patrimonio_total'] > 10_000_000

    # 4. Carga final na Gold
    print("📤 Carregando tabelas na Camada Gold...")
    with engine.connect() as conn:
        conn.execute(text("CREATE SCHEMA IF NOT EXISTS gold;"))
        conn.commit()
    
    # Salva o Ranking de Candidatos
    df_gold.to_sql('ranking_patrimonial', engine, schema='gold', if_exists='replace', index=False)
    
    # Salva o Log de Anomalias (Bilionários suspeitos)
    df_erros.to_sql('log_anomalias_tse', engine, schema='gold', if_exists='replace', index=False)
    
    print("✅ Camada GOLD finalizada com sucesso!")
    print(f"📊 Ranking: {len(df_gold)} registros | 🚩 Anomalias: {len(df_erros)} registros")

if __name__ == "__main__":
    gerar_camada_gold()