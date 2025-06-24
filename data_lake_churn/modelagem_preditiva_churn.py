# C:\Programacao\Projetos\Python\analise-preditiva\data_lake_churn\modelagem_preditiva_churn.py

import pandas as pd
import json
import os
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score, confusion_matrix
import numpy as np

# --- 1. Carregamento dos Dados Tratados (Resultado da ETL) ---
def load_processed_data(processed_data_path):
    """Extrai dados de clientes de um arquivo CSV."""
    clientes_df = pd.read_csv(os.path.join(processed_data_path, 'clientes_tratado.csv'))
    transacoes_df = pd.read_csv(os.path.join(processed_data_path, 'transacoes_tratado.csv'))
    
    with open(os.path.join(processed_data_path, 'interacoes_tratado.json'), 'r') as f:
        interacoes_list = json.load(f)
    interacoes_df = pd.DataFrame(interacoes_list)
    
    return clientes_df, transacoes_df, interacoes_df

# --- 2. Feature Engineering e Unificação dos Dados ---
def prepare_data_for_modeling(clientes_df, transacoes_df, interacoes_df):
    """
    Realiza Feature Engineering e unifica os dados para a modelagem preditiva.
    
    Para simular o problema de 'churn', adicionaremos uma coluna 'churn' de forma sintética
    com base em algumas características dos dados gerados, como status 'inativo' e
    interações com sentimento negativo. Na vida real, o churn seria uma coluna real
    indicando se o cliente cancelou ou não.
    """
    
    # Converter colunas de data para datetime se ainda não estiverem
    clientes_df['data_adesao'] = pd.to_datetime(clientes_df['data_adesao'])
    transacoes_df['data_transacao'] = pd.to_datetime(transacoes_df['data_transacao'])
    
    # Feature: Total de transações por cliente
    transacoes_agg = transacoes_df.groupby('id_cliente').agg(
        total_valor_transacoes=('valor', 'sum'),
        num_transacoes=('id_transacao', 'count')
    ).reset_index()

    # Feature: Número de interações negativas por cliente
    interacoes_negativas = interacoes_df[interacoes_df['sentimento'] == 'negativo']
    interacoes_negativas_agg = interacoes_negativas.groupby('id_cliente').agg(
        num_interacoes_negativas=('id_cliente', 'count')
    ).reset_index()
    
    # Feature: Última interação (para churn)
    # Certifique-se de que 'data' é datetime para usar idxmax corretamente
    interacoes_df['data_interacao'] = pd.to_datetime(interacoes_df['data'])
    
    # Correção do SettingWithCopyWarning e manipulação robusta da última interação
    # Encontra o índice da linha com a data de interação mais recente para cada cliente
    idx_max_date = interacoes_df.groupby('id_cliente')['data_interacao'].idxmax()
    # Seleciona as linhas correspondentes a esses índices do DataFrame original
    interacoes_ultima = interacoes_df.loc[idx_max_date, ['id_cliente', 'data_interacao', 'tipo_interacao', 'sentimento', 'canal']].copy()
    
    interacoes_ultima.rename(columns={
        'tipo_interacao': 'tipo_ultima_interacao',
        'sentimento': 'sentimento_ultima_interacao',
        'canal': 'canal_ultima_interacao'
    }, inplace=True)
    
    # Unificar os DataFrames
    df_merged = clientes_df.copy()
    df_merged = pd.merge(df_merged, transacoes_agg, on='id_cliente', how='left')
    df_merged = pd.merge(df_merged, interacoes_negativas_agg, on='id_cliente', how='left')
    df_merged = pd.merge(df_merged, interacoes_ultima, on='id_cliente', how='left')

    # Preencher NaNs criados pelos merges (clientes sem transações/interações)
    # Correção dos FutureWarnings: usar atribuição direta em vez de inplace=True
    df_merged['total_valor_transacoes'] = df_merged['total_valor_transacoes'].fillna(0)
    df_merged['num_transacoes'] = df_merged['num_transacoes'].fillna(0)
    df_merged['num_interacoes_negativas'] = df_merged['num_interacoes_negativas'].fillna(0)
    
    # As colunas da última interação podem ter NaNs se o cliente não teve interações
    df_merged['tipo_ultima_interacao'] = df_merged['tipo_ultima_interacao'].fillna('desconhecido')
    df_merged['sentimento_ultima_interacao'] = df_merged['sentimento_ultima_interacao'].fillna('desconhecido')
    df_merged['canal_ultima_interacao'] = df_merged['canal_ultima_interacao'].fillna('desconhecido')


    # Converter colunas categóricas para numéricas (One-Hot Encoding)
    df_merged = pd.get_dummies(df_merged, columns=[
        'plano', 
        'tipo_ultima_interacao', 
        'sentimento_ultima_interacao', 
        'canal_ultima_interacao'
    ], dummy_na=False)
    
    # Remover colunas que não serão usadas diretamente ou que são redundantes e são do tipo data/hora
    # Garante que 'data_adesao', 'data_ultima_interacao' e 'data_transacao' (se ainda existissem) são removidas
    # antes de passar para o modelo
    cols_to_drop = ['nome', 'telefone', 'data_adesao', 'data_ultima_interacao']
    # Adicionar colunas de data/hora restantes se houverem, para garantir a remoção
    for col in ['data', 'data_interacao', 'data_transacao_x', 'data_transacao_y']: # nomes possíveis após merges ou renomeações
        if col in df_merged.columns:
            cols_to_drop.append(col)
    
    # Remove duplicatas da lista de colunas a serem dropadas e as remove do DataFrame
    df_merged.drop(columns=list(set(cols_to_drop)), inplace=True, errors='ignore')
    
    # Criar a coluna 'churn' sintética
    # Para fins de demonstração, consideraremos churn se:
    # 1. O status do cliente for 'inativo' OU
    # 2. Houve mais de 2 interações negativas E o plano não é 'Premium'
    # Esta é uma simulação, na vida real o 'churn' viria de dados históricos.
    df_merged['churn'] = ((df_merged['status'] == 'inativo') | 
                          ((df_merged['num_interacoes_negativas'] > 2) & (df_merged['plano_Premium'] == 0))) # Usar == 0 para False do OHE
    df_merged['churn'] = df_merged['churn'].astype(int) # Converte True/False para 1/0
    
    # Remover a coluna 'status' original após usar para criar 'churn'
    df_merged.drop(columns=['status'], inplace=True)

    # Reordenar colunas para que 'id_cliente' e 'churn' fiquem no início/fim
    cols = [col for col in df_merged.columns if col not in ['id_cliente', 'churn']]
    df_merged = df_merged[['id_cliente'] + cols + ['churn']]

    return df_merged

