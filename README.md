## 🛠️ Infraestrutura e Ferramentas

O projeto utiliza um ambiente conteinerizado para garantir a reprodutibilidade dos dados:

1. **IDE:** Visual Studio Code (VS Code) com extensões de Python e Docker.
2. **Banco de Dados:** PostgreSQL 15 rodando em Docker, com persistência em volume local (`./postgres_data`).
3. **BI / Visualização:** Metabase (Docker) conectado diretamente à camada **Gold** do banco.
4. **Linguagem:** Python 3.12 (Pandas, SQLAlchemy, Requests).

### Como subir o ambiente:
1. Instalar Docker e Docker Compose.
2. Executar `sudo docker compose up -d`.
3. Acessar o Metabase em `localhost:3000`.


### 📈 Camada de Visualização (Metabase)

Para a análise visual, foi integrado o **Metabase** via Docker. A principal vantagem desta abordagem é a conexão direta com o banco de dados via rede interna do Docker (`db_eleicoes`), garantindo segurança e performance.

**Lógica de Dashboards implementada:**
- **Filtro de Integridade:** Separação visual entre candidatos com dados "Normais" e "Suspeitos".
- **KPIs de Auditoria:** Contagem de registros sinalizados pelo processo de ETL.
- **Distribuição Partidária:** Análise de patrimônio médio por legenda, utilizando apenas dados validados.


📝 Registro Final de Configuração (README.md)

Adicione este trecho ao seu arquivo de documentação para encerrar o capítulo de "Infraestrutura de Visualização":

    Status da Camada de BI: Operacional ✅

        Ferramenta: Metabase (Dockerizado)

        Endpoint: http://localhost:3001

        Persistência de Metadados: Integrada ao volume do PostgreSQL (db_eleicoes), garantindo que dashboards e perguntas não sejam perdidos ao reiniciar os containers.

        Resolução de Conflitos: Porta ajustada para 3001 para evitar colisões no Host Ubuntu.