
### Usuários

| id | nome             |
|----|------------------|
| 3  | Tom Lindwall     |
| 1  | Rob Carsson      |
| 2  | Eli Preston      |
| 4  | Leif Shine       |
| 5  | Ingrid Hendrix   |
| 7  | Rock Rollman     |
| 6  | Lennart Skoglund |
| 8  | Helen Brolin     |
| 9  | Joan Callins     |

### Vendas

| id_venda | id_funcionario | id_categoria | data_venda | venda  |
|----------|----------------|--------------|------------|--------|
| 1        | 1              | 1            | 2017-10-01 | 21636  |
| 2        | 1              | 4            | 2018-05-12 | 3312   |
| 3        | 1              | 3            | 2019-02-01 | 11778  |
| 4        | 1              | 4            | 2019-03-11 | 2554   |
| 5        | 1              | 3            | 2018-09-07 | 4425   |
| 6        | 1              | 1            | 2017-02-02 | 12336  |
| 7        | 1              | 6            | 2017-04-10 | 32782  |
| 8        | 1              | 1            | 2017-05-02 | 46317  |
| 9        | 1              | 6            | 2017-06-10 | 2528   |
| 10       | 1              | 2            | 2017-11-06 | 11038  |
| 11       | 1              | 7            | 2017-05-09 | 106638 |
| 12       | 1              | 1            | 2019-05-01 | 14288  |
| 13       | 1              | 7            | 2019-05-11 | 917025 |
| 14       | 1              | 3            | 2017-02-02 | 29084  |
| 15       | 1              | 2            | 2018-05-03 | 17103  |
| 16       | 1              | 2            | 2018-07-07 | 5432   |
| 17       | 1              | 4            | 2017-11-11 | 158    |
| 18       | 1              | 1            | 2017-02-01 | 5805   |
| 19       | 1              | 4            | 2017-02-02 | 2496   |
| 20       | 1              | 4            | 2018-01-02 | 29719  |

### Categorias

| id | nome_categoria  |
|----|-----------------|
| 1  | Babywear        |
| 2  | Womens wear     |
| 3  | Womens Footwear |
| 4  | Sportwear       |
| 5  | Mens Clothes    |
| 6  | Bath Clothes    |
| 7  | Mens Footwear   |
| 8  | Childrens wear  |

### Sugestões de tabelas
1. Total de vendas por usuário:

```sql
CREATE TABLE total_vendas_por_usuario AS
SELECT u.id, u.nome, COALESCE(SUM(v.venda), 0) AS total_vendas
FROM Usuarios u
LEFT JOIN Vendas v ON u.id = v.id_funcionario
GROUP BY u.id, u.nome;
```

2. Quantidade de vendas por categoria:

```sql
CREATE TABLE quantidade_vendas_por_categoria AS
SELECT c.id, c.nome_categoria, COUNT(v.id_venda) AS quantidade_vendas
FROM Categorias c
LEFT JOIN Vendas v ON c.id = v.id_categoria
GROUP BY c.id, c.nome_categoria;
```

3. Total de vendas por ano:

```sql
CREATE TABLE total_vendas_por_ano AS
SELECT EXTRACT(YEAR FROM data_venda) AS ano, SUM(venda) AS total_vendas
FROM Vendas
GROUP BY EXTRACT(YEAR FROM data_venda);
```

4. Média de vendas por categoria:

```sql
CREATE TABLE media_vendas_por_categoria AS
SELECT c.id, c.nome_categoria, AVG(v.venda) AS media_vendas
FROM Categorias c
LEFT JOIN Vendas v ON c.id = v.id_categoria
GROUP BY c.id, c.nome_categoria;
```

5. Top 5 maiores vendas:

```sql
CREATE TABLE top_5_maiores_vendas AS
SELECT id_venda, id_categoria, data_venda, venda
FROM Vendas
ORDER BY venda DESC
LIMIT 5;
```

6. Vendas por mês em 2018:

