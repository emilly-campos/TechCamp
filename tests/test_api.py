"""Testes com banco simulado: não acessam nem alteram seu MySQL.
Execute: python -m unittest discover -s tests -v
"""
import unittest
from decimal import Decimal
from unittest.mock import patch
import app
from models import Produto
from mysql.connector import Error
from dao import ProdutoDAO, CategoriaDAO


class TestAPI(unittest.TestCase):
    def setUp(self):
        # patch troca o DAO por um objeto de teste somente enquanto o teste roda.
        self.troca = patch.object(app, 'dao')
        self.dao = self.troca.start()
        self.addCleanup(self.troca.stop)
        self.cliente = app.app.test_client()
        self.dados = {'nome': 'Fone', 'preco': '59.90', 'id_categoria': 1}
        self.produto = Produto('Fone', Decimal('59.90'), 1, 13)

    def test_pagina_e_arquivos(self):
        for url in ['/', '/static/css/style.css', '/static/js/script.js']:
            resposta = self.cliente.get(url)
            self.assertEqual(resposta.status_code, 200)
            resposta.close()

    def test_cadastro(self):
        self.dao.inserir.return_value = 13
        resposta = self.cliente.post('/produtos', json=self.dados)
        self.assertEqual(resposta.status_code, 201)
        self.assertEqual(resposta.json, self.produto.to_dict())

    def test_listagem_e_detalhe(self):
        self.dao.buscar_todos.return_value = [self.produto]
        self.dao.buscar_por_id.return_value = self.produto
        self.assertEqual(self.cliente.get('/produtos').json, [self.produto.to_dict()])
        self.assertEqual(self.cliente.get('/produtos/13').json, self.produto.to_dict())

    def test_lista_vazia(self):
        self.dao.buscar_todos.return_value = []
        self.assertEqual(self.cliente.get('/produtos').json, [])

    def test_atualizacao_e_exclusao(self):
        self.dao.atualizar.return_value = True
        self.dao.deletar.return_value = True
        self.assertEqual(self.cliente.put('/produtos/13', json=self.dados).status_code, 200)
        self.assertEqual(self.cliente.delete('/produtos/13').status_code, 200)

    def test_inexistentes(self):
        self.dao.buscar_por_id.return_value = None
        self.dao.atualizar.return_value = False
        self.dao.deletar.return_value = False
        self.assertEqual(self.cliente.get('/produtos/99').status_code, 404)
        self.assertEqual(self.cliente.put('/produtos/99', json=self.dados).status_code, 404)
        self.assertEqual(self.cliente.delete('/produtos/99').status_code, 404)

    def test_validacao(self):
        for valor in [None, True, 'NaN', 'Infinity', '-1', '1.234', '100000000', 'abc']:
            dados = dict(self.dados)
            dados['preco'] = valor
            self.assertEqual(self.cliente.post('/produtos', json=dados).status_code, 400)
        for dados in [[], {}, {'nome': ' ', 'preco': '1.00', 'id_categoria': 1}]:
            self.assertEqual(self.cliente.post('/produtos', json=dados).status_code, 400)
        self.assertEqual(self.cliente.post('/produtos', data='{', content_type='application/json').status_code, 400)
        self.dao.inserir.assert_not_called()

    def test_chaves_estrangeiras(self):
        self.dao.inserir.side_effect = Error(errno=1452)
        self.assertEqual(self.cliente.post('/produtos', json=self.dados).status_code, 400)
        self.dao.deletar.side_effect = Error(errno=1451)
        self.assertEqual(self.cliente.delete('/produtos/1').status_code, 409)

    def test_erro_conexao(self):
        self.dao.buscar_todos.side_effect = Error('Banco indisponível', errno=2003)
        resposta = self.cliente.get('/produtos')
        self.assertEqual(resposta.status_code, 500)
        self.assertIn('erro', resposta.json)

    def test_categorias(self):
        with patch.object(app, 'CategoriaDAO') as classe:
            classe.return_value.buscar_todas.return_value = [{'id_categoria': 1, 'nome': 'Informática'}]
            self.assertEqual(self.cliente.get('/categorias').json, [{'id_categoria': 1, 'nome': 'Informática'}])

    def test_erro_http_json(self):
        self.assertTrue(self.cliente.get('/nao-existe').is_json)
        resposta = self.cliente.patch('/produtos')
        self.assertEqual(resposta.status_code, 405)
        self.assertIn('GET', resposta.headers['Allow'])


class TestDAO(unittest.TestCase):
    def setUp(self):
        self.troca = patch('dao.conectar')
        self.conectar = self.troca.start()
        self.addCleanup(self.troca.stop)
        self.conexao = self.conectar.return_value
        self.cursor = self.conexao.cursor.return_value
        self.dao = ProdutoDAO()
        self.produto = Produto("Fone ' USB", Decimal('9.90'), 1)

    def test_parametros_insert(self):
        self.cursor.lastrowid = 15
        self.assertEqual(self.dao.inserir(self.produto), 15)
        sql, parametros = self.cursor.execute.call_args.args
        self.assertNotIn(self.produto.nome, sql)
        self.assertEqual(parametros, (self.produto.nome, self.produto.preco, 1))
        self.conexao.commit.assert_called_once()
        self.conexao.close.assert_called_once()

    def test_leitura(self):
        self.cursor.fetchall.return_value = [(1, 'Fone', Decimal('9.90'), 2)]
        self.assertEqual(self.dao.buscar_todos()[0].nome, 'Fone')
        self.cursor.fetchone.return_value = None
        self.assertIsNone(self.dao.buscar_por_id(99))

    def test_update_igual_e_inexistente(self):
        self.cursor.fetchone.return_value = (1,)
        self.cursor.rowcount = 0
        self.assertTrue(self.dao.atualizar(1, self.produto))
        self.cursor.fetchone.return_value = None
        self.assertFalse(self.dao.atualizar(99, self.produto))

    def test_delete(self):
        self.cursor.rowcount = 1
        self.assertTrue(self.dao.deletar(1))
        self.cursor.rowcount = 0
        self.assertFalse(self.dao.deletar(99))

    def test_falha_fecha_conexao(self):
        self.cursor.execute.side_effect = Error(errno=1451)
        with self.assertRaises(Error):
            self.dao.deletar(1)
        self.conexao.commit.assert_not_called()
        self.cursor.close.assert_called_once()
        self.conexao.close.assert_called_once()

    def test_categoria_dao(self):
        self.cursor.fetchall.return_value = [(1, 'Informática')]
        self.assertEqual(CategoriaDAO().buscar_todas(), [{'id_categoria': 1, 'nome': 'Informática'}])
        self.conexao.close.assert_called_once()


if __name__ == '__main__':
    unittest.main()
