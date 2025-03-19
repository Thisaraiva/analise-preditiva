# analise-preditiva
Avaliação para a disciplina de Analise Preditiva com conceitos e resultados que serão desenvolvidos ao longo do semestre do curso de Engenharia de Software

# Análise Preditiva e Modelos de Banco de Dados: Um Estudo de Caso em Previsão de Churn

## 1. Introdução

A análise preditiva é uma área da ciência de dados que utiliza técnicas estatísticas e de machine learning para prever eventos futuros com base em dados históricos. Para implementar um pipeline eficiente de análise preditiva, é essencial escolher os modelos de banco de dados adequados para armazenar e processar os dados, garantindo desempenho e escalabilidade. Este trabalho explora os conceitos de análise de dados, apresenta um domínio de problema para aplicação de análise preditiva (previsão de churn em telecomunicações), justifica a escolha de modelos de banco de dados (relacional e NoSQL), propõe um modelo de dados simples e exemplifica a manipulação de dados. Por fim, discute a escolha do ambiente para armazenamento de dados brutos e pré-processados. Este documento está estruturado para guiá-lo através dos conceitos, exemplos práticos e decisões de design que sustentam um pipeline de análise preditiva robusto.

## 2. Desenvolvimento

### 2.1. Tipos de Análise de Dados

A análise de dados pode ser categorizada em quatro tipos principais, cada um com objetivos e técnicas distintas:

#### Análise Descritiva

* **Objetivo**: Resumir e descrever dados históricos, fornecendo insights sobre o que aconteceu.
* **Técnicas**: Estatísticas descritivas (média, mediana, desvio padrão), visualizações (gráficos, tabelas).
* **Exemplo no contexto de churn**:
    * "Um gráfico de barras mostrando a distribuição de churn por região revela que clientes em áreas urbanas têm uma taxa de churn 20% maior do que em áreas rurais."
    * "Um heatmap da taxa de churn por tipo de plano e tempo de assinatura pode identificar padrões, como maior churn em planos básicos com mais de 12 meses de uso."

#### Análise Diagnóstica

* **Objetivo**: Entender as causas de eventos passados, investigando o porquê de certas ocorrências.
* **Técnicas**: Testes de hipóteses, análise de causa e efeito (diagrama de Ishikawa), análise de correlação.
* **Exemplo no contexto de churn**:
    * "Um diagrama de Ishikawa (espinha de peixe) identifica que as principais causas de churn são problemas de conectividade, atendimento ao cliente insatisfatório e preços altos."
    * "Uma análise de correlação mostra que clientes com mais de três reclamações no último semestre têm 70% mais chances de cancelar o serviço."

#### Análise Preditiva

* **Objetivo**: Utilizar dados históricos para prever eventos futuros, antecipando tendências e comportamentos.
* **Técnicas**: Regressão, classificação, séries temporais, machine learning (Random Forest, Gradient Boosting, redes neurais).
* **Exemplo no contexto de churn**:
    * "Um modelo de classificação baseado em Random Forest prevê a probabilidade de um cliente cancelar o serviço nos próximos 30 dias, com base em histórico de pagamentos, interações e feedbacks."
    * "Uma série temporal prevê o número de cancelamentos para o próximo trimestre, considerando sazonalidade e tendências históricas."

#### Análise Prescritiva

* **Objetivo**: Recomendar ações com base em previsões, otimizando decisões e resultados.
* **Técnicas**: Otimização, simulação, sistemas de recomendação, inteligência artificial.
* **Exemplo no contexto de churn**:
    * "Um sistema de recomendação sugere ofertas personalizadas, como upgrades de plano ou descontos, para clientes com alta probabilidade de churn."
    * "Um modelo de otimização define a alocação ideal de recursos para campanhas de retenção, maximizando o ROI (Retorno sobre Investimento)."

### 2.1.1. Pipeline de Análise Preditiva

O fluxo de análise segue as seguintes etapas:

