// O estado da tela fica em variáveis simples; o banco continua sendo a fonte dos dados.
let produtos = [];
let categorias = [];
let idEdicao = null;
let produtoDetalhado = null;
let ocupado = false;
let carregando = false;
let dadosDisponiveis = false;
const editor = document.getElementById('editor');
const detalhes = document.getElementById('detalhes');
const formulario = document.getElementById('form-produto');
const moeda = new Intl.NumberFormat('pt-BR', {style: 'currency', currency: 'BRL'});

function avisar(texto, erro = false) {
    const mensagem = document.getElementById('mensagem');
    mensagem.textContent = texto; // textContent não interpreta nomes do banco como HTML.
    mensagem.className = erro ? 'message error' : 'message';
    mensagem.hidden = false;
}

async function requisicao(url, opcoes = {}) {
    // Fetch envia uma requisição para o Flask. await espera a resposta.
    let resposta;
    try {
        resposta = await fetch(url, opcoes);
    } catch (erro) {
        throw new Error('Não foi possível acessar o servidor. Confira se o Flask está aberto.');
    }
    const dados = await resposta.json(); // Converte o JSON recebido em objetos JavaScript.
    // Fetch não lança erro sozinho para status 400, 404, 409 ou 500.
    if (!resposta.ok) {
        throw new Error(dados.erro || 'Não foi possível concluir a operação.');
    }
    return dados;
}

function nomeCategoria(id) {
    const categoria = categorias.find(item => item.id_categoria === id);
    return categoria ? categoria.nome : 'Categoria #' + id;
}

function mostrarEstado(titulo, texto) {
    const estado = document.getElementById('estado');
    estado.querySelector('h3').textContent = titulo;
    estado.querySelector('p').textContent = texto;
    estado.hidden = false;
}

function preencherCategorias() {
    const filtro = document.getElementById('filtro-categoria');
    const selecao = document.getElementById('categoria');
    const filtroAnterior = filtro.value;
    filtro.replaceChildren(new Option('Todas as categorias', ''));
    selecao.replaceChildren(new Option('Selecione', ''));
    for (const categoria of categorias) {
        // Option cria as opções sem inserir HTML com dados do banco.
        filtro.add(new Option(categoria.nome, categoria.id_categoria));
        selecao.add(new Option(categoria.nome, categoria.id_categoria));
    }
    if (categorias.some(item => String(item.id_categoria) === filtroAnterior)) {
        filtro.value = filtroAnterior;
    }
}

function renderizar() {
    if (carregando || !dadosDisponiveis) return;
    const busca = document.getElementById('busca').value.toLocaleLowerCase('pt-BR').trim();
    const categoria = document.getElementById('filtro-categoria').value;
    // O filtro altera apenas a exibição; não exclui registros do banco.
    let lista = produtos.filter(produto =>
        (produto.nome.toLocaleLowerCase('pt-BR').includes(busca) || String(produto.id_produto).includes(busca)) &&
        (!categoria || String(produto.id_categoria) === categoria)
    );
    const ordem = document.getElementById('ordenacao').value;
    if (ordem === 'nome') lista.sort((a, b) => a.nome.localeCompare(b.nome, 'pt-BR'));
    else if (ordem === 'preco') lista.sort((a, b) => Number(a.preco) - Number(b.preco));
    else lista.sort((a, b) => b.id_produto - a.id_produto);

    const corpo = document.getElementById('produtos');
    corpo.replaceChildren();
    for (const produto of lista) {
        // Clona a estrutura da linha e preenche seus campos com segurança.
        const linha = document.getElementById('linha-produto').content.cloneNode(true);
        linha.querySelector('.product-icon').textContent = produto.nome.charAt(0).toUpperCase();
        linha.querySelector('.product-name').textContent = produto.nome;
        linha.querySelector('.product-name').addEventListener('click', () => verDetalhes(produto.id_produto));
        linha.querySelector('.product-code').textContent = '#' + String(produto.id_produto).padStart(4, '0');
        linha.querySelector('.badge').textContent = nomeCategoria(produto.id_categoria);
        // Number é usado só na exibição; o preço enviado à API permanece texto decimal.
        linha.querySelector('.price').textContent = moeda.format(Number(produto.preco));
        const editar = linha.querySelector('.edit-button');
        editar.setAttribute('aria-label', 'Editar ' + produto.nome);
        editar.addEventListener('click', () => editarProduto(produto.id_produto));
        const excluir = linha.querySelector('.delete-button');
        excluir.setAttribute('aria-label', 'Excluir ' + produto.nome);
        excluir.addEventListener('click', () => excluirProduto(produto));
        corpo.appendChild(linha);
    }
    document.getElementById('contagem').textContent = produtos.length;
    document.getElementById('resultado').textContent = lista.length + ' de ' + produtos.length + ' produtos';
    document.getElementById('estado').hidden = lista.length > 0;
    if (!lista.length) {
        mostrarEstado(produtos.length ? 'Nenhum resultado encontrado' : 'Seu catálogo começa aqui',
            produtos.length ? 'Experimente outro nome ou selecione todas as categorias.' : 'Clique em Novo produto para cadastrar o primeiro item.');
    }
}

