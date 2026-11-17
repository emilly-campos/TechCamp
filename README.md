# TechCamp — sistema integrado

Projeto acadêmico de gestão de produtos. Interface HTML/CSS/JavaScript, Fetch, API Flask, classes Produto e ProdutoDAO e conexão com o MySQL existente `loja_virtual`.

## Comece aqui — Windows / XAMPP

1. Extraia o ZIP e abra a pasta `loja_virtual_completa` no VS Code. O arquivo `app.py` deve estar na pasta aberta.
2. Inicie **MySQL** no XAMPP. O banco `loja_virtual` já deve estar criado com as tabelas do seu SQL anterior. Não reimporte scripts que recriam o banco.
3. Confira `conexao.py`: servidor `127.0.0.1`, porta `3306`, usuário `root`, senha vazia e banco `loja_virtual`. Ajuste para sua instalação, se necessário.
4. Abra **Terminal → Novo Terminal** no VS Code e execute, uma linha por vez:

```powershell
py -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
.\.venv\Scripts\python.exe verificar_conexao.py
.\.venv\Scripts\python.exe app.py
```

Use Python 3.10 ou superior. Não é necessário ativar o ambiente virtual. Caso `py` não seja reconhecido, tente `python` no primeiro comando ou confira a instalação do Python.

5. Acesse **http://127.0.0.1:5000/** no navegador. É a tela da loja, não a lista JSON.
6. Deixe o terminal do Flask aberto. Para encerrar, use Ctrl+C.

**Não abra o HTML com duplo clique nem com Live Server.** O Flask serve o HTML e a API no mesmo endereço, permitindo Fetch com URLs relativas. O Apache não é necessário para a loja; ligue-o apenas para usar o phpMyAdmin.

Em Linux/macOS, substitua os comandos por `python3 -m venv .venv`, `.venv/bin/python -m pip install -r requirements.txt`, `.venv/bin/python verificar_conexao.py` e `.venv/bin/python app.py`.

## Funcionalidades

- Listagem dos produtos reais do banco.
- Cadastro com nome, preço e categoria.
- Consulta dos detalhes ao clicar no nome do produto.
- Edição e exclusão com confirmação.
- Busca por nome ou código, filtro de categoria e ordenação por nome, preço ou ID.
- Contagem de produtos e categorias e indicação da última consulta ao banco.
- Mensagens de sucesso, validação, carregamento, lista vazia e falha de conexão.
- Layout adaptável a desktop e celular. Em telas estreitas, a tabela permite rolagem horizontal.

O escopo é o **CRUD de produtos** solicitado. Não inclui carrinho, pagamentos, login, checkout ou CRUD de clientes/pedidos. As tabelas existentes continuam preservadas.

## Organização

| Arquivo | Função |
| --- | --- |
| `app.py` | Rotas Flask, validações e respostas HTTP. |
| `models.py` | Classe Produto, com atributos e `to_dict()`. |
| `dao.py` | ProdutoDAO e CategoriaDAO, responsáveis pelo SQL. |
| `conexao.py` | Dados de acesso ao MySQL existente. |
| `templates/index.html` | Estrutura da página e formulários. |
| `static/css/style.css` | Cores, componentes e adaptação a telas menores. |
| `static/js/script.js` | Fetch, filtros, eventos e atualização da interface. |
| `verificar_conexao.py` | Teste de conexão real somente de leitura. |
| `tests/test_api.py` | Testes automatizados sem acessar seu banco. |
| `APRESENTACAO.md` | Roteiro da demonstração e explicação do código. |
| `requirements.txt` | Bibliotecas Python necessárias. |

## Rotas e integração

| Método | Rota | Uso na página |
| --- | --- | --- |
| GET | `/` | Entrega o HTML. |
| GET | `/produtos` | Carrega e atualiza o catálogo. |
| POST | `/produtos` | Cadastra produto pelo formulário. |
| GET | `/produtos/<id>` | Busca detalhes e dados atuais para edição. |
| PUT | `/produtos/<id>` | Salva todos os campos da edição. |
| DELETE | `/produtos/<id>` | Exclui após confirmação. |
| GET | `/categorias` | Preenche os seletores com categorias reais. |

