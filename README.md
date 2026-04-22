# 🗳️ Observatório de Dados Eleitorais: Auditoria de Patrimônio (Eleições 2024)

## 🎯 Objetivo
Desenvolver um ecossistema de dados automatizado para identificar disparidades patrimoniais em candidatos do pleito de 2024. O pipeline processa quase **1 milhão de registros de bens** para sinalizar perfis com patrimônio superior a **R$ 10 milhões** e isolar anomalias de preenchimento que distorcem a realidade estatística.

## 📊 Origem dos Dados
Os dados utilizados são públicos, extraídos do **Portal de Dados Abertos do TSE**, referentes aos candidatos e bens declarados nas Eleições Municipais de 2024.

## 🛠️ Stack Tecnológica
- **SO:** Linux Ubuntu 24.04 (Estação Vaio)
- **Infraestrutura:** Docker & Docker Compose (Isolamento de serviços).
- **Banco de Dados:** PostgreSQL 15 (Arquitetura Medalhão: Bronze, Silver, Gold).
- **Linguagem:** Python 3.12 (Pandas para ETL, SQLAlchemy para persistência).
- **BI & Visualização:** Metabase (Dashboarding e Data Discovery).
- **Acesso Remoto:** ngrok (Exposição segura via túnel HTTP).

---

## 🏗️ Arquitetura do Pipeline (Medallion Architecture)
O projeto garante a linhagem e qualidade do dado através de três camadas lógicas:
1.  **Bronze (Raw):** Ingestão direta dos arquivos CSV do TSE via `scripts/ingestao_bronze.py`.
2.  **Silver (Cleaned):** Processamento via `scripts/processamento_silver.py`. Resolvemos divergências de esquemas (ex: normalização de `sg_ue` para `sg_uf`) e realizamos a limpeza monetária de strings para float.
3.  **Gold (Curated):** Consolidação final via `scripts/gerar_camada_gold.py`. Os dados são bifurcados em:
    * `gold.ranking_patrimonial`: Dados higienizados e otimizados para o Dashboard.
    * `gold.log_anomalias_tse`: Registros de auditoria para inspeção de erros na fonte.

---

## 🛡️ Qualidade e Resiliência (Data Quality & Disaster Recovery)

### Filtro de Integridade
Identificamos que o sistema do TSE contém erros de preenchimento (ex: candidatos declarando patrimônios de bilhões por erro de digitação). 
- **Regra de Negócio:** Candidatos com soma de bens > **R$ 500 milhões** são movidos para a tabela `gold.log_anomalias_tse`, protegendo a fidedignidade das médias do Dashboard.

### Garantia de Resiliência
Implementamos uma rotina de validação de integridade para garantir que os dados analíticos sejam recuperáveis:
1. **Backup Automático:** O script `scripts/backup_db.sh` gera dumps SQL completos (~685MB).
2. **Ambiente Isolado:** O script `scripts/validate_backup.py` instancia um banco temporário no Docker.
3. **Restore Test:** Simula a recuperação total do sistema e audita a volumetria da camada **GOLD**.

**Comando de Segurança:**
```bash
sudo bash scripts/backup_db.sh && sudo python3 scripts/validate_backup.py