1.  **Extração**: Dados extraídos dos bancos SQL e NoSQL.
2.  **Transformação**: Tratamento de dados inconsistentes e engenharia de features (Pandas, PySpark).
3.  **Modelagem**: Treinamento do modelo preditivo (Scikit-Learn, TensorFlow).
4.  **Validação**: Avaliação da performance utilizando métricas como acurácia e matriz de confusão.
5.  **Implantação**: Modelo integrado ao sistema para previsão em tempo real.

### 2.2. Domínio de Problema: Previsão de Churn em Telecomunicações

* **Problema**: Prever quais clientes de uma empresa de telecomunicações têm maior probabilidade de cancelar seus serviços (churn).
* **Justificativa**: A previsão de churn é crucial para empresas de serviços, pois permite identificar clientes insatisfeitos e implementar estratégias de retenção, reduzindo custos e aumentando a receita.
* **Tipo de Análise**: Classificação (prever se um cliente vai ou não cancelar o serviço).

### 2.3. Justificativa da Escolha dos Modelos de Banco de Dados

Para o domínio de previsão de churn, propõe-se a utilização combinada de bancos de dados relacionais e NoSQL:

1.  **Banco Relacional (SQL)**:
    * **Vantagens**: Estrutura bem definida, suporte a transações ACID, ideal para dados estruturados, como dados transacionais e informações cadastrais.
    * **Uso**: Armazenar dados transacionais, como histórico de pagamentos, contratos e informações cadastrais dos clientes.
    * **Exemplo de dados**: Dados de clientes (nome, endereço, plano), histórico de pagamentos, informações de contrato.
2.  **Banco NoSQL (MongoDB)**:
    * **Vantagens**: Escalabilidade horizontal, flexibilidade para dados semiestruturados ou não estruturados, ideal para dados de interação e feedback.
    * **Uso**: Armazenar logs de interações com clientes, feedbacks, ou dados de redes sociais.
    * **Exemplo de dados**: Logs de atendimento, comentários de clientes, dados de uso de aplicativos.
* **Justificativa**: A combinação dos dois modelos permite lidar com dados estruturados (transacionais) e não estruturados (interações e feedbacks), atendendo às necessidades do pipeline de análise preditiva. A flexibilidade do NoSQL complementa a estrutura rígida do SQL, permitindo armazenar uma variedade maior de dados relevantes para a previsão de churn.

### 2.4. Modelo de Dados Proposto

#### Modelo Relacional (SQL):

* Tabela Clientes:
  
    ```SQL
    CREATE TABLE Clientes (
      id_cliente INT PRIMARY KEY,
      nome VARCHAR(100),
      telefone VARCHAR(15),
      data_adesao DATE,
      status VARCHAR(10),
      plano VARCHAR(50),
      tempo_assinatura INT
    );
    ```

* Tabela Transacoes:

    ```SQL
    CREATE TABLE Transacoes (
      id_transacao INT PRIMARY KEY,
      id_cliente INT,
      valor DECIMAL(10, 2),
      data_transacao DATE,
      FOREIGN KEY (id_cliente) REFERENCES Clientes(id_cliente)
    );
    ```

#### Modelo NoSQL (MongoDB):

* Coleção Interacoes:

    ```JSON
    {
    "id_cliente": 1,
    "tipo_interacao": "reclamação",
    "data": "2023-10-01T00:00:00Z",
    "detalhes": "Cliente reclamou sobre lentidão na internet.",
    "canal": "telefone",
    "sentimento": "negativo"
    }
    ```

### 2.5. Exemplos de Manipulação de Dados

#### SQL (Relacional):

* Inserir um novo cliente:

    ```SQL
    INSERT INTO Clientes (id_cliente, nome, telefone, data_adesao, status, plano, tempo_assinatura)
    VALUES (1, 'João Silva', '11999999999', '2023-01-01', 'ativo', 'Plano Premium', 12);
    ```
    
* Consultar clientes ativos com tempo de assinatura superior a 6 meses:

    ```SQL
    SELECT * FROM Clientes WHERE status = 'ativo' AND tempo_assinatura > 6;
    ```

#### NoSQL (MongoDB):

