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

## 🏗️ Arquitetura do Pipeline (Medallion Architecture)
O projeto garante a linhagem e qualidade do dado através de três camadas:
1.  **Bronze (Raw):** Ingestão direta dos arquivos CSV do TSE via `scripts/ingestao_bronze.py`.
2.  **Silver (Cleaned):** Processamento via `scripts/processamento_silver.py`. Nesta fase, resolvemos divergências de esquemas (ex: normalização da coluna `sg_ue` para `sg_uf`) e realizamos a limpeza monetária de strings para float.
3.  **Gold (Curated):** Consolidação final via `scripts/gerar_camada_gold.py`. Os dados são bifurcados em:
    * `ranking_patrimonial`: Dados higienizados para o Dashboard.
    * `log_anomalias_tse`: Registros de auditoria para inspeção de erros na fonte.

## 🛡️ Tratamento de Qualidade e Integridade (Data Quality)
Um diferencial crítico deste projeto é o **Filtro de Integridade**. Identificamos que o sistema do TSE contém erros de preenchimento (ex: vereadores declarando patrimônios de R$ 10 bilhões devido a erros de casas decimais). 
- **Regra de Negócio:** Candidatos com soma de bens > **R$ 500 milhões** são movidos para uma tabela de auditoria (`log_anomalias_tse`), protegendo a média e a escala visual do Dashboard principal.

## 📈 Resultados da Auditoria (Dados Consolidados)
- **Total de registros de bens processados:** ~912.620
- **Candidatos únicos no Ranking:** 296.063
- **Candidatos sinalizados (> R$ 10M):** 622
- **Anomalias Detectadas:** 13 casos isolados (bilionários suspeitos isolados para garantir a fidedignidade do BI).

## 🚀 Como Reproduzir
1. **Inicie a Infraestrutura:** `docker-compose up -d`
2. **Configure o ambiente Python:**
   ```bash
   python3 -m venv venv
   source venv/bin/activate
   pip install -r requirements.txt