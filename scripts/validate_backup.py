import subprocess
import os
from datetime import datetime

# 1. Configurações Dinâmicas
hoje = datetime.now().strftime("%Y-%m-%d")
BACKUP_PATH = f"/home/otolima/Projetos/observatorio_eleitoral/Backup-Banco/backup_eleicoes_{hoje}.sql"
TEMP_DB_NAME = "db_teste_integridade"
POSTGRES_USER = "admin"
CONTAINER_NAME = "pg_eleicoes"

def run_command(cmd):
    return subprocess.run(cmd, shell=True, capture_output=True, text=True)

def validate():
    print(f"--- INICIANDO PROTOCOLO DE VALIDAÇÃO ({hoje}) ---")
    
    if not os.path.exists(BACKUP_PATH):
        print(f"❌ ERRO: Backup de hoje não encontrado em: {BACKUP_PATH}")
        return

    # --- PASSO 1: Preparar o Banco ---
    print(f"🛠 Criando ambiente temporário: {TEMP_DB_NAME}")
    run_command(f"docker exec {CONTAINER_NAME} psql -U {POSTGRES_USER} -d postgres -c 'DROP DATABASE IF EXISTS {TEMP_DB_NAME} WITH (FORCE);'")
    run_command(f"docker exec {CONTAINER_NAME} psql -U {POSTGRES_USER} -d postgres -c 'CREATE DATABASE {TEMP_DB_NAME};'")
    
    # --- PASSO 2: Restaurar o backup ---
    print("⏳ Restaurando dados (Processando ~685MB)...")
    restore_cmd = f'cat "{BACKUP_PATH}" | docker exec -i {CONTAINER_NAME} psql -U {POSTGRES_USER} -d {TEMP_DB_NAME}'
    restore_res = run_command(restore_cmd)

    if restore_res.returncode != 0:
        print("❌ ERRO crítico na restauração do arquivo SQL.")
        return

    # --- PASSO 3: Validação de Conteúdo (Camada GOLD) ---
    print("✅ Restauração finalizada. Auditando camada GOLD...")
    
    # Query de Contagem
    query_count = "SELECT count(*) FROM gold.ranking_patrimonial;"
    res_count = run_command(f"docker exec {CONTAINER_NAME} psql -U {POSTGRES_USER} -d {TEMP_DB_NAME} -t -c \"{query_count}\"")
    
    # Query de Amostra (Ajustada para os nomes reais das suas colunas)
    query_sample = "SELECT nm_candidato, sg_uf, patrimonio_total FROM gold.ranking_patrimonial ORDER BY patrimonio_total DESC LIMIT 3;"
    res_sample = run_command(f"docker exec {CONTAINER_NAME} psql -U {POSTGRES_USER} -d {TEMP_DB_NAME} -c \"{query_sample}\"")

    count_val = res_count.stdout.strip()
    if count_val.isdigit():
        print(f"🚀 SUCESSO: Backup Íntegro!")
        print(f"📊 Volume na GOLD: {count_val} registros.")
        print("\n👀 TOP 3 Patrimônios Restaurados:")
        print(res_sample.stdout)
    else:
        print("⚠️ ALERTA: Dados não encontrados. Verifique os logs do pg_dump.")

    # --- PASSO 4: Limpeza ---
    print(f"🧹 Removendo banco temporário...")
    run_command(f"docker exec {CONTAINER_NAME} psql -U {POSTGRES_USER} -d postgres -c 'DROP DATABASE {TEMP_DB_NAME};'")
    print("✨ Processo concluído com sucesso.")

if __name__ == "__main__":
    validate()