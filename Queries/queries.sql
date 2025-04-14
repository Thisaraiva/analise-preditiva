USE AnaliseMultidimensional;

-- Query (a): Alunos de SC com Instrutor de Curso Diferente e Nota > 70
SELECT e.nome, a.Instituicao, aa.notas
FROM Aulas_assistidas aa
JOIN Estudante e ON aa.estudanteID = e.estudanteID
JOIN Instrutor i ON aa.instrutorID = i.instrutorID
JOIN Aula a ON aa.aulaID = a.aulaID
WHERE a.estado = 'SC' 
  AND i.curso != e.curso 
  AND aa.notas > 70;

-- Query (b): Média de Notas por Aluno e Instrutor em Joinville
SELECT e.nome, i.instrutorID, AVG(aa.notas) AS media_notas
FROM Aulas_assistidas aa
JOIN Estudante e ON aa.estudanteID = e.estudanteID
JOIN Instrutor i ON aa.instrutorID = i.instrutorID
JOIN Aula a ON aa.aulaID = a.aulaID
WHERE a.cidade = 'Joinville'
GROUP BY e.nome, i.instrutorID;

-- Query (c): ROLLUP (Agregação por Instrutor)
SELECT i.instrutorID, AVG(aa.notas) AS media_notas
FROM Aulas_assistidas aa
JOIN Instrutor i ON aa.instrutorID = i.instrutorID
GROUP BY ROLLUP(i.instrutorID);

-- Query (d): Média de Pontuação por Curso do Estudante
SELECT e.curso, AVG(aa.notas) AS media_notas
FROM Aulas_assistidas aa
JOIN Estudante e ON aa.estudanteID = e.estudanteID
GROUP BY e.curso;

-- Query (e): Drill Down (Curso do Instrutor + Estudante)
SELECT i.curso AS curso_instrutor, e.curso AS curso_estudante, AVG(aa.notas) AS media_notas
FROM Aulas_assistidas aa
JOIN Estudante e ON aa.estudanteID = e.estudanteID
JOIN Instrutor i ON aa.instrutorID = i.instrutorID
GROUP BY i.curso, e.curso;

-- Query (f): ROLLUP para Granularidades Geográficas
SELECT a.estado, a.cidade, a.Instituicao, AVG(aa.notas) AS media_notas
FROM Aulas_assistidas aa
JOIN Aula a ON aa.aulaID = a.aulaID
GROUP BY ROLLUP(a.estado, a.cidade, a.Instituicao);

-- Query (g): Simulação de CUBO (para SQL Server que não tem CUBE)
SELECT a.estado, a.cidade, AVG(aa.notas) AS media_notas
FROM Aulas_assistidas aa
JOIN Aula a ON aa.aulaID = a.aulaID
GROUP BY a.estado, a.cidade WITH ROLLUP
UNION ALL
SELECT NULL, a.cidade, AVG(aa.notas)
FROM Aulas_assistidas aa
JOIN Aula a ON aa.aulaID = a.aulaID
GROUP BY a.cidade WITH ROLLUP;