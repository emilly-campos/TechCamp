# Roteiro de apresentação — TechCamp

## Antes de apresentar

- Inicie o MySQL no XAMPP.
- Rode `verificar_conexao.py`; ele deve informar conexão e campos disponíveis.
- Inicie `app.py` e abra http://127.0.0.1:5000/.
- Confira se a página mostra o catálogo do seu banco e a indicação “Conectado”.
- Separe esta pasta no VS Code e o phpMyAdmin para mostrar a persistência.

## Demonstração de 5 a 7 minutos

1. **Objetivo (30 s):** “Este sistema gerencia o catálogo de produtos de uma loja de informática. O usuário faz as operações pela página e o Flask se comunica com o MySQL.”
2. **Listagem (30 s):** mostre os produtos. Pesquise “Mouse”, selecione uma categoria e depois limpe os filtros. Explique que os filtros organizam os dados já recebidos.
3. **Cadastro (1 min):** clique em Novo produto, cadastre “Carregador USB-C apresentação”, preço 59,90 e uma categoria existente. Mostre a mensagem e o novo código gerado pelo banco.
4. **Detalhes e edição (1 min):** clique no nome para ver os detalhes. Edite o preço para 69,90 e salve. O formulário usa GET por ID e PUT para atualizar.
5. **Persistência real (1 min):** recarregue o navegador e confirme o produto. No phpMyAdmin, abra a tabela produtos e localize o código. Para uma prova adicional, pare e reinicie o Flask: o produto deve continuar disponível porque está no banco.
6. **Exclusão (30 s):** exclua somente o produto que acabou de cadastrar e confirme. Recarregue e confira que ele saiu do banco. Não use produtos antigos vinculados a pedidos: a FK impede sua exclusão.
7. **Código (1 a 2 min):** mostre Produto em models.py, um método do ProdutoDAO, a rota correspondente e a chamada Fetch em script.js.

## Como explicar o caminho dos dados

Ao clicar em Salvar, o JavaScript impede o envio tradicional do formulário com `preventDefault()`. Ele reúne os campos, usa `JSON.stringify()` e faz um Fetch com POST ou PUT. A rota Flask lê e valida o JSON, cria um objeto Produto e chama o DAO. O DAO executa SQL com parâmetros e confirma a transação com `commit()`. A rota devolve JSON; o JavaScript consulta a lista novamente e atualiza a tabela sem recarregar a página toda.

## Perguntas que podem aparecer

| Pergunta | Resposta simples |
| --- | --- |
| Onde está a POO? | Produto representa o dado; ProdutoDAO encapsula o acesso ao banco. |
| Por que separar DAO e model? | O objeto Produto não precisa saber executar SQL. Cada classe tem uma responsabilidade. |
| O que faz Fetch? | Envia uma requisição HTTP do navegador para o Flask e recebe uma resposta. |
| O que é JSON? | Um formato de texto usado para trocar os dados entre JavaScript e Python. |
| O que faz await? | Espera uma operação assíncrona terminar antes de continuar aquela função. |
| Por que testar response.ok? | Fetch pode receber um erro HTTP sem lançar uma exceção automaticamente. |
| Por que não colocar os valores direto no SQL? | Os parâmetros fazem o conector tratar a entrada como dado, protegendo a consulta. |
| Por que não guardar tudo no JavaScript? | Variáveis da página desaparecem; o banco mantém os registros entre execuções. |
| Por que validar no servidor? | Alguém pode chamar a API diretamente, sem passar pelo formulário. |
| Por que uma exclusão pode falhar? | A FK de itens_pedido protege um produto já usado em pedidos. |
| Precisa de CORS? | Nesta estrutura, não: página e API são servidas pelo mesmo Flask. |
| O preço é float? | No Python usamos Decimal; na resposta ele é texto com duas casas. |

## Checklist de integração no seu computador

- [ ] Verificação de conexão passa.
- [ ] Produtos e categorias reais aparecem.
- [ ] Cadastro aparece na tabela produtos no phpMyAdmin.
- [ ] Edição permanece depois de recarregar e reiniciar o Flask.
- [ ] Exclusão remove o produto de teste no banco.
- [ ] Busca e filtro funcionam.
- [ ] Erros são exibidos sem apagar os dados do formulário.
- [ ] Você consegue explicar models.py, dao.py, app.py e script.js.

Os testes simulados incluídos não substituem este checklist com o MySQL real.
