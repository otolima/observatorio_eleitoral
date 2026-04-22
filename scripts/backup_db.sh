#!/bin/bash
# scripts/backup_db.sh
DATE=$(date +%Y-%m-%d)
# Usando caminho absoluto para evitar erro de diretório
BACKUP_PATH="/home/otolima/Projetos/observatorio_eleitoral/Backup-Banco/backup_eleicoes_$DATE.sql"

echo "🔍 Iniciando backup do banco db_eleicoes..."
docker exec pg_eleicoes pg_dump -U admin db_eleicoes > $BACKUP_PATH

if [ $? -eq 0 ]; then
    echo "✅ Backup concluído em: $BACKUP_PATH"
    # Opcional: Chamar a validação automaticamente logo após o backup
    # sudo python3 /home/otolima/Projetos/observatorio_eleitoral/scripts/validate_backup.py
else
    echo "❌ Erro ao gerar backup!"
fi  