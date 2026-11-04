// ====== CONFIGURAÇÃO ======
// Endereço do seu back-end Python (FastAPI roda em 8000 por padrão).
const API_URL = "http://localhost:8000";
const LIMITE_ESTOQUE_BAIXO = 5;

let produtos = [];
let editandoId = null;
const $ = (id) => document.getElementById(id);
const brl = (v) => Number(v).toLocaleString("pt-BR", { style: "currency", currency: "BRL" });

async function api(caminho, opcoes = {}) {
  const resp = await fetch(API_URL + caminho, {
    headers: { "Content-Type": "application/json" },
    ...opcoes,
  });
  if (resp.status === 204) return null;
  let dados = null;
  try { dados = await resp.json(); } catch (_) {}
  if (!resp.ok) {
    let msg = "Erro " + resp.status;
    if (dados && typeof dados.detail === "string") msg = dados.detail;
    else if (dados && Array.isArray(dados.detail)) msg = dados.detail.map(d => (d.loc || []).slice(-1) + ": " + d.msg).join("; ");
    throw new Error(msg);
  }
  return dados;
}

function avisar(texto) {
  const b = $("banner");
  b.textContent = texto || "";
  b.classList.toggle("show", !!texto);
}

async function carregar() {
  try {
    produtos = await api("/produtos");
    avisar("");
  } catch (e) {
    produtos = [];
    avisar(e instanceof TypeError
      ? "Não consegui falar com o servidor em " + API_URL + ". Ele está rodando? O CORS está habilitado?"
      : e.message);
  }
  desenhar();
}

function situacao(q) {
  if (q === 0) return ["out", "Sem estoque"];
  if (q <= LIMITE_ESTOQUE_BAIXO) return ["low", "Estoque baixo"];
  return ["ok", "Em estoque"];
}

function celula(tr, texto, classe) {
  const td = document.createElement("td");
  td.textContent = texto;
  if (classe) td.className = classe;
  tr.appendChild(td);
  return td;
}

function desenhar() {
  const termo = $("busca").value.trim().toLowerCase();
  const filtrados = produtos.filter(p =>
    [p.nome, p.sku, p.categoria].some(c => String(c).toLowerCase().includes(termo)));
  const tbody = $("lista");
  tbody.replaceChildren();

  filtrados.forEach(p => {
    const tr = document.createElement("tr");
    celula(tr, p.nome);
    celula(tr, p.sku);
    celula(tr, p.categoria);
    celula(tr, p.quantidade, "num");
    celula(tr, brl(p.preco), "num");
    const [cls, rotulo] = situacao(p.quantidade);
    const tdS = document.createElement("td");
    const badge = document.createElement("span");
    badge.className = "badge " + cls; badge.textContent = rotulo;
    tdS.appendChild(badge); tr.appendChild(tdS);

    const tdA = document.createElement("td");
    tdA.style.whiteSpace = "nowrap";
    const bEd = document.createElement("button");
    bEd.className = "link"; bEd.textContent = "Editar";
    bEd.onclick = () => abrirForm(p);
    const bEx = document.createElement("button");
    bEx.className = "link danger"; bEx.textContent = "Excluir";
    bEx.onclick = () => excluir(p);
    tdA.append(bEd, bEx); tr.appendChild(tdA);
    tbody.appendChild(tr);
  });

  $("vazio").hidden = filtrados.length > 0;
  $("vazio").textContent = produtos.length
    ? "Nenhum produto encontrado para esse filtro."
    : "Nenhum produto cadastrado. Clique em “Novo produto” para começar.";
  $("sProdutos").textContent = produtos.length;
  $("sUnidades").textContent = produtos.reduce((s, p) => s + p.quantidade, 0);
  $("sValor").textContent = brl(produtos.reduce((s, p) => s + p.quantidade * p.preco, 0));
}

function abrirForm(p) {
  editandoId = p ? p.id : null;
  $("dlgTitulo").textContent = p ? "Editar produto" : "Novo produto";
  $("formError").textContent = "";
  const f = $("form");
  ["nome", "sku", "categoria", "quantidade", "preco"].forEach(c => f.elements[c].value = p ? p[c] : "");
  $("dlg").showModal();
}

$("form").addEventListener("submit", async (ev) => {
  ev.preventDefault();
  const f = ev.target.elements;
  const corpo = {
    nome: f.nome.value.trim(),
    sku: f.sku.value.trim(),
    categoria: f.categoria.value.trim(),
    quantidade: parseInt(f.quantidade.value, 10),
    preco: parseFloat(f.preco.value),
  };
  try {
    if (editandoId === null) await api("/produtos", { method: "POST", body: JSON.stringify(corpo) });
    else await api("/produtos/" + editandoId, { method: "PUT", body: JSON.stringify(corpo) });
    $("dlg").close();
    await carregar();
  } catch (e) {
    $("formError").textContent = e instanceof TypeError ? "Servidor fora do ar." : e.message;
  }
});

async function excluir(p) {
  if (!confirm("Excluir “" + p.nome + "”? Essa ação não pode ser desfeita.")) return;
  try { await api("/produtos/" + p.id, { method: "DELETE" }); await carregar(); }
  catch (e) { avisar(e.message); }
}

$("btnNovo").onclick = () => abrirForm(null);
$("btnCancelar").onclick = () => $("dlg").close();
$("busca").addEventListener("input", desenhar);
carregar();
