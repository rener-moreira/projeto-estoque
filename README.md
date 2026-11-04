# Sistema de Estoque

Aplicação web para gerenciamento de produtos em estoque, desenvolvida com **Python, FastAPI e PostgreSQL**, com uma interface web em HTML, CSS e JavaScript.

O projeto foi desenvolvido com foco no aprendizado e na aplicação prática de desenvolvimento de APIs REST, integração com banco de dados e comunicação entre front-end e back-end.

## Funcionalidades

- Listar produtos cadastrados.
- Cadastrar novos produtos.
- Excluir produtos.
- Editar informações de produtos pela interface.
- Buscar produtos por nome, SKU ou categoria.
- Exibir resumo do estoque:
  - quantidade de produtos cadastrados;
  - total de unidades;
  - valor total estimado do estoque.
- Identificar produtos sem estoque, com estoque baixo ou disponíveis.
- Validar dados de entrada, incluindo quantidade e preço não negativos.
- Impedir o cadastro de produtos com SKU duplicado no endpoint de criação.

## Tecnologias

### Back-end
- Python
- FastAPI
- Pydantic
- Psycopg
- python-dotenv

### Banco de dados
- PostgreSQL

### Front-end
- HTML
- CSS
- JavaScript

## Estrutura do projeto

```text
.
├── back-end/
│   ├── main.py          # Aplicação FastAPI e endpoints
│   ├── banco.py         # Configuração da conexão com PostgreSQL
│   ├── models.py        # Modelos e validações com Pydantic
│   └── teste_banco.py   # Teste simples de conexão com o banco
├── front/
│   ├── index.html       # Interface da aplicação
│   ├── javascript.js    # Integração com a API e comportamento da interface
│   └── style.css        # Estilos
├── .gitignore
└── README.md
```

## Pré-requisitos

- Python 3.10 ou superior
- PostgreSQL
- Git

## Configuração e execução

### 1. Clone o repositório

```bash
git clone https://github.com/SEU-USUARIO/SEU-REPOSITORIO.git
cd SEU-REPOSITORIO
```

### 2. Crie e ative um ambiente virtual

Linux/macOS:

```bash
python3 -m venv .venv
source .venv/bin/activate
```

Windows:

```bash
python -m venv .venv
.venv\Scripts\activate
```

### 3. Instale as dependências

```bash
pip install fastapi "uvicorn[standard]" "psycopg[binary]" python-dotenv
```

### 4. Configure o banco de dados

Crie um banco PostgreSQL para a aplicação. Em seguida, crie a tabela de produtos:

```sql
CREATE TABLE produtos (
    id SERIAL PRIMARY KEY,
    nome VARCHAR(80) NOT NULL,
    sku VARCHAR(30) NOT NULL UNIQUE,
    categoria VARCHAR(40) NOT NULL,
    quantidade INTEGER NOT NULL CHECK (quantidade >= 0),
    preco NUMERIC(10, 2) NOT NULL CHECK (preco >= 0)
);
```

### 5. Configure as variáveis de ambiente

Crie um arquivo `.env` dentro da pasta `back-end/`:

```env
DB_USER=seu_usuario
DB_PASSWORD=sua_senha
DB_HOST=localhost
DB_NAME=seu_banco
```

**Não publique o arquivo `.env` nem suas credenciais no GitHub.**

### 6. Inicie o back-end

Entre na pasta do back-end:

```bash
cd back-end
```

Execute:

```bash
uvicorn main:app --reload
```

A API ficará disponível em:

```text
http://localhost:8000
```

Documentação interativa da API:

```text
http://localhost:8000/docs
```

### 7. Abra o front-end

Abra `front/index.html` no navegador. A interface está configurada para acessar a API em `http://localhost:8000`.

## Endpoints da API

| Método | Rota | Descrição |
|---|---|---|
| `GET` | `/produtos` | Lista os produtos |
| `POST` | `/produtos` | Cadastra um produto |
| `PUT` | `/produtos/{id}` | Atualiza um produto |
| `DELETE` | `/produtos/{id}` | Exclui um produto |

### Exemplo de corpo para cadastro

```json
{
  "nome": "Teclado mecânico",
  "sku": "TEC-001",
  "categoria": "Periféricos",
  "quantidade": 25,
  "preco": 189.90
}
```

## Sobre o desenvolvimento

O back-end, incluindo a API e a integração com o PostgreSQL, foi desenvolvido por mim.

A interface inicial do front-end foi criada com auxílio de inteligência artificial e integrada à API do projeto.

## Status

Projeto em desenvolvimento. Novas melhorias, funcionalidades e testes poderão ser adicionados ao longo da evolução.

## Autor

**Rener Moreira**

- GitHub: [@renermoreira](https://github.com/renermoreira)
