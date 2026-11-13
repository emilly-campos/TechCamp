USE loja_virtual;

-- 1. Produtos com sua categoria (12 linhas). INNER JOIN encontra a categoria pela FK.
SELECT pr.id_produto, pr.nome AS produto, pr.preco, cat.nome AS categoria
FROM produtos AS pr
INNER JOIN categorias AS cat ON cat.id_categoria = pr.id_categoria
ORDER BY pr.id_produto;

-- 2. Pedidos com nome do cliente (7 linhas).
SELECT p.id_pedido, p.data_pedido, c.nome AS cliente, p.status, p.valor_total
FROM pedidos AS p
INNER JOIN clientes AS c ON c.id_cliente = p.id_cliente
ORDER BY p.id_pedido;

-- 3. Pedidos entregues, dos mais recentes aos mais antigos (4 linhas).
SELECT p.id_pedido, c.nome AS cliente, p.data_pedido
FROM pedidos AS p
INNER JOIN clientes AS c ON c.id_cliente = p.id_cliente
WHERE p.status = 'entregue'
ORDER BY p.data_pedido DESC, p.id_pedido DESC;

-- 4. Todos os clientes, mesmo sem pedido (9 linhas). LEFT JOIN preserva os clientes.
SELECT c.nome, p.id_pedido
FROM clientes AS c
LEFT JOIN pedidos AS p ON p.id_cliente = c.id_cliente
ORDER BY c.id_cliente, p.id_pedido;

-- 5. Clientes sem pedido: Elisa e Felipe (2 linhas). IS NULL detecta a falta de par.
SELECT c.nome
FROM clientes AS c
LEFT JOIN pedidos AS p ON p.id_cliente = c.id_cliente
WHERE p.id_pedido IS NULL
ORDER BY c.id_cliente;

-- 6. Detalhes com tres tabelas (11 linhas). O subtotal usa o preco da compra.
SELECT p.id_pedido, pr.nome AS produto, i.quantidade, i.preco_unitario,
       i.quantidade * i.preco_unitario AS subtotal
FROM pedidos AS p
INNER JOIN itens_pedido AS i ON i.id_pedido = p.id_pedido
INNER JOIN produtos AS pr ON pr.id_produto = i.id_produto
ORDER BY p.id_pedido, i.id_item;

-- 7. Quantidade em pedidos por produto (9 linhas); inclui pedidos pendentes.
SELECT pr.id_produto, pr.nome, SUM(i.quantidade) AS quantidade_total
FROM produtos AS pr
INNER JOIN itens_pedido AS i ON i.id_produto = pr.id_produto
GROUP BY pr.id_produto, pr.nome
ORDER BY pr.id_produto;

-- 8. Precos acima da media: subconsulta retorna um unico valor (2 linhas).
SELECT nome, preco
FROM produtos
WHERE preco > (SELECT AVG(preco) FROM produtos)
ORDER BY preco DESC, id_produto;

-- 9. Clientes com pedidos usando IN: testa participacao na lista (4 linhas).
SELECT id_cliente, nome
FROM clientes
WHERE id_cliente IN (SELECT id_cliente FROM pedidos)
ORDER BY id_cliente;

-- 10. Clientes com pedidos usando EXISTS: testa existencia de um pedido (4 linhas).
SELECT c.id_cliente, c.nome
FROM clientes AS c
WHERE EXISTS (SELECT 1 FROM pedidos AS p WHERE p.id_cliente = c.id_cliente)
ORDER BY c.id_cliente;

-- 11. Pagina 3, cinco produtos por pagina: OFFSET = (3 - 1) * 5 = 10 (2 linhas).
SELECT id_produto, nome, preco
FROM produtos
ORDER BY nome, id_produto
LIMIT 5 OFFSET 10;

-- 12. Ate dez pedidos recentes com cliente (7 linhas). ID desempata datas iguais.
SELECT p.id_pedido, c.nome AS cliente, p.data_pedido, p.valor_total
FROM pedidos AS p
INNER JOIN clientes AS c ON c.id_cliente = p.id_cliente
ORDER BY p.data_pedido DESC, p.id_pedido DESC
LIMIT 10;

-- 13. Conferencia dos totais: deve retornar ZERO linhas.
SELECT p.id_pedido, p.valor_total,
       COALESCE(SUM(i.quantidade * i.preco_unitario), 0) AS total_calculado
FROM pedidos AS p
LEFT JOIN itens_pedido AS i ON i.id_pedido = p.id_pedido
GROUP BY p.id_pedido, p.valor_total
HAVING p.valor_total <> ROUND(COALESCE(SUM(i.quantidade * i.preco_unitario), 0), 2);