* Inserir uma interação:
  
    ```javascript
    db.Interacoes.insertOne({
      id_cliente: 1,
      tipo_interacao: "reclamação",
      data: ISODate("2023-10-01"),
      detalhes: "Cliente reclamou sobre lentidão na internet.",
      "canal": "telefone",
      "sentimento": "negativo"
    });
    ```
    
* Consultar interações de um cliente com sentimento negativo:

    ```javascript
    db.Interacoes.find({ id_cliente: 1, sentimento: "negativo" });
    ```

### 2.6. Escolha do Ambiente para Armazenamento de Dados

**Ambiente Escolhido:** Data Lakehouse.

O Data Lakehouse é uma arquitetura moderna que combina as melhores características de um Data Lake (escalabilidade e capacidade de armazenar dados brutos e não estruturados) com as funcionalidades de um Data Warehouse (estrutura, governança e suporte a consultas SQL). Essa combinação o torna ideal para pipelines de análise preditiva, especialmente em cenários como a previsão de churn, onde é necessário lidar com grandes volumes de dados de diferentes fontes e formatos.

**Justificativa da Escolha:**

1.  **Integração de Dados Brutos e Estruturados:**
    * O Data Lakehouse permite armazenar dados brutos (ex.: logs de interações, feedbacks de clientes) em formatos como JSON, Parquet ou CSV, enquanto também suporta dados estruturados (ex.: tabelas SQL) após o pré-processamento.
    * Exemplo: Dados brutos de logs de atendimento ao cliente são armazenados no Data Lake, enquanto dados transformados (ex.: métricas de uso do serviço) são armazenados em tabelas estruturadas para consulta rápida.
2.  **Escalabilidade e Desempenho:**
    * O Data Lakehouse é altamente escalável, permitindo o armazenamento e processamento de grandes volumes de dados sem comprometer o desempenho.
    * Exemplo: Em um cenário de telecomunicações, milhões de registros de interações com clientes podem ser armazenados e processados em tempo real.
3.  **Governança e Qualidade de Dados:**
    * Tecnologias como Delta Lake, Apache Iceberg e Apache Hudi oferecem recursos avançados de governança, como transações ACID, versionamento de dados e auditoria de mudanças.
    * Exemplo: O Delta Lake permite rastrear alterações nos dados, garantindo consistência e confiabilidade ao longo do pipeline de análise preditiva.
4.  **Suporte a Ferramentas de Análise e Machine Learning:**
    * O Data Lakehouse é compatível com ferramentas populares de análise e machine learning, como Apache Spark, Databricks, TensorFlow e Scikit-Learn.
    * Exemplo: Dados armazenados no Data Lakehouse podem ser diretamente utilizados para treinar modelos de machine learning, como Random Forest ou XGBoost, sem a necessidade de movimentação adicional de dados.
5.  **Flexibilidade e Custo-Efetividade:**
    * Ao unir as funcionalidades de Data Lake e Data Warehouse, o Data Lakehouse reduz a complexidade e os custos associados à manutenção de duas infraestruturas separadas.
    * Exemplo: Empresas podem armazenar dados brutos e processados em um único ambiente, simplificando a gestão e reduzindo custos operacionais.

**Exemplo de Uso no Contexto de Churn:**

* **Armazenamento de Dados Brutos:** Logs de interações com clientes (ex.: reclamações, feedbacks) são armazenados no Data Lake em formato JSON.
* **Pré-Processamento:** Utilizando Apache Spark e Delta Lake, os dados brutos são limpos, transformados e enriquecidos com informações adicionais (ex.: tempo de assinatura, histórico de pagamentos).
* **Armazenamento Estruturado:** Os dados processados são armazenados em tabelas estruturadas no Data Warehouse, utilizando tecnologias como Apache Iceberg para otimização de consultas.
* **Consulta e Análise:** Analistas e cientistas de dados podem acessar os dados tratados via SQL ou APIs, facilitando a criação de dashboards e a execução de modelos preditivos.

### 2.6.1. Fluxo de Dados no Data Lakehouse

