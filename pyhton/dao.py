from pyhton.conexao import conectar
from models import Produto


class ProdutoDAO:
    def inserir(self, produto):
        # Uma conexão por operação evita compartilhar a conexão entre requisições.
        conexao = conectar()
        cursor = None
        try:
            cursor = conexao.cursor()  # O cursor executa comandos SQL.
            # %s substitui o ? do SQLite. Os valores são enviados separadamente
            # para que o conector os trate como dados, não como código SQL.
            cursor.execute(
                "INSERT INTO produtos (nome, preco, id_categoria) VALUES (%s, %s, %s)",
                (produto.nome, produto.preco, produto.id_categoria)
            )
            conexao.commit()  # Confirma a gravação no banco.
            return cursor.lastrowid  # ID criado pelo AUTO_INCREMENT existente.
        finally:
            # finally executa mesmo quando o SQL falha.
            # Fechar sem commit descarta alterações pendentes no InnoDB.
            if cursor is not None:
                cursor.close()
            conexao.close()

    def buscar_todos(self):
        conexao = conectar()
        cursor = None
        try:
            cursor = conexao.cursor()
            cursor.execute(
                "SELECT id_produto, nome, preco, id_categoria FROM produtos ORDER BY id_produto"
            )
            linhas = cursor.fetchall()  # Lê todas as linhas da consulta.
            produtos = []
            for linha in linhas:
                # As posições seguem a ordem das colunas do SELECT.
                produto = Produto(linha[1], linha[2], linha[3], linha[0])
                produtos.append(produto)
            return produtos
        finally:
            if cursor is not None:
                cursor.close()
            conexao.close()

    def buscar_por_id(self, id_produto):
        conexao = conectar()
        cursor = None
        try:
            cursor = conexao.cursor()
            cursor.execute(
                "SELECT id_produto, nome, preco, id_categoria FROM produtos WHERE id_produto = %s",
                (id_produto,)  # A vírgula forma uma tupla com um único valor.
            )
            linha = cursor.fetchone()  # Retorna uma linha, ou None se não existir.
            if linha is None:
                return None
            return Produto(linha[1], linha[2], linha[3], linha[0])
        finally:
            if cursor is not None:
                cursor.close()
            conexao.close()

    def atualizar(self, id_produto, produto):
        conexao = conectar()
        cursor = None
        try:
            cursor = conexao.cursor()
            # Confere e bloqueia esta linha até o commit/fechamento da conexão.
            # Assim, dados iguais aos atuais também contam como atualização válida.
            cursor.execute("SELECT id_produto FROM produtos WHERE id_produto = %s FOR UPDATE", (id_produto,))
            if cursor.fetchone() is None:
                return False
            cursor.execute(
                "UPDATE produtos SET nome = %s, preco = %s, id_categoria = %s WHERE id_produto = %s",
                (produto.nome, produto.preco, produto.id_categoria, id_produto)
            )
            conexao.commit()
            return True
        finally:
            if cursor is not None:
                cursor.close()
            conexao.close()

    def deletar(self, id_produto):
        conexao = conectar()
        cursor = None
        try:
            cursor = conexao.cursor()
            cursor.execute("DELETE FROM produtos WHERE id_produto = %s", (id_produto,))
            apagou = cursor.rowcount > 0  # Informa se alguma linha foi excluída.
            conexao.commit()
            return apagou
        finally:
            if cursor is not None:
                cursor.close()
            conexao.close()
