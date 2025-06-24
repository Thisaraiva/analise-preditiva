import pandas as pd
import json
import os

def extract_clientes(file_path):
    """Extrai dados de clientes de um arquivo CSV."""
    return pd.read_csv(file_path)

def extract_transacoes(file_path):
    """Extrai dados de transações de um arquivo CSV."""
    return pd.read_csv(file_path)

def extract_interacoes(file_path):
    """Extrai dados de interações de um arquivo JSON."""
    with open(file_path, 'r') as f:
        return json.load(f)

def transform_clientes(df):
    """Transforma os dados de clientes (exemplo simples)."""
    df['data_adesao'] = pd.to_datetime(df['data_adesao'])
    df['status'] = df['status'].astype('category')
    df['plano'] = df['plano'].astype('category')
    return df

def transform_transacoes(df):
    """Transforma os dados de transações (exemplo simples)."""
    df['data_transacao'] = pd.to_datetime(df['data_transacao'])
    return df

def transform_interacoes(data):
    """Transforma os dados de interacoes (exemplo simples)."""
    for item in data:
        item['data'] = pd.to_datetime(item['data']).strftime('%Y-%m-%d %H:%M:%S')
        item['tipo_interacao'] = item['tipo_interacao'].lower()
        item['canal'] = item['canal'].lower()
        item['sentimento'] = item['sentimento'].lower()
    return data

def load_clientes(df, output_path):
    """Carrega os dados de clientes transformados em um arquivo CSV."""
    df.to_csv(os.path.join(output_path, 'clientes_tratado.csv'), index=False)
    print(f"Dados de clientes tratados e carregados em: {os.path.join(output_path, 'clientes_tratado.csv')}")

def load_transacoes(df, output_path):
    """Carrega os dados de transações transformados em um arquivo CSV."""
    df.to_csv(os.path.join(output_path, 'transacoes_tratado.csv'), index=False)
    print(f"Dados de transações tratados e carregados em: {os.path.join(output_path, 'transacoes_tratado.csv')}")

def load_interacoes(data, output_path):
    """Carrega os dados de interacoes transformados em um arquivo JSON."""
    with open(os.path.join(output_path, 'interacoes_tratado.json'), 'w') as f:
        json.dump(data, f, indent=4)
    print(f"Dados de interacoes tratados e carregados em: {os.path.join(output_path, 'interacoes_tratado.json')}")

if __name__ == "__main__":
    base_dir = os.path.dirname(os.path.abspath(__file__)) # Diretório corrente de data_lake_churn
    raw_data_path = os.path.join(base_dir, 'raw')
    processed_data_path = os.path.join(base_dir, 'processed')

    os.makedirs(raw_data_path, exist_ok=True)
    os.makedirs(processed_data_path, exist_ok=True)

    # Extração
    clientes_bruto_path = os.path.join(raw_data_path, 'clientes_bruto.csv')
    transacoes_bruto_path = os.path.join(raw_data_path, 'transacoes_bruto.csv')
    interacoes_bruto_path = os.path.join(raw_data_path, 'interacoes_bruto.json')

    df_clientes_extraido = extract_clientes(clientes_bruto_path)
    df_transacoes_extraido = extract_transacoes(transacoes_bruto_path)
    lista_interacoes_extraida = extract_interacoes(interacoes_bruto_path)

    print("Extração concluída.")

    # Transformação
    df_clientes_transformado = transform_clientes(df_clientes_extraido.copy())
    df_transacoes_transformado = transform_transacoes(df_transacoes_extraido.copy())
    lista_interacoes_transformada = transform_interacoes(lista_interacoes_extraida.copy())

    print("Transformação concluída.")

    # Load
    load_clientes(df_clientes_transformado, processed_data_path)
    load_transacoes(df_transacoes_transformado, processed_data_path)
    load_interacoes(lista_interacoes_transformada, processed_data_path)

    print("ETL concluído.")