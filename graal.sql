PRAGMA foreign_keys = ON;

DROP TABLE IF EXISTS produto;
DROP TABLE IF EXISTS pedido;
DROP TABLE IF EXISTS item_pedido;
DROP TABLE IF EXISTS venda;
DROP TABLE IF EXISTS cargo;
DROP TABLE IF EXISTS funcionario;

CREATE TABLE produto (
    id_produto INTEGER PRIMARY KEY AUTOINCREMENT,
    nome TEXT,
    codigo_de_barras INTEGER,
    preco REAL,
    data_validade TEXT,
    peso_kg REAL,
    fornecedor TEXT,
    estoque INTEGER DEFAULT 0
);

CREATE TABLE pedido (
    id_pedido INTEGER PRIMARY KEY AUTOINCREMENT,
    data_pedido TEXT,
    status TEXT
);

CREATE TABLE item_pedido (
    id_item INTEGER PRIMARY KEY AUTOINCREMENT,
    id_pedido INTEGER,
    id_produto INTEGER,
    quantidade INTEGER,
    preco_unitario REAL,
    FOREIGN KEY (id_pedido) REFERENCES pedido(id_pedido),
    FOREIGN KEY (id_produto) REFERENCES produto(id_produto)
);

CREATE TABLE venda (
    id_venda INTEGER PRIMARY KEY AUTOINCREMENT,
    id_pedido INTEGER,
    data_venda TEXT,
    valor_total REAL,
    forma_pagamento TEXT,
    cpf_cliente TEXT,
    FOREIGN KEY (id_pedido) REFERENCES pedido(id_pedido)
);

CREATE TABLE cargo (
    id_cargo INTEGER PRIMARY KEY AUTOINCREMENT,
    nome TEXT UNIQUE
);

CREATE TABLE funcionario (
    id_funcionario INTEGER PRIMARY KEY AUTOINCREMENT,
    nome TEXT,
    usuario TEXT UNIQUE,
    senha TEXT,
    id_cargo INTEGER,
    FOREIGN KEY (id_cargo) REFERENCES cargo(id_cargo)
);
