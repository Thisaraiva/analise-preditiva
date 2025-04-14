import pandas as pd
import os
from sqlalchemy import create_engine
import random

# Configuração do Data Lake
os.makedirs("data_lake/raw", exist_ok=True)
os.makedirs("data_lake/processed", exist_ok=True)

# Conexão com SQL Server
engine = create_engine(
    "mssql+pyodbc://NOTE_THIAGO\\SQLEXPRESS/AnaliseMultidimensional?"
    "trusted_connection=yes&driver=ODBC+Driver+17+for+SQL+Server"
)

# Extração: Buscar dados do SQL Server
def extract_data():
    query = "SELECT * FROM Estudante"
    df_estudantes = pd.read_sql(query, engine)
    
    query = "SELECT * FROM Aulas_assistidas"
    df_notas = pd.read_sql(query, engine)
    
    # Salvar dados brutos
    df_estudantes.to_csv("data_lake/raw/estudantes.csv", index=False)
    df_notas.to_csv("data_lake/raw/notas.csv", index=False)
    return df_estudantes, df_notas

# Transformação
def transform_data(df_estudantes, df_notas):
    # Calcular média de notas por aluno
    medias = df_notas.groupby('estudanteID')['notas'].mean().reset_index()
    
    # Juntar com dados dos estudantes
    df_final = pd.merge(df_estudantes, medias, on='estudanteID')
    
    # Adicionar status (exemplo de transformação)
    df_final['status'] = ['Ativo' if media > 70 else 'Inativo' 
                         for media in df_final['notas']]
    
    return df_final

def generate_report(df_final):
    """Gera relatório consolidado em formato JSON"""
    import json
    
    # Calcula métricas principais
    media_geral = df_final['notas'].mean()
    
    # Obtém o melhor instrutor (usando sintaxe SQL Server)
    query = """
        SELECT TOP 1 i.instrutorID, AVG(aa.notas) as media
        FROM Aulas_assistidas aa
        JOIN Instrutor i ON aa.instrutorID = i.instrutorID
        GROUP BY i.instrutorID
        ORDER BY media DESC
    """
    melhor_instrutor = pd.read_sql(query, engine).iloc[0].to_dict()
    
    # Obtém cidade com melhor desempenho (sintaxe SQL Server)
    query = """
        SELECT TOP 1 a.cidade, a.estado, AVG(aa.notas) as media
        FROM Aulas_assistidas aa
        JOIN Aula a ON aa.aulaID = a.aulaID
        GROUP BY a.cidade, a.estado
        ORDER BY media DESC
    """
    melhor_cidade = pd.read_sql(query, engine).iloc[0]
    cidade_formatada = f"{melhor_cidade['cidade']}/{melhor_cidade['estado']} ({melhor_cidade['media']:.2f})"
    
    # Calcula médias por curso
    medias_cursos = df_final.groupby('curso')['notas'].mean().to_dict()
    
    # Estrutura do relatório
    relatorio = {
        "metricas_principais": {
            "media_geral": round(media_geral, 2),
            "melhor_instrutor": {
                "id": int(melhor_instrutor['instrutorID']),
                "media": round(melhor_instrutor['media'], 2)
            },
            "cidade_melhor_desempenho": cidade_formatada
        },
        "estatisticas_cursos": {k: round(v, 2) for k, v in medias_cursos.items()}
    }
    
    # Salva o arquivo JSON
    os.makedirs('data_lake/processed', exist_ok=True)
    with open('data_lake/processed/relatorio_desempenho.json', 'w', encoding='utf-8') as f:
        json.dump(relatorio, f, indent=4, ensure_ascii=False)
    
    return relatorio

# Carga
def load_data(df):
    # Salvar dados processados
    df.to_csv("data_lake/processed/estudantes_processados.csv", index=False)
    
    # Carregar de volta para o SQL Server (opcional)
    df.to_sql('Estudantes_Processados', engine, if_exists='replace', index=False)

# Execução do ETL
if __name__ == "__main__":
    print("Iniciando processo ETL...")
    df_est, df_not = extract_data()
    df_final = transform_data(df_est, df_not)
    load_data(df_final)

    # Gera o relatório JSON
    relatorio = generate_report(df_final)
    print("Relatório gerado:", relatorio)

    print("ETL concluído com sucesso!")
    print(f"Arquivos salvos em: {os.path.abspath('data_lake')}")