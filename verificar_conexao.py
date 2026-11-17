"""Verifica a conexão real sem inserir, alterar ou excluir dados."""
from mysql.connector import Error
from conexao import conectar

conexao = None
cursor = None
try:
    conexao = conectar()
    cursor = conexao.cursor()
    # Consultas de leitura conferem banco, campos e tabelas usados pela API.
    cursor.execute('SELECT DATABASE()')
    print('Banco conectado:', cursor.fetchone()[0])
    cursor.execute('SELECT id_produto, nome, preco, id_categoria FROM produtos LIMIT 1')
    cursor.fetchall()
    cursor.execute('SELECT id_categoria, nome FROM categorias LIMIT 1')
    cursor.fetchall()
    print('OK: conexão e campos necessários disponíveis.')
except Error as erro:
    print('Falha:', erro)
    print('Confira o MySQL no XAMPP e as configurações em conexao.py.')
    raise SystemExit(1)  # Informa ao terminal que a verificação falhou.
finally:
    if cursor is not None:
        cursor.close()
    if conexao is not None:
        conexao.close()