async function carregar() {
    if (carregando) return false;
    carregando = true;
    document.getElementById('recarregar').disabled = true;
    document.getElementById('novo').disabled = true;
    document.getElementById('produtos').replaceChildren();
    document.getElementById('mensagem').hidden = true;
    mostrarEstado('Carregando seu catálogo…', 'Consultando os produtos e as categorias da loja.');
    try {
        // As duas consultas GET são independentes e podem acontecer juntas.
        const respostas = await Promise.all([requisicao('/produtos'), requisicao('/categorias')]);
        dadosDisponiveis = true;
        produtos = respostas[0];
        categorias = respostas[1];
        preencherCategorias();
        document.getElementById('total').textContent = produtos.length;
        document.getElementById('total-categorias').textContent = categorias.length;
        document.getElementById('conexao').textContent = 'Conectado';
        document.getElementById('conexao-detalhe').textContent = 'Catálogo sincronizado com o banco';
        document.getElementById('status-dot').classList.add('online');
        document.getElementById('novo').disabled = categorias.length === 0;
        if (!categorias.length) avisar('Nenhuma categoria cadastrada. Cadastre uma categoria no seu banco antes de adicionar produtos.', true);
        carregando = false;
        renderizar();
        return true;
    } catch (erro) {
        dadosDisponiveis = false;
        produtos = [];
        document.getElementById('total').textContent = '—';
        document.getElementById('total-categorias').textContent = '—';
        document.getElementById('contagem').textContent = '—';
        document.getElementById('resultado').textContent = 'Dados indisponíveis';
        document.getElementById('conexao').textContent = 'Sem conexão';
        document.getElementById('conexao-detalhe').textContent = 'Confira o servidor e tente novamente';
        document.getElementById('status-dot').classList.remove('online');
        mostrarEstado('Não foi possível carregar o catálogo', 'Confira o MySQL no XAMPP e as configurações em conexao.py. Depois, clique em Atualizar lista.');
        avisar(erro.message, true);
        return false;
    } finally {
        carregando = false;
        document.getElementById('recarregar').disabled = false;
    }
}

function abrirEditor(produto = null) {
    idEdicao = produto ? produto.id_produto : null;
    formulario.reset();
    document.getElementById('erro-form').hidden = true;
    document.getElementById('titulo-editor').textContent = produto ? 'Editar produto' : 'Novo produto';
    if (produto) {
        document.getElementById('nome').value = produto.nome;
        document.getElementById('preco').value = produto.preco;
        document.getElementById('categoria').value = produto.id_categoria;
    }
    editor.showModal();
    document.getElementById('nome').focus();
}

async function editarProduto(id) {
    if (ocupado) return;
    ocupado = true;
    try {
        // Consulta o produto por ID antes da edição, evitando usar dados antigos da tela.
        const produto = await requisicao('/produtos/' + id);
        abrirEditor(produto);
    } catch (erro) { avisar(erro.message, true); }
    finally { ocupado = false; }
}

