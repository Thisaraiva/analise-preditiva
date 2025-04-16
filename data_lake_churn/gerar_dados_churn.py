import pandas as pd
from datetime import datetime
from faker import Faker
import random
import json
import os

fake = Faker('pt_BR')

def gerar_dados_clientes(num_clientes=500):
    """Gera dados sintéticos para a tabela Clientes."""
    data = []
    planos = ['Básico', 'Intermediário', 'Premium', 'Familiar']
    status_list = ['ativo', 'inativo']
    for i in range(1, num_clientes + 1):
        data_adesao = fake.date_between(start_date='-2y', end_date='today')
        tempo_assinatura = (datetime.now().date() - data_adesao).days // 30
        data.append({
            'id_cliente': i,
            'nome': fake.name(),
            'telefone': fake.phone_number(),
            'data_adesao': data_adesao.strftime('%Y-%m-%d'),
            'status': random.choice(status_list),
            'plano': random.choice(planos),
            'tempo_assinatura': tempo_assinatura
        })
    return pd.DataFrame(data)

def gerar_dados_transacoes(df_clientes, num_transacoes_por_cliente_min=1, num_transacoes_por_cliente_max=10):
    """Gera dados sintéticos para a tabela Transacoes."""
    data = []
    for id_cliente in df_clientes['id_cliente']:
        data_adesao_str = df_clientes[df_clientes['id_cliente'] == id_cliente]['data_adesao'].iloc[0]
        data_adesao = datetime.strptime(data_adesao_str, '%Y-%m-%d').date()
        num_transacoes = random.randint(num_transacoes_por_cliente_min, num_transacoes_por_cliente_max)
        for _ in range(num_transacoes):
            data_transacao = fake.date_between(start_date=data_adesao, end_date='today')
            valor = round(random.uniform(10, 200), 2)
            data.append({
                'id_transacao': fake.unique.random_number(digits=8),
                'id_cliente': id_cliente,
                'valor': valor,
                'data_transacao': data_transacao.strftime('%Y-%m-%d')
            })
    return pd.DataFrame(data)

def gerar_dados_interacoes(df_clientes, num_interacoes_por_cliente_min=0, num_interacoes_por_cliente_max=5):
    """Gera dados sintéticos para a coleção Interacoes (simulando dados NoSQL)."""
    data = []
    tipos_interacao = ['reclamação', 'elogio', 'dúvida', 'sugestão']
    canais = ['telefone', 'email', 'chat', 'redes sociais']
    sentimentos = ['positivo', 'negativo', 'neutro']
    for id_cliente in df_clientes['id_cliente']:
        data_interacao = fake.date_between(start_date='-1y', end_date='today')
        data.append({
            'id_cliente': id_cliente,
            'tipo_interacao': random.choice(tipos_interacao),
            'data': data_interacao.strftime('%Y-%m-%dT%H:%M:%SZ'),
            'detalhes': fake.sentence(),
            'canal': random.choice(canais),
            'sentimento': random.choice(sentimentos)
        })
    return data

if __name__ == "__main__":
    num_amostras = 500
    df_clientes = gerar_dados_clientes(num_amostras)
    df_transacoes = gerar_dados_transacoes(df_clientes)
    lista_interacoes = gerar_dados_interacoes(df_clientes)

    # Salvar os dados gerados (simulando o armazenamento bruto)
    base_path = '.'  # Diretório corrente (data_lake_churn)
    raw_data_path = os.path.join(base_path, 'raw')
    os.makedirs(raw_data_path, exist_ok=True)

    df_clientes.to_csv(os.path.join(raw_data_path, 'clientes_bruto.csv'), index=False)
    df_transacoes.to_csv(os.path.join(raw_data_path, 'transacoes_bruto.csv'), index=False)

    with open(os.path.join(raw_data_path, 'interacoes_bruto.json'), 'w') as f:
        json.dump(lista_interacoes, f, indent=4)

    print(f"Dados brutos simulados e salvos em '{raw_data_path}'.")