```sql
CREATE TABLE vendas_por_mes_2018 AS
SELECT EXTRACT(MONTH FROM data_venda) AS mes, SUM(venda) AS total_vendas
FROM Vendas
WHERE EXTRACT(YEAR FROM data_venda) = 2018
GROUP BY EXTRACT(MONTH FROM data_venda)
ORDER BY mes;
```

7. Distribuição de vendas por trimestre:

```sql
CREATE TABLE vendas_por_trimestre AS
SELECT
    EXTRACT(YEAR FROM data_venda) AS ano,
    CONCAT('Q', EXTRACT(QUARTER FROM data_venda)) AS trimestre,
    SUM(venda) AS total_vendas
FROM Vendas
GROUP BY
    EXTRACT(YEAR FROM data_venda),
    EXTRACT(QUARTER FROM data_venda)
ORDER BY
    ano, trimestre;
```

### Sugestão de Modelagens
#### Star Schema:

No Star Schema, teríamos uma tabela de fatos central (Vendas) e dimensões ao redor.

Tabela de Fatos:
```sql
CREATE TABLE Fato_Vendas (
    id_venda INT PRIMARY KEY,
    id_data INT,
    id_funcionario INT,
    id_categoria INT,
    valor_venda DECIMAL(10,2),
    quantidade INT
);
```

Dimensões:
```sql
CREATE TABLE Dim_Data (
    id_data INT PRIMARY KEY,
    data DATE,
    dia INT,
    mes INT,
    ano INT,
    trimestre INT
);

CREATE TABLE Dim_Funcionario (
    id_funcionario INT PRIMARY KEY,
    nome VARCHAR(100)
);

CREATE TABLE Dim_Categoria (
    id_categoria INT PRIMARY KEY,
    nome_categoria VARCHAR(50)
);
```

#### Snowflake Schema:

O Snowflake Schema é uma extensão do Star Schema, onde as dimensões são normalizadas em múltiplas tabelas relacionadas.

Tabela de Fatos (igual ao Star Schema):
```sql
CREATE TABLE Fato_Vendas (
    id_venda INT PRIMARY KEY,
    id_data INT,
    id_funcionario INT,
    id_categoria INT,
    valor_venda DECIMAL(10,2),
    quantidade INT
);
```

Dimensões (com algumas normalizadas):
```sql
CREATE TABLE Dim_Data (
    id_data INT PRIMARY KEY,
    data DATE,
    id_mes INT,
    id_ano INT,
    id_trimestre INT
);

CREATE TABLE Dim_Mes (
    id_mes INT PRIMARY KEY,
    mes INT,
    nome_mes VARCHAR(20)
);

CREATE TABLE Dim_Ano (
    id_ano INT PRIMARY KEY,
    ano INT
);

CREATE TABLE Dim_Trimestre (
    id_trimestre INT PRIMARY KEY,
    trimestre INT,
    nome_trimestre VARCHAR(20)
);

CREATE TABLE Dim_Funcionario (
    id_funcionario INT PRIMARY KEY,
    nome VARCHAR(100),
    id_departamento INT
);

CREATE TABLE Dim_Departamento (
    id_departamento INT PRIMARY KEY,
    nome_departamento VARCHAR(50)
);

CREATE TABLE Dim_Categoria (
    id_categoria INT PRIMARY KEY,
    nome_categoria VARCHAR(50),
    id_grupo_categoria INT
);

CREATE TABLE Dim_Grupo_Categoria (
    id_grupo_categoria INT PRIMARY KEY,
    nome_grupo VARCHAR(50)
);
```

### SQL para Modelagem
#### Para o Star Schema:

1. Dim_Data:
```sql
INSERT INTO Dim_Data (id_data, data, dia, mes, ano, trimestre)
SELECT DISTINCT
    CAST(REPLACE(data_venda, '-', '') AS INT) AS id_data,
    data_venda AS data,
    EXTRACT(DAY FROM data_venda) AS dia,
    EXTRACT(MONTH FROM data_venda) AS mes,
    EXTRACT(YEAR FROM data_venda) AS ano,
    EXTRACT(QUARTER FROM data_venda) AS trimestre
FROM Vendas;
```