O fluxo de dados no Data Lakehouse pode ser dividido em quatro etapas principais:

1.  **Ingestão:**
    * Dados brutos são coletados de diversas fontes (ex.: sistemas de CRM, logs de atendimento, redes sociais) e armazenados no Data Lake.
    * Exemplo: Dados de interações com clientes são ingeridos em formato JSON no Amazon S3 ou Azure Data Lake.
2.  **Processamento:**
    * Utilizando ferramentas como Apache Spark e Delta Lake, os dados brutos são limpos, transformados e enriquecidos.
    * Exemplo: Logs de atendimento são processados para extrair métricas como tempo de resposta, tipo de reclamação e sentimento do cliente.
3.  **Armazenamento Estruturado:**
    * Os dados processados são armazenados em tabelas estruturadas, utilizando tecnologias como Apache Iceberg ou Delta Tables.
    * Exemplo: Dados de clientes e métricas de uso são armazenados em tabelas SQL para consulta rápida.
4.  **Consulta e Análise:**
    * Analistas e cientistas de dados acessam os dados tratados via SQL ou APIs, utilizando ferramentas como Databricks ou Tableau.
    * Exemplo: Consultas SQL são executadas para identificar padrões de churn e alimentar modelos preditivos.

### 2.6.2. Métricas de Avaliação do Modelo

Para garantir a qualidade das previsões de churn, são utilizadas as seguintes métricas:

1.  **Acurácia:**
    * Mede a proporção de previsões corretas em relação ao total de previsões.
    * Exemplo: Um modelo com 90% de acurácia prevê corretamente 90% dos casos de churn.
2.  **Precisão:**
    * Indica a proporção de previsões corretas dentro da classe "churn".
    * Exemplo: Uma precisão de 85% significa que 85% dos clientes identificados como propensos a churn realmente cancelaram o serviço.
3.  **Recall:**
    * Mede a capacidade do modelo de capturar todos os casos reais de churn.
    * Exemplo: Um recall de 80% indica que o modelo identificou 80% dos clientes que realmente cancelaram o serviço.
4.  **Matriz de Confusão:**
    * Avalia erros e acertos na classificação, dividindo os resultados em verdadeiros positivos, falsos positivos, verdadeiros negativos e falsos negativos.
    * Exemplo: A matriz de confusão ajuda a identificar se o modelo está tendendo a falsos positivos (clientes erroneamente classificados como propensos a churn).

### 2.6.3. Desafios na Implementação

A implementação de um Data Lakehouse e a construção de modelos preditivos enfrentam alguns desafios:

1.  **Limpeza de Dados:**
    * Dados brutos podem conter valores ausentes, inconsistentes ou duplicados, exigindo técnicas avançadas de limpeza e transformação.
    * Exemplo: Logs de atendimento podem conter registros incompletos ou com formatos inconsistentes.
2.  **Feature Engineering:**
    * A criação de variáveis relevantes (features) é crucial para melhorar a precisão do modelo.
    * Exemplo: Variáveis como "número de reclamações nos últimos 6 meses" ou "tempo médio de resposta ao cliente" podem ser criadas a partir dos dados brutos.
3.  **Escolha do Modelo Ideal:**
    * A comparação de diferentes algoritmos (ex.: Random Forest, XGBoost, Redes Neurais) é necessária para selecionar o modelo mais adequado ao problema.
    * Exemplo: Um modelo de Random Forest pode ser mais eficaz para dados tabulares, enquanto redes neurais podem ser mais adequadas para dados de texto.
4.  **Escalabilidade:**
    * O modelo deve ser capaz de lidar com grandes volumes de dados e crescer conforme a demanda.
    * Exemplo: A utilização de ferramentas como Apache Spark e Delta Lake garante a escalabilidade do pipeline.

### 2.6.4. Governança de Dados no Data Lakehouse

A governança de dados é essencial para garantir a qualidade, segurança e conformidade dos dados no Data Lakehouse. As principais práticas incluem:

1.  **Versionamento de Dados:**
    * Utilizando Delta Lake, é possível rastrear mudanças nos dados e reverter para versões anteriores, se necessário.
    * Exemplo: Alterações em tabelas de clientes podem ser versionadas para auditoria e controle.
