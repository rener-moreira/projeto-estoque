// ====== CONFIGURAÇÃO ======
const API_URL = "http://localhost:8000";
const $ = (id) => document.getElementById(id);

// Já está logado? Vai direto para o estoque.
if (localStorage.getItem("token")) location.href = "index.html";

function mostrar(texto, tipo) {
  const m = $("msg");
  m.textContent = texto || "";
  m.className = texto ? tipo : "";
}

function aba(entrar) {
  $("formLogin").hidden = !entrar;
  $("formCadastro").hidden = entrar;
  $("tabEntrar").setAttribute("aria-selected", entrar);
  $("tabCriar").setAttribute("aria-selected", !entrar);
  mostrar("");
}

async function enviar(caminho, corpo) {
  let resp;
  try {
    resp = await fetch(API_URL + caminho, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(corpo),
    });
  } catch (_) {
    throw new Error("Não consegui falar com o servidor. Ele está rodando?");
  }
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

$("formLogin").addEventListener("submit", async (ev) => {
  ev.preventDefault();
  const f = ev.target.elements;
  try {
    const d = await enviar("/login", { email: f.email.value.trim(), senha: f.senha.value });
    localStorage.setItem("token", d.access_token);
    localStorage.setItem("usuario", d.nome || f.email.value.trim());
    location.href = "index.html";
  } catch (e) {
    mostrar(e.message, "erro");
  }
});

$("formCadastro").addEventListener("submit", async (ev) => {
  ev.preventDefault();
  const f = ev.target.elements;
  if (f.senha.value !== f.confirmar.value) {
    mostrar("As senhas não conferem.", "erro");
    return;
  }
  const email = f.email.value.trim();
  try {
    await enviar("/cadastro", { nome: f.nome.value.trim(), email, senha: f.senha.value });
    ev.target.reset();
    aba(true);
    $("formLogin").elements.email.value = email;
    mostrar("Conta criada! Entre com seu e-mail e senha.", "ok");
  } catch (e) {
    mostrar(e.message, "erro");
  }
});

$("tabEntrar").onclick = () => aba(true);
$("tabCriar").onclick = () => aba(false);
