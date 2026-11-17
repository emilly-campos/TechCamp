# TechCamp — Diagrama de Classes UML

Diagrama revisado com base em models.py e dao.py do projeto TechCamp.

## Arquivos

- TechCamp_Classes.png: imagem pronta para inserir em um trabalho ou apresentação.
- TechCamp_Classes.svg: versão vetorial para ampliar sem perder nitidez.
- TechCamp_Classes.puml: código editável em PlantUML.
- TechCamp_Classes.dot: fonte da imagem, renderizável com Graphviz.

## Classes e responsabilidades

| Classe | Arquivo | Responsabilidade |
| --- | --- | --- |
| Produto | models.py | Representa os dados de um produto e os converte em dicionário. |
| ProdutoDAO | dao.py | Insere, consulta, atualiza e exclui produtos no banco. |
| CategoriaDAO | dao.py | Consulta as categorias já existentes e retorna dicionários. |

ProdutoDAO depende de Produto porque recebe objetos Produto para gravar e cria objetos Produto ao consultar. Não há herança, composição ou agregação declaradas entre essas classes. Não há multiplicidade na seta de dependência.

O símbolo + representa visibilidade pública, compatível com os nomes dos atributos e métodos atuais. Os DAOs não armazenam atributos de instância; suas conexões e cursores são variáveis locais dos métodos. Por isso não são mostrados como atributos.

Os tipos apresentados são inferidos do uso no sistema, para facilitar a leitura. Eles não são anotações de tipo adicionadas ao código Python. O parâmetro id_produto do construtor pode ser None até o banco gerar o ID. O parâmetro self foi omitido como é usual na apresentação das operações UML.

## Retornos dos métodos

- Produto.to_dict(): dicionário com id_produto, nome, preco e id_categoria; preco é texto com duas casas decimais.
- ProdutoDAO.inserir(): ID inteiro gerado pelo banco.
- ProdutoDAO.buscar_todos(): lista de objetos Produto, podendo ser vazia.
- ProdutoDAO.buscar_por_id(): objeto Produto, ou None se o ID não existir.
- ProdutoDAO.atualizar(): True se o produto existir e a operação terminar; False se não existir. Dados iguais aos atuais também retornam True.
- ProdutoDAO.deletar(): True se uma linha for excluída; False se nenhuma linha for excluída.
- CategoriaDAO.buscar_todas(): lista de dicionários com id_categoria e nome.

Erros de acesso ao banco podem interromper os métodos DAO e são tratados nas rotas Flask.

## O que não é uma classe neste projeto

app.py é um módulo com funções de rotas Flask. conexao.py é um módulo com a função conectar(). Não existe uma classe própria chamada App, Controller, Conexao ou Categoria. O diagrama não inventa essas classes.

As tabelas clientes, categorias, produtos, pedidos e itens_pedido pertencem à modelagem do banco. Elas não se tornam automaticamente classes Python. Este é o diagrama de classes implementadas do CRUD de produtos; não é um diagrama entidade-relacionamento de todas as tabelas.

## Para explicar na apresentação

“Produto representa os dados. ProdutoDAO cuida das operações SQL e utiliza objetos Produto. CategoriaDAO consulta as categorias disponíveis. As rotas Flask chamam os DAOs, e a página consome essas rotas por Fetch. A separação mantém cada parte com uma responsabilidade.”

A inclusão do diagrama documenta as classes existentes. A validação com o MySQL real continua dependendo do teste local descrito no README e em APRESENTACAO.md.
