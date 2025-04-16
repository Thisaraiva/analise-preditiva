# Implementação do Ambiente para Armazenamento de Dados e ETL para Previsão de Churn

## 2. Implementação do Ambiente para Armazenamento de Dados Brutos/Pré-Processados

Conforme definido na Tarefa N1, o ambiente escolhido para o armazenamento de dados relacionados ao problema de previsão de churn em telecomunicações é um **Data Lakehouse**. Para simular as etapas iniciais deste ambiente, foram criadas duas pastas dentro do diretório `data_lake_churn`:

* **`raw`**: Para armazenar os dados brutos gerados sinteticamente.
* **`processed`**: Para armazenar os dados após uma etapa inicial de pré-processamento (ETL).

A estrutura de pastas criada é a seguinte:

```mermaid
data_lake_churn/
├── processed/
├── raw/
├── etl_datalake_churn.py
└── gerar_dados_churn.py
```

## 3. Inserção de ao Menos 500 Amostras de Dados

### a) Geração Sintética dos Dados

Para atender à necessidade de inserir ao menos 500 amostras de dados, foi desenvolvido um script em Python (`gerar_dados_churn.py`) que utiliza a biblioteca `Faker` para gerar dados sintéticos relacionados ao domínio do problema de churn em telecomunicações. O script gera dados para três entidades principais, seguindo o modelo de dados proposto na Tarefa N1:

1.  **Clientes (`clientes_bruto.csv`):** Contém informações sobre os clientes, como ID, nome, telefone, data de adesão, status, plano e tempo de assinatura. Foram geradas 500 amostras de clientes.
2.  **Transações (`transacoes_bruto.csv`):** Registra as transações realizadas pelos clientes, incluindo ID da transação, ID do cliente, valor e data da transação. Um número variável de transações (entre 1 e 10) foi gerado para cada cliente.
3.  **Interações (`interacoes_bruto.json`):** Simula interações dos clientes com a empresa, como reclamações, elogios, dúvidas e sugestões, incluindo detalhes, canal e sentimento. Um número variável de interações (entre 0 e 5) foi gerado para cada cliente.

O processo de geração envolveu a utilização de funcionalidades da biblioteca `Faker` para criar dados realistas, como nomes, telefones e datas aleatórias dentro de um período específico. Para as transações e interações, a geração foi vinculada aos IDs dos clientes gerados previamente, garantindo a integridade relacional.

Os dados brutos gerados foram salvos na pasta `data_lake_churn/raw/` nos seguintes arquivos:

* `clientes_bruto.csv`
* `transacoes_bruto.csv`
* `interacoes_bruto.json`

### b) Demonstração das Operações ETL (Extraction, Transformation, Load)

Para conceituar e demonstrar as operações ETL, foi criado um script Python (`etl_datalake_churn.py`). Este script realiza as seguintes etapas:

1.  **Extraction (Extração):**
    * Lê os dados brutos dos arquivos localizados na pasta `data_lake_churn/raw/`.
        * `extract_clientes()`: Extrai os dados do arquivo `clientes_bruto.csv` utilizando a biblioteca `pandas`.
        * `extract_transacoes()`: Extrai os dados do arquivo `transacoes_bruto.csv` utilizando a biblioteca `pandas`.
        * `extract_interacoes()`: Extrai os dados do arquivo `interacoes_bruto.json` utilizando a biblioteca `json`.

2.  **Transformation (Transformação):**
    * Aplica transformações básicas nos dados extraídos. Embora simples neste exemplo, estas etapas representam o processo de limpeza, formatação e enriquecimento dos dados.
        * `transform_clientes()`: Converte a coluna `data_adesao` para o tipo datetime e as colunas `status` e `plano` para o tipo category.
        * `transform_transacoes()`: Converte a coluna `data_transacao` para o tipo datetime.
        * `transform_interacoes()`: Converte a coluna `data` para o formato datetime, e converte as colunas `tipo_interacao`, `canal` e `sentimento` para lowercase.

3.  **Load (Carregamento):**
    * Carrega os dados transformados em arquivos na pasta `data_lake_churn/processed/`.
        * `load_clientes()`: Salva o DataFrame de clientes transformado no arquivo `clientes_tratado.csv`.
        * `load_transacoes()`: Salva o DataFrame de transações transformado no arquivo `transacoes_tratado.csv`.
        * `load_interacoes()`: Salva a lista de interações transformada no arquivo `interacoes_tratado.json`.

Após a execução do script `etl_datalake_churn.py`, a pasta `data_lake_churn/processed/` conterá os seguintes arquivos com os dados pré-processados:

* `clientes_tratado.csv`
* `transacoes_tratado.csv`
* `interacoes_tratado.json`

Este processo demonstra um fluxo básico de ETL, essencial para preparar os dados brutos para etapas subsequentes de análise e modelagem preditiva dentro do ambiente Data Lakehouse proposto.