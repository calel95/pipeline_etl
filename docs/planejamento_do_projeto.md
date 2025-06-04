# **Pipeline de ETL**


## **Planejamento do Projeto de Pipeline de Dados**
### **1. Planejamento Inicial**

- Definir claramente o escopo do projeto: ingestão diária de dados do Portal da Transparência via API e download de arquivos CSV.

- Listar os dados que serão consumidos e suas características (formatos, frequência de atualização).

- Documentar requisitos funcionais (ex: frequência diária, schema esperado) e não funcionais (ex: tolerância a falhas, tempo máximo de execução).

- Escolher ferramentas e bibliotecas: Python, SQLAlchemy, FastAPI (para API interna se necessário), PostgreSQL, OneDrive SDK para upload.

### **2. Configuração do Ambiente**

- Criar ambiente virtual Python e instalar dependências (requests, pandas, sqlalchemy, fastapi, pyodbc ou onedrivesdk para OneDrive, jsonschema para validação).

- Configurar banco PostgreSQL local ou na nuvem.

- Configurar acesso e credenciais para API do Portal da Transparência e para OneDrive.

- Configurar repositório de código (Git) e pipeline CI/CD básico (opcional).

### **3. Desenvolvimento da Ingestão de Dados**

**3.1 Ingestão via API**

- Implementar módulo Python para consumir dados da API do Portal da Transparência.

- Tratar erros HTTP, limites de requisição e paginar resultados se necessário.

- Armazenar dados brutos em disco temporariamente para backup e validação.

**3.2 Ingestão via Download Automático**

- Implementar script para baixar arquivos ZIP com CSV do Portal da Transparência.

- Automatizar descompactação dos arquivos usando zipfile.

- Salvar os arquivos originais localmente para backup.

### **4. Backup dos Dados Originais na Nuvem**

- Implementar upload automático dos arquivos CSV (ou ZIP) para OneDrive após download.

- Organizar os arquivos na nuvem por data para manter histórico (ex: /portal_transparencia/YYYY-MM-DD/arquivo.csv).

- Garantir que o upload seja assíncrono ou separado da etapa de processamento para não atrasar o pipeline.

### **5. Validação de Schema e Tratamento dos Dados**

- Definir schemas JSON para os dados esperados (colunas, tipos, formatos).

- Implementar validação automática usando jsonschema ou validação customizada em pandas.

- Tratar dados inconsistentes: preencher valores faltantes, corrigir formatos, remover duplicados.

- Registrar logs detalhados de erros e estatísticas de qualidade.

### **6. Carga dos Dados no Banco de Dados PostgreSQL**

- Modelar tabelas no PostgreSQL conforme o schema dos dados.

- Usar SQLAlchemy para conexão e inserção/atualização eficiente dos dados.

- Implementar lógica para evitar duplicidade e garantir integridade.

- Criar índices e otimizações para consultas futuras.

### **7. Testes**
- Criar testes unitários para funções de ingestão, validação e carga.

- Criar testes de integração para o pipeline completo, usando dados reais ou simulados.

- Testar cenários de falha (ex: arquivo corrompido, erro na API, falha no upload).

- Automatizar testes para rodar em CI/CD.

### **8. Automação com Apache Airflow**

- Criar DAGs para orquestrar o pipeline: download → upload OneDrive → validação → carga no banco.

- Configurar agendamento diário (schedule_interval="@daily").

- Implementar sensores e operadores para dependências entre tarefas.

- Configurar alertas (e-mail, Slack) para falhas ou atrasos.

- Monitorar execução via interface do Airflow.

### **9. Documentação**

- Documentar arquitetura do pipeline, fluxos de dados, schemas e regras de negócio.

- Documentar instruções para implantação, execução e manutenção.

- Registrar decisões técnicas e pontos de atenção.

- Criar README no repositório com visão geral e exemplos de uso.

### **10. Monitoramento e Manutenção**

- Implementar logs detalhados e dashboards simples para acompanhar ingestão e qualidade.

- Planejar revisões periódicas para atualização do schema e melhorias.

- Monitorar custos e espaço usado no OneDrive.

- Estabelecer processo para lidar com mudanças na API ou formato dos arquivos.

