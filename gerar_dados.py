import pandas as pd
from faker import Faker
import random
import pyodbc
from sqlalchemy import create_engine

fake = Faker('pt_BR')

# Gerar 500 estudantes
estudantes = [{
    "estudanteID": i,
    "nome": fake.name(),
    "curso": random.choice(["Engenharia", "Medicina", "Direito", "Administração"])
} for i in range(1, 501)]

# Gerar 50 instrutores
instrutores = [{
    "instrutorID": i,
    "curso": random.choice(["Matemática", "Biologia", "Direito", "Economia"])
} for i in range(101, 151)]

# Gerar 20 aulas (em SC e PR)
aulas = [{
    "aulaID": i,
    "Instituicao": random.choice(["UFSC", "UDESC", "PUCPR", "UNIVILLE"]),
    "cidade": random.choice(["Joinville", "Florianópolis", "Curitiba"]),
    "estado": random.choice(["SC", "PR"])
} for i in range(501, 521)]

# Gerar registros na tabela fato (500 registros)
aulas_assistidas = [{
    "estudanteID": random.randint(1, 500),
    "instrutorID": random.randint(101, 150),
    "aulaID": random.randint(501, 520),
    "notas": round(random.uniform(50, 100), 2)
} for _ in range(500)]

# Salvar em DataFrames
df_estudantes = pd.DataFrame(estudantes)
df_instrutores = pd.DataFrame(instrutores)
df_aulas = pd.DataFrame(aulas)
df_aulas_assistidas = pd.DataFrame(aulas_assistidas)

# Conexão com SQL Server usando SQLAlchemy (recomendado para pandas)
connection_string = (
    "mssql+pyodbc://NOTE_THIAGO\\SQLEXPRESS/AnaliseMultidimensional?"
    "trusted_connection=yes&driver=ODBC+Driver+17+for+SQL+Server"
)
engine = create_engine(connection_string)

# Inserir dados no SQL Server
df_estudantes.to_sql("Estudante", engine, if_exists="append", index=False)
df_instrutores.to_sql("Instrutor", engine, if_exists="append", index=False)
df_aulas.to_sql("Aula", engine, if_exists="append", index=False)
df_aulas_assistidas.to_sql("Aulas_assistidas", engine, if_exists="append", index=False)

print("Dados inseridos com sucesso!")