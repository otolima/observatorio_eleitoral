from sqlalchemy import create_engine, text

# TESTE DIRETO: Sem .env, sem variáveis ocultas.
USER = "admin"
PASS = "senha_eleicoes_2026"
HOST = "127.0.0.1"
PORT = "5432"
DB = "db_eleicoes"

url = f"postgresql://{USER}:{PASS}@{HOST}:{PORT}/{DB}"

print(f"--- Tentando conexão direta com a senha: {PASS} ---")

try:
    engine = create_engine(url)
    with engine.connect() as conn:
        conn.execute(text("SELECT 1"))
        print("✅ SUCESSO ABSOLUTO: A infraestrutura Docker está perfeita!")
except Exception as e:
    print("❌ ERRO DE INFRAESTRUTURA:")
    print(e)