2.  **Catálogo de Metadados:**
    * Ferramentas como Apache Hive Metastore ou AWS Glue documentam os schemas e metadados dos dados, facilitando a descoberta e o uso.
    * Exemplo: Um catálogo de metadados permite que analistas encontrem rapidamente tabelas relevantes para análise.
3.  **Controle de Acesso:**
    * Políticas de segurança são implementadas para proteger dados sensíveis e garantir conformidade com regulamentações como a LGPD.
    * Exemplo: Acesso a dados de clientes é restrito a usuários autorizados, com auditoria de atividades.

### 2.6.5. Justificativa

A escolha do Data Lakehouse como ambiente de armazenamento e processamento de dados oferece uma solução robusta e escalável para a análise preditiva de churn. Ao combinar a flexibilidade do Data Lake com a estrutura do Data Warehouse, o Data Lakehouse permite a integração de dados brutos e processados, facilitando a construção de modelos preditivos precisos e confiáveis. A adoção de tecnologias como Delta Lake, Apache Iceberg e ferramentas de governança garante a qualidade e a segurança dos dados, enquanto a escalabilidade e o suporte a machine learning tornam o Data Lakehouse uma escolha ideal para empresas de telecomunicações.

## 3. Conclusão

Este trabalho apresentou uma abordagem para a implementação de um pipeline de análise preditiva, utilizando modelos de banco de dados relacionais e NoSQL para armazenar e processar dados. A escolha do Data Lakehouse como ambiente de armazenamento permite a integração de dados brutos e pré-processados, facilitando a construção de modelos preditivos robustos e escaláveis.

A combinação de bancos de dados relacionais e NoSQL demonstrou ser eficaz para lidar com a diversidade de dados presentes no domínio de previsão de churn em telecomunicações. O modelo relacional oferece estrutura e consistência para dados transacionais, enquanto o NoSQL proporciona flexibilidade para dados de interação e feedback. A escolha do MongoDB como banco NoSQL, com sua capacidade de escalar horizontalmente e flexibilidade de esquema, mostrou-se adequada para o armazenamento de dados semiestruturados e não estruturados.

O Data Lakehouse, com sua capacidade de unificar dados de diferentes fontes e formatos, emerge como uma solução ideal para pipelines de análise preditiva. A adoção de tecnologias como Delta Lake, Apache Iceberg ou Apache Hudi, juntamente com ferramentas como Databricks, AWS Lake Formation ou Google BigLake, permite a construção de um ambiente robusto e escalável para o armazenamento e processamento de dados.

A previsão de churn em telecomunicações foi utilizada como exemplo para demonstrar a aplicabilidade dos conceitos discutidos. A implementação de modelos de A previsão de churn em telecomunicações foi utilizada como exemplo para demonstrar a aplicabilidade dos conceitos discutidos. A implementação de modelos de classificação de churn, alimentados por dados armazenados e processados no Data Lakehouse, pode auxiliar as empresas a identificarem clientes insatisfeitos e implementar estratégias de retenção eficazes.

### Desafios e Trabalhos Futuros:

Durante a elaboração deste trabalho, alguns desafios foram identificados, como a necessidade de garantir a qualidade e a consistência dos dados em um ambiente distribuído e heterogêneo. Em trabalhos futuros, pretende-se explorar técnicas de governança de dados e qualidade de dados para o Data Lakehouse, bem como avaliar o desempenho de diferentes modelos de machine learning para a previsão de churn.

Além disso, a implementação de um pipeline completo de análise preditiva, desde a coleta de dados até a visualização dos resultados, permitirá validar a eficácia da abordagem proposta. A avaliação de outros modelos de banco de dados e ambientes de armazenamento também pode fornecer insights valiosos para a otimização do pipeline.

A combinação de tecnologias e abordagens propostas neste trabalho oferece uma solução robusta e escalável para problemas de análise preditiva, com potencial para ser aplicada em diversos domínios e contextos.