# --- 3. Treinamento e Avaliação dos Modelos ---
def train_and_evaluate_models(df_modeling):
    """
    Treina e avalia dois modelos preditivos (Random Forest e Regressão Logística).
    """
    
    # Definir features (X) e target (y)
    # Remove 'id_cliente' pois não é uma feature para o modelo
    X = df_modeling.drop(columns=['id_cliente', 'churn'])
    y = df_modeling['churn']
    
    # Dividir os dados em conjuntos de treino e teste
    # Garantir que todas as colunas em X sejam numéricas
    # Convertendo tipos de colunas que podem ter sido afetadas por dummies ou preenchimento
    X = X.select_dtypes(include=[np.number, np.bool_]).astype(float) # Garante que são numéricas (int, float, bool)
    
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42, stratify=y)
    
    print("\n--- Informações do Dataset de Treino/Teste ---")
    print(f"Dimensões de X_train: {X_train.shape}")
    print(f"Dimensões de X_test: {X_test.shape}")
    print(f"Proporção de Churn no Treino: {y_train.sum() / len(y_train):.2f}")
    print(f"Proporção de Churn no Teste: {y_test.sum() / len(y_test):.2f}")

    models = {
        'Random Forest Classifier': RandomForestClassifier(n_estimators=100, random_state=42),
        'Logistic Regression': LogisticRegression(random_state=42, solver='liblinear')
    }

    results = {}

    for name, model in models.items():
        print(f"\n--- Treinando e avaliando {name} ---")
        model.fit(X_train, y_train)
        y_pred = model.predict(X_test)
        
        accuracy = accuracy_score(y_test, y_pred)
        precision = precision_score(y_test, y_pred)
        recall = recall_score(y_test, y_pred)
        f1 = f1_score(y_test, y_pred)
        cm = confusion_matrix(y_test, y_pred)
        
        results[name] = {
            'Acurácia': accuracy,
            'Precisão': precision,
            'Recall': recall,
            'F1-Score': f1,
            'Matriz de Confusão': cm.tolist()
        }
        
        print(f"Modelo: {name}")
        print(f"Acurácia: {accuracy:.4f}")
        print(f"Precisão: {precision:.4f}")
        print(f"Recall: {recall:.4f}")
        print(f"F1-Score: {f1:.4f}")
        print("Matriz de Confusão:\n", cm)
        
    return results, X_train, X_test, y_train, y_test

if __name__ == "__main__":
    base_dir = os.path.dirname(os.path.abspath(__file__))
    processed_data_path = os.path.join(base_dir, 'processed')

    # Carregar dados tratados
    clientes_df, transacoes_df, interacoes_df = load_processed_data(processed_data_path)
    print("Dados tratados carregados com sucesso.")
    
    # Preparar dados para modelagem (Feature Engineering e Unificação)
    df_final_modeling = prepare_data_for_modeling(clientes_df, transacoes_df, interacoes_df)
    print("\nDados preparados para modelagem:")
    print(df_final_modeling.head())
    print(f"Dimensões do dataset final: {df_final_modeling.shape}")
    print(f"Contagem de Churn (1) vs Não Churn (0):\n{df_final_modeling['churn'].value_counts()}")
    
    # Treinar e avaliar modelos
    modeling_results, X_train, X_test, y_train, y_test = train_and_evaluate_models(df_final_modeling)
    
    print("\n--- Resultados Finais dos Modelos ---")
    for name, metrics in modeling_results.items():
        print(f"\nModelo: {name}")
        for metric, value in metrics.items():
            if metric == 'Matriz de Confusão':
                print(f"{metric}:\n {np.array(value)}")
            else:
                print(f"{metric}: {value:.4f}")

    # Salvar o dataset preparado para modelagem (opcional, mas bom para auditoria)
    df_final_modeling.to_csv(os.path.join(processed_data_path, 'dados_para_modelagem.csv'), index=False)
    print(f"\nDataset final para modelagem salvo em: {os.path.join(processed_data_path, 'dados_para_modelagem.csv')}")