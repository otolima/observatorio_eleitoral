import os
from sqlalchemy import create_engine, text
from dotenv import load_dotenv

# Carrega as variáveis do seu cofre .env
load_dotenv()

# Monta a URL de conexão usando as variáveis do .env
# Assim você não expõe sua senha no terminal
user = os.getenv("DB_USER")
password = os.getenv("DB_PASS")
host = os.getenv("DB_HOST", "localhost")
port = os.getenv("DB_PORT", "5432")
db = os.getenv("DB_NAME")

url = f"postgresql://{user}:{password}@{host}:{port}/{db}"

try:
    engine = create_engine(url)
    with engine.connect() as conn:
        # Faz uma consulta boba só para ver se o banco responde
        result = conn.execute(text("SELECT 1"))
        print("✅ Conexão estabelecida com sucesso!")
        print(f"📡 Conectado ao banco: {db} no host: {host}")
except Exception as e:
    print("❌ Falha na conexão!")
    print(f"Erro: {e}")