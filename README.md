# 🗳️ Observatório de Dados Eleitorais: Auditoria de Patrimônio 2026

## 🎯 Objetivo
Desenvolver um ecossistema de dados automatizado para identificar disparidades patrimoniais em candidatos eleitorais, processando mais de **460.000 registros** para sinalizar perfis com patrimônio superior a **R$ 10 milhões**.

## 🛠️ Stack Tecnológica (Engenharia & BI)
- **Infraestrutura:** Docker & Docker Compose (Ambiente 100% conteinerizado).
- **Banco de Dados:** PostgreSQL 15 (Arquitetura de Medalhão: Bronze, Silver, Gold).
- **Linguagem:** Python 3.12 (Pandas para ETL, SQLAlchemy para persistência).
- **Ambiente de Desenvolvimento:** VS Code, Venv (Ambiente Virtual) e Git para versionamento.
- **Business Intelligence:** Metabase (Conectado via rede interna do Docker).

## 🏗️ Arquitetura do Pipeline (ETL)
O projeto utiliza a **Medallion Architecture**, garantindo a linhagem e qualidade do dado:
1. **Bronze (Raw):** Ingestão de CSVs brutos do TSE para o Postgres.
2. **Silver (Cleaned):** Tratamento de tipos, limpeza de nulos e padronização de valores monetários via Python.
3. **Gold (Analytics):** Script automatizado (`gerar_camada_gold.py`) que aplica regras de negócio e gera flags de auditoria (`flag_alerta`).

## 📈 Principais Insights (Data Discovery)
Através do pipeline, foi possível identificar:
- **Total de registros analisados:** 463.580
- **Candidatos em Alerta (> R$ 10M):** 638 (0,13% do total).
- **Concentração de Riqueza:** Este grupo restrito detém aproximadamente **35% de todo o patrimônio declarado** no banco de dados.

## 🚀 Como Reproduzir
1. Clone o repositório.
2. Execute `sudo docker compose up -d` para subir o banco e o BI.
3. Ative o venv e execute `python scripts/gerar_camada_gold.py`.
4. Acesse o Dashboard em `localhost:3001`.