POST e PUT recebem JSON com `nome`, `preco` e `id_categoria`. Por exemplo:

```json
{"nome":"Carregador USB-C","preco":"59.90","id_categoria":1}
```

O banco gera `id_produto`. O preço é enviado como texto decimal e tratado com `Decimal` no Python; a resposta também usa texto com duas casas. Na interface, `Intl.NumberFormat` exibe o valor em reais. A categoria deve existir no banco; a chave estrangeira valida essa relação. No SQL original, 1 é Informática, mas a interface consulta os dados atuais e não fixa esse ID.

O formulário tem validação HTML (`required`, `min`, `max`, `step`, `maxlength`). O servidor repete as verificações, pois uma requisição pode ser enviada sem usar a interface.

## Banco preservado e base didática

O código mantém os campos `id_produto`, `nome`, `preco`, `id_categoria` da tabela produtos. A única consulta adicional é a leitura de categorias para preencher os seletores. Não há criação de banco, tabelas, migração, importação automática ou carga inicial de dados.

A separação models/DAO/rotas segue a apostila de POO; os métodos HTTP e o consumo por Fetch seguem o conteúdo de DWS. O conector MySQL substitui o SQLite do exemplo para usar seu banco existente. As particularidades do conector, Flask, Fetch, Decimal, dialogs e tratamento de erros estão comentadas no código.

## Validação e limites

17 testes automatizados passaram com conexões simuladas. Foram conferidos: HTML e assets, CRUD, categorias, dados inválidos, IDs inexistentes, falhas de conexão, erros de FK, parâmetros SQL, confirmação da gravação e fechamento de conexões.

O navegador também foi usado para verificar listagem, cadastro, edição, detalhes, exclusão, busca combinada com categoria e estado sem resultados, com Flask real e DAO de teste em memória. Esse DAO de teste não está incluído no sistema entregue, que usa MySQL.

**A conexão com o MySQL do seu computador não foi executada aqui.** Antes de apresentar, rode `verificar_conexao.py` e siga o roteiro de persistência em APRESENTACAO.md. O projeto está implementado; a comprovação de ponta a ponta com o banco real depende dessa execução local.

Para repetir os testes simulados:

```powershell
.\.venv\Scripts\python.exe -m unittest discover -s tests -v
```

## Solução de problemas

| Sintoma | O que conferir |
| --- | --- |
| `No module named flask` ou `mysql` | Instale requirements com o mesmo Python usado para executar app.py. |
| `Unknown database` | Nome real do banco no phpMyAdmin e `database` em conexao.py. Não recrie o banco. |
| `Access denied` | Usuário e senha do MySQL em conexao.py. |
| Falha ao conectar | MySQL iniciado, host e porta corretos. |
| Tabela ou coluna inexistente | Se o banco corresponde ao SQL que você enviou. |
| Categoria inexistente | Atualize a lista e selecione uma categoria atual. |
| Exclusão bloqueada | O produto já está ligado a itens_pedido. A API retorna 409 para preservar os pedidos. |
| Lista não atualizou após salvar | Clique em Atualizar lista; uma falha de leitura posterior não desfaz uma gravação já confirmada. |
| Endereço ocupado | Feche outro Flask na porta 5000 ou altere a porta no final de app.py e no endereço do navegador. |
| Página sem estilos ou erro de Fetch | Abra pelo endereço do Flask, com a pasta static preservada. |

Servidor local de estudo, sem autenticação, acessível apenas no próprio computador (127.0.0.1). O indicador “Conectado” representa a última leitura bem-sucedida, não um monitoramento contínuo.


## Diagrama de classes UML

Consulte a pasta `uml`: imagem PNG, vetor SVG, fontes PlantUML/Graphviz e explicacao em LEIA_O_DIAGRAMA.md.
