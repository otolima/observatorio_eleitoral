# 🗳️ Observatório de Dados Eleitorais 2026

Este projeto implementa um pipeline de Engenharia de Dados completo para auditoria e análise de patrimônio de candidatos, utilizando a **Arquitetura de Medalhão** para transformar dados brutos em insights acionáveis.

## 🎯 Objetivo do Projeto
Identificar disparidades patrimoniais e automatizar o flagging (alerta) de candidatos com patrimônio superior a R$ 10 milhões, facilitando a auditoria cívica.

## 🏗️ Arquitetura e Pipeline (ETL)
O fluxo de dados segue o padrão de mercado:
1.  **Bronze (Raw):** Ingestão dos dados brutos do TSE para o PostgreSQL.
2.  **Silver (Cleaned):** Limpeza de tipos, tratamento de nulos e padronização.
3.  **Gold (Analytics):** Geração de rankings e tabelas de auditoria prontas para BI.

## 🛠️ Tecnologias Utilizadas
- **Infraestrutura:** Docker & Docker Compose (PostgreSQL 15 e Metabase).
- **Linguagem:** Python 3.12 (Pandas para transformação, SQLAlchemy para conexão).
- **Orquestração:** Scripts modulares para automação do pipeline Gold.
- **Visualização:** Metabase conectado à camada Gold para dashboards em tempo real.

## 🚀 Como Executar
1. Subir os containers: `sudo docker compose up -d`
2. Ativar o ambiente: `source venv/bin/activate`
3. Processar a Camada Gold: `python scripts/gerar_camada_gold.py`
4. Acessar os Dashboards: `http://localhost:3001`

---
*Projeto desenvolvido como parte do aprendizado prático em Engenharia de Dados.*