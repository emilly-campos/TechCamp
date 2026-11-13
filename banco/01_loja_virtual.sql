-- LOJA VIRTUAL - MySQL / phpMyAdmin
-- Estrutura e dados baseados no Apendice A da apostila de Banco de Dados.
-- Execute uma vez em um banco novo. Nao apaga bancos ou tabelas existentes.
CREATE DATABASE loja_virtual DEFAULT CHARACTER SET utf8mb4;
USE loja_virtual;

CREATE TABLE clientes (
id_cliente INT PRIMARY KEY AUTO_INCREMENT,
nome       VARCHAR(100) NOT NULL,
cidade     VARCHAR(80) NOT NULL
) ENGINE=InnoDB;

CREATE TABLE categorias (
id_categoria INT PRIMARY KEY AUTO_INCREMENT,
nome         VARCHAR(80) NOT NULL
) ENGINE=InnoDB;

CREATE TABLE produtos (
id_produto   INT PRIMARY KEY AUTO_INCREMENT,
nome         VARCHAR(100) NOT NULL,
preco        DECIMAL(10,2) NOT NULL,
id_categoria INT NOT NULL,
FOREIGN KEY (id_categoria) REFERENCES categorias(id_categoria)
) ENGINE=InnoDB;

CREATE TABLE pedidos (
id_pedido   INT PRIMARY KEY AUTO_INCREMENT,
data_pedido DATE          NOT NULL,
status      VARCHAR(30)   NOT NULL,
valor_total DECIMAL(10,2) NOT NULL,
id_cliente INT NOT NULL,
FOREIGN KEY (id_cliente) REFERENCES clientes(id_cliente)
) ENGINE=InnoDB;

CREATE TABLE itens_pedido (
id_item        INT PRIMARY KEY AUTO_INCREMENT,
id_pedido      INT NOT NULL,
id_produto     INT NOT NULL,
quantidade     INT NOT NULL,
preco_unitario DECIMAL(10,2) NOT NULL,
FOREIGN KEY (id_pedido) REFERENCES pedidos(id_pedido),
FOREIGN KEY (id_produto) REFERENCES produtos(id_produto)
) ENGINE=InnoDB;

START TRANSACTION;

INSERT INTO clientes (id_cliente, nome, cidade) VALUES
(1, 'Ana Souza',    'Campinas'),
(2, 'Bruno Lima',   'São Paulo'),
(3, 'Carla Mendes', 'Santos'),
(4, 'Diego Rocha', 'Campinas'),
(5, 'Elisa Prado', 'Sorocaba'),
(6, 'Felipe Nunes', 'São Paulo');

INSERT INTO categorias (id_categoria, nome) VALUES
(1, 'Informática'), (2, 'Periféricos'),
(3, 'Livros'),      (4, 'Games');

INSERT INTO produtos (id_produto, nome, preco, id_categoria) VALUES
(1, 'Notebook Pro 14',              3200.00, 1),
(2, 'Monitor 24 polegadas',          950.00, 1),
(3, 'SSD 1TB',                       420.00, 1),
(4, 'Roteador Wi-Fi',                260.00, 1),
(5, 'Mouse sem fio',                  89.90, 2),
(6, 'Teclado mecânico',              349.00, 2),
(7, 'Headset USB',                   199.00, 2),
(8, 'Webcam HD',                     179.00, 2),
(9, 'Livro SQL Essencial',            79.90, 3),
(10, 'Livro Lógica de Programação',   64.50, 3),
(11, 'Pendrive 64GB',                 49.90, 2),
(12, 'Hub USB-C',                    139.00, 2);

INSERT INTO pedidos
(id_pedido, data_pedido, status, valor_total, id_cliente) VALUES
(101, '2026-08-03', 'entregue', 259.70, 1),
(102, '2026-08-10', 'entregue', 3200.00, 2),
(103, '2026-08-15', 'enviado', 548.00, 1),
(104, '2026-08-22', 'pendente', 840.00, 3),
(105, '2026-09-01', 'entregue', 1039.90, 4),
(106, '2026-09-05', 'pendente', 149.70, 2),
(107, '2026-09-08', 'entregue', 224.30, 3);

INSERT INTO itens_pedido
(id_pedido, id_produto, quantidade, preco_unitario) VALUES
(101, 5, 2, 89.90), (101, 9, 1, 79.90),
(102, 1, 1, 3200.00),
(103, 6, 1, 349.00), (103, 7, 1, 199.00),
(104, 3, 2, 420.00),
(105, 2, 1, 950.00), (105, 5, 1, 89.90),
(106, 11, 3, 49.90),
(107, 9, 2, 79.90), (107, 10, 1, 64.50);

COMMIT;
