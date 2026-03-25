import pandas as pd
from sqlalchemy import create_engine
import sys

def executar_pipeline_auditoria():
    """
    Script de Produção: Transforma a Camada Gold de Ranking em uma Camada de Auditoria.
    Objetivo: Identificar candidatos com patrimônio acima de R$ 10 milhões.
    """
    try:
        # 1. Configuração da Conexão (Ajuste conforme seu ambiente Docker)
        DATABASE_URL = 'postgresql://admin:senha_eleicoes_2026@localhost:5432/db_eleicoes'
        engine = create_engine(DATABASE_URL)
        
        print("🔗 Conectando ao PostgreSQL...")

        # 2. EXTRAÇÃO: Lendo da tabela Gold existente
        # Usamos o nome completo com o esquema 'gold'
        query = 'SELECT * FROM gold.ranking_patrimonio_gold'
        df = pd.read_sql(query, engine)
        
        if df.empty:
            print("⚠️ A tabela gold.ranking_patrimonio_gold está vazia. Verifique o banco.")
            return

        print(f"📊 {len(df)} registros carregados para análise.")

        # 3. TRANSFORMAÇÃO: Regra de Negócio de Auditoria
        # Definimos o limite de corte (10 Milhões)
        LIMITE_ALERTA = 10000000 
        COLUNA_VALOR = 'patrimonio_total' # Nome confirmado via DBeaver
        
        # Criando a flag de alerta (SIM para > 10M, NÃO para os demais)
        df['flag_alerta'] = df[COLUNA_VALOR].fillna(0).apply(
            lambda x: 'SIM' if x >= LIMITE_ALERTA else 'NÃO'
        )

        # 4. CARGA: Salvando a nova tabela de Auditoria no esquema 'gold'
        # O parâmetro schema='gold' garante que ela fique no lugar certo
        df.to_sql('analise_auditoria_gold', 
                  engine, 
                  schema='gold', 
                  if_exists='replace', 
                  index=False)
        
        # Resumo para o log
        total_suspeitos = len(df[df['flag_alerta'] == 'SIM'])
        print("-" * 30)
        print("✅ PIPELINE CONCLUÍDO COM SUCESSO!")
        print(f"📂 Tabela gerada: gold.analise_auditoria_gold")
        print(f"🚩 Candidatos com Alerta (>10M): {total_suspeitos}")
        print("-" * 30)

    except Exception as e:
        print(f"❌ ERRO CRÍTICO NO PIPELINE: {e}")
        sys.exit(1)

if __name__ == "__main__":
    executar_pipeline_auditoria()