2. Dim_Funcionario:
```sql
INSERT INTO Dim_Funcionario (id_funcionario, nome)
SELECT id, nome
FROM Usuarios;
```

3. Dim_Categoria:
```sql
INSERT INTO Dim_Categoria (id_categoria, nome_categoria)
SELECT id, nome_categoria
FROM Categorias;
```

4. Fato_Vendas:
```sql
INSERT INTO Fato_Vendas (id_venda, id_data, id_funcionario, id_categoria, valor_venda, quantidade)
SELECT
    id_venda,
    CAST(REPLACE(data_venda, '-', '') AS INT) AS id_data,
    id_funcionario,
    id_categoria,
    venda AS valor_venda,
    1 AS quantidade  -- Assumindo que cada registro representa uma venda
FROM Vendas;
```

#### Para o Snowflake Schema:

1. Dim_Ano:
```sql
INSERT INTO Dim_Ano (id_ano, ano)
SELECT DISTINCT
    EXTRACT(YEAR FROM data_venda) AS id_ano,
    EXTRACT(YEAR FROM data_venda) AS ano
FROM Vendas;
```

2. Dim_Mes:
```sql
INSERT INTO Dim_Mes (id_mes, mes, nome_mes)
SELECT DISTINCT
    EXTRACT(MONTH FROM data_venda) AS id_mes,
    EXTRACT(MONTH FROM data_venda) AS mes,
    TO_CHAR(data_venda, 'Month') AS nome_mes
FROM Vendas;
```

3. Dim_Trimestre:
```sql
INSERT INTO Dim_Trimestre (id_trimestre, trimestre, nome_trimestre)
SELECT DISTINCT
    EXTRACT(QUARTER FROM data_venda) AS id_trimestre,
    EXTRACT(QUARTER FROM data_venda) AS trimestre,
    'Q' || EXTRACT(QUARTER FROM data_venda) AS nome_trimestre
FROM Vendas;
```

4. Dim_Data:
```sql
INSERT INTO Dim_Data (id_data, data, id_mes, id_ano, id_trimestre)
SELECT DISTINCT
    CAST(REPLACE(data_venda, '-', '') AS INT) AS id_data,
    data_venda AS data,
    EXTRACT(MONTH FROM data_venda) AS id_mes,
    EXTRACT(YEAR FROM data_venda) AS id_ano,
    EXTRACT(QUARTER FROM data_venda) AS id_trimestre
FROM Vendas;
```

5. Dim_Departamento (assumindo que não temos essa informação, então criamos um departamento genérico):
```sql
INSERT INTO Dim_Departamento (id_departamento, nome_departamento)
VALUES (1, 'Vendas');
```

6. Dim_Funcionario:
```sql
INSERT INTO Dim_Funcionario (id_funcionario, nome, id_departamento)
SELECT id, nome, 1 AS id_departamento
FROM Usuarios;
```

7. Dim_Grupo_Categoria (assumindo que não temos essa informação, então criamos um grupo genérico):
```sql
INSERT INTO Dim_Grupo_Categoria (id_grupo_categoria, nome_grupo)
VALUES (1, 'Produtos');
```

8. Dim_Categoria:
```sql
INSERT INTO Dim_Categoria (id_categoria, nome_categoria, id_grupo_categoria)
SELECT id, nome_categoria, 1 AS id_grupo_categoria
FROM Categorias;
```

9. Fato_Vendas (igual ao Star Schema):
```sql
INSERT INTO Fato_Vendas (id_venda, id_data, id_funcionario, id_categoria, valor_venda, quantidade)
SELECT
    id_venda,
    CAST(REPLACE(data_venda, '-', '') AS INT) AS id_data,
    id_funcionario,
    id_categoria,
    venda AS valor_venda,
    1 AS quantidade
FROM Vendas;
```
