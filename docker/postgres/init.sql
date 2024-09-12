\c db;
CREATE TABLE public.fato_venda (
    id_venda INT PRIMARY KEY,
    id_data INT,
    id_usuario INT,
    id_categoria INT,
    valor_venda DECIMAL(10,2),
    quantidade INT
);

CREATE TABLE public.dim_data (
    id_data INT PRIMARY KEY,
    data DATE,
    dia INT,
    mes INT,
    ano INT,
    trimestre INT
);

CREATE TABLE public.dim_usuario (
    id_usuario INT PRIMARY KEY,
    nome VARCHAR(100)
);

CREATE TABLE public.dim_categoria (
    id_categoria INT PRIMARY KEY,
    nome_categoria VARCHAR(50)
);

CREATE TABLE public.total_vendas_por_usuario (
    id INTEGER PRIMARY KEY,
    nome VARCHAR(100) NOT NULL,
    total_vendas DECIMAL(10, 2) NOT NULL
);

CREATE TABLE public.quantidade_vendas_por_categoria (
    id INTEGER PRIMARY KEY,
    nome_categoria VARCHAR(100) NOT NULL,
    quantidade_vendas INTEGER NOT NULL
);

CREATE TABLE public.media_vendas_por_categoria (
    id INTEGER PRIMARY KEY,
    nome_categoria VARCHAR(100) NOT NULL,
    media_vendas DECIMAL(10, 2) NOT NULL
);
