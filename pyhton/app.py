# Decimal evita trabalhar com aproximações binárias nos valores de dinheiro.
from decimal import Decimal, InvalidOperation
from flask import Flask, jsonify, request
from mysql.connector import Error
from werkzeug.exceptions import HTTPException
from dao import ProdutoDAO
from models import Produto

app = Flask(__name__)  # Cria a aplicação que recebe as requisições HTTP.
dao = ProdutoDAO()  # Somente o DAO executa as operações com produtos no banco.


def ler_produto():
    # silent=True permite devolver nossa mensagem JSON se o corpo estiver inválido.
    dados = request.get_json(silent=True)
    if not isinstance(dados, dict):
        raise ValueError("Envie um objeto JSON com nome, preco e id_categoria.")

    nome = dados.get("nome")  # get retorna None quando a chave está ausente.
    if not isinstance(nome, str) or not nome.strip() or len(nome.strip()) > 100:
        raise ValueError("O nome deve conter de 1 a 100 caracteres.")

    valor = dados.get("preco")
    # bool é tratado como inteiro pelo Python, mas não representa um preço aqui.
    if isinstance(valor, bool) or not isinstance(valor, (str, int, float)):
        raise ValueError("Informe um preco numérico, usando ponto para os centavos.")
    try:
        preco = Decimal(str(valor))
    except InvalidOperation:
        raise ValueError("Preco inválido. Exemplo: 59.90.")
    # DECIMAL(10,2) comporta oito dígitos inteiros e duas casas decimais.
    if not preco.is_finite() or preco < 0 or preco > Decimal("99999999.99"):
        raise ValueError("O preco deve estar entre 0 e 99999999.99.")
    if preco != preco.quantize(Decimal("0.01")):
        raise ValueError("O preco deve ter no máximo duas casas decimais.")

    categoria = dados.get("id_categoria")
    # Exige número inteiro no JSON; a existência da categoria é conferida pela FK.
    if type(categoria) is not int or not 1 <= categoria <= 2147483647:
        raise ValueError("id_categoria deve ser um inteiro positivo válido.")
    return Produto(nome.strip(), preco, categoria)


# Cada decorador associa um endereço e um método HTTP à função abaixo dele.
@app.route("/produtos", methods=["POST"])
def cadastrar_produto():
    produto = ler_produto()
    produto.id_produto = dao.inserir(produto)
    return jsonify(produto.to_dict()), 201  # 201 significa registro criado.


@app.route("/produtos", methods=["GET"])
def listar_produtos():
    lista = []
    for produto in dao.buscar_todos():
        lista.append(produto.to_dict())
    return jsonify(lista)  # Uma lista vazia vira [] no JSON; status padrão: 200.


# <int:id_produto> converte o trecho numérico da URL para um inteiro Python.
@app.route("/produtos/<int:id_produto>", methods=["GET"])
def buscar_produto(id_produto):
    produto = dao.buscar_por_id(id_produto)
    if produto is None:
        return jsonify({"erro": "Produto não encontrado."}), 404
    return jsonify(produto.to_dict())


@app.route("/produtos/<int:id_produto>", methods=["PUT"])
def atualizar_produto(id_produto):
    produto = ler_produto()  # PUT exige os três campos, assim como POST.
    if not dao.atualizar(id_produto, produto):
        return jsonify({"erro": "Produto não encontrado."}), 404
    produto.id_produto = id_produto
    return jsonify(produto.to_dict())


@app.route("/produtos/<int:id_produto>", methods=["DELETE"])
def deletar_produto(id_produto):
    if not dao.deletar(id_produto):
        return jsonify({"erro": "Produto não encontrado."}), 404
    return jsonify({"mensagem": "Produto excluído com sucesso."})


# Os tratadores evitam repetir o mesmo try/except em todas as rotas.
@app.errorhandler(ValueError)
def tratar_validacao(erro):
    return jsonify({"erro": str(erro)}), 400  # Dados enviados incorretamente.


@app.errorhandler(Error)
def tratar_banco(erro):
    # Códigos do MySQL para violações das chaves estrangeiras já existentes.
    if erro.errno == 1452:
        return jsonify({"erro": "A categoria informada não existe."}), 400
    if erro.errno == 1451:
        return jsonify({"erro": "Este produto está ligado a pedidos e não pode ser excluído."}), 409
    # O detalhe técnico fica no terminal; a resposta traz uma orientação simples.
    app.logger.error("Falha no banco: %s", erro)
    return jsonify({"erro": "Falha no banco. Confira o MySQL e o arquivo conexao.py."}), 500


@app.errorhandler(HTTPException)
def tratar_http(erro):
    # Mantém erros de rota/método em JSON, preservando cabeçalhos HTTP como Allow.
    resposta = erro.get_response()
    resposta.data = app.json.dumps({"erro": erro.description})
    resposta.content_type = "application/json"
    return resposta


if __name__ == "__main__":
    # Inicia somente ao executar este arquivo; disponível apenas neste computador.
    app.run(host="127.0.0.1", port=5000, debug=False)