async function verDetalhes(id) {
    if (ocupado) return;
    ocupado = true;
    try {
        produtoDetalhado = await requisicao('/produtos/' + id);
        document.getElementById('titulo-detalhes').textContent = produtoDetalhado.nome;
        const lista = document.getElementById('dados-detalhes');
        lista.replaceChildren();
        const campos = [['Código', '#' + produtoDetalhado.id_produto], ['Categoria', nomeCategoria(produtoDetalhado.id_categoria)], ['Preço', moeda.format(Number(produtoDetalhado.preco))]];
        for (const campo of campos) {
            const termo = document.createElement('dt');
            const valor = document.createElement('dd');
            termo.textContent = campo[0];
            valor.textContent = campo[1];
            lista.append(termo, valor);
        }
        detalhes.showModal();
    } catch (erro) { avisar(erro.message, true); }
    finally { ocupado = false; }
}

formulario.addEventListener('submit', async function(evento) {
    evento.preventDefault(); // Evita o envio tradicional do formulário e o recarregamento da página.
    if (ocupado) return;
    const dados = {
        nome: document.getElementById('nome').value.trim(),
        preco: document.getElementById('preco').value,
        id_categoria: Number(document.getElementById('categoria').value)
    };
    if (!dados.nome) {
        document.getElementById('erro-form').textContent = 'Informe o nome do produto.';
        document.getElementById('erro-form').hidden = false;
        return;
    }
    ocupado = true;
    const botao = document.getElementById('salvar');
    botao.disabled = true;
    botao.textContent = 'Salvando…';
    document.getElementById('erro-form').hidden = true;
    try {
        await requisicao(idEdicao === null ? '/produtos' : '/produtos/' + idEdicao, {
            method: idEdicao === null ? 'POST' : 'PUT',
            headers: {'Content-Type': 'application/json'},
            body: JSON.stringify(dados) // Transforma o objeto em texto JSON para o Flask.
        });
        editor.close();
        const atualizou = await carregar();
        avisar(atualizou ? 'Produto salvo com sucesso.' : 'Produto salvo, mas a lista não pôde ser atualizada. Clique em Atualizar lista.', !atualizou);
    } catch (erro) {
        document.getElementById('erro-form').textContent = erro.message;
        document.getElementById('erro-form').hidden = false;
    } finally {
        ocupado = false;
        botao.disabled = false;
        botao.textContent = 'Salvar produto';
    }
});

async function excluirProduto(produto) {
    if (ocupado) return;
    // A confirmação evita exclusões por um clique acidental.
    if (!window.confirm('Excluir "' + produto.nome + '"? Esta ação não pode ser desfeita.')) return;
    ocupado = true;
    try {
        await requisicao('/produtos/' + produto.id_produto, {method: 'DELETE'});
        const atualizou = await carregar();
        avisar(atualizou ? 'Produto excluído com sucesso.' : 'Produto excluído, mas a lista não pôde ser atualizada. Clique em Atualizar lista.', !atualizou);
    } catch (erro) { avisar(erro.message, true); }
    finally { ocupado = false; }
}

// Os eventos ligam os controles da página às funções acima.
document.getElementById('novo').addEventListener('click', () => { if (!ocupado) abrirEditor(); });
document.getElementById('recarregar').addEventListener('click', () => { if (!ocupado) carregar(); });
document.getElementById('busca').addEventListener('input', renderizar);
document.getElementById('filtro-categoria').addEventListener('change', renderizar);
document.getElementById('ordenacao').addEventListener('change', renderizar);
for (const id of ['cancelar', 'fechar-editor']) {
    document.getElementById(id).addEventListener('click', () => { if (!ocupado) editor.close(); });
}
editor.addEventListener('cancel', evento => { if (ocupado) evento.preventDefault(); });
document.getElementById('fechar-detalhes').addEventListener('click', () => detalhes.close());
document.getElementById('editar-detalhes').addEventListener('click', () => {
    detalhes.close();
    editarProduto(produtoDetalhado.id_produto);
});
carregar();
