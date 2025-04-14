CREATE DATABASE AnaliseMultidimensional;

USE AnaliseMultidimensional;

-- Tabelas Dimensão
CREATE TABLE Estudante (
    estudanteID INT PRIMARY KEY,
    nome VARCHAR(100),
    curso VARCHAR(50)
);

CREATE TABLE Instrutor (
    instrutorID INT PRIMARY KEY,
    curso VARCHAR(50)
);

CREATE TABLE Aula (
    aulaID INT PRIMARY KEY,
    Instituicao VARCHAR(100),
    cidade VARCHAR(50),
    estado VARCHAR(2)
);

-- Tabela Fato
CREATE TABLE Aulas_assistidas (
    estudanteID INT,
    instrutorID INT,
    aulaID INT,
    notas DECIMAL(5,2),
    FOREIGN KEY (estudanteID) REFERENCES Estudante(estudanteID),
    FOREIGN KEY (instrutorID) REFERENCES Instrutor(instrutorID),
    FOREIGN KEY (aulaID) REFERENCES Aula(aulaID)
);