class Produto:
    def __init__(self, nome, preco, id_categoria, id_produto=None):
        # None indica que o banco ainda não gerou o ID do novo produto.
        self.id_produto = id_produto
        self.nome = nome
        self.preco = preco
        self.id_categoria = id_categoria

    def to_dict(self):
        # O Flask transforma este dicionário em JSON na resposta da API.
        return {
            "id_produto": self.id_produto,
            "nome": self.nome,
            # Texto com duas casas preserva os centavos do DECIMAL no JSON.
            "preco": format(self.preco, ".2f"),
            "id_categoria": self.id_categoria
        }
