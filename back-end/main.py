from fastapi import FastAPI, HTTPException
from models import ProdutosEntrada, Produto
from psycopg.errors import UniqueViolation
from banco import conexao

app = FastAPI()

produtos = [
    {   
        "id":1,
        "nome": "Teclado mecânico",
        "sku": "TEC-001",
        "categoria": "Periféricos",
        "quantidade": 25,
        "preco": 189.90
    },
    {   
        "id":2,
        "nome": "Mouse sem fio",
        "sku": "MOU-002",
        "categoria": "Periféricos",
        "quantidade": 40,
        "preco": 79.90
    },
    {   
        "id":3,
        "nome": "Monitor 24 polegadas",
        "sku": "MON-003",
        "categoria": "Monitores",
        "quantidade": 12,
        "preco": 749.00
    },
    {   
        "id":4,
        "nome": "Cabo HDMI 2m",
        "sku": "CAB-004",
        "categoria": "Cabos",
        "quantidade": 3,
        "preco": 24.50
    },
    {   
        "id":5,
        "nome": "Webcam Full HD",
        "sku": "WEB-005",
        "categoria": "Periféricos",
        "quantidade": 0,
        "preco": 159.00
    },
    {
        "id":6,
        "nome": "Headset gamer",
        "sku": "HEA-006",
        "categoria": "Áudio",
        "quantidade": 8,
        "preco": 229.90
    },
    {   
        "id":7,
        "nome": "Hub USB-C",
        "sku": "HUB-007",
        "categoria": "Acessórios",
        "quantidade": 5,
        "preco": 119.00
    },
    {   
        "id":8,
        "nome": "Suporte para notebook",
        "sku": "SUP-008",
        "categoria": "Acessórios",
        "quantidade": 18,
        "preco": 94.90
    }
]

proximo_id = 9

@app.get("/produtos", response_model=list[Produto])
def listar_produtos():
    conectar = conexao()
    cursor = conectar.cursor()

    cursor.execute(
        "SELECT * FROM produtos ORDER BY id"
    )

    produto = cursor.fetchall()

    cursor.close()
    conectar.close()
    return produto

@app.post("/produtos", status_code=201)
def criar_produtos(prod: ProdutosEntrada):
    conectar = conexao()
    cursor = conectar.cursor()

    try:
        cursor.execute(
            "INSERT INTO produtos (nome, sku, categoria, quantidade, preco) VALUES (%s,%s,%s,%s,%s) RETURNING *", (
                prod.nome, prod.sku, prod.categoria, prod.quantidade, prod.preco
            )
        )
        p = cursor.fetchone()
        conectar.commit()

    except UniqueViolation:
            conectar.rollback()
            raise HTTPException(409, f"SKU já em uso") 
        
    finally: 
        cursor.close()
        conectar.close()

    return p

@app.delete("/produtos/{id}", status_code=204)
def  deletar_by_id(id:int):
    conectar = conexao()
    cursor = conectar.cursor()
    
    try:
        cursor.execute(
                    "DELETE FROM produtos WHERE id=%s", (id,)
                )
        if cursor.rowcount == 0:
                raise HTTPException(404, "Produto não encontrado")

        conectar.commit()

    finally:
        cursor.close()
        conectar.close()

    return


@app.put("/produtos/{id}")
def atualizar_produto(id:int, prod_novo: ProdutosEntrada):
    conectar = conexao()
    cursor = conectar.cursor()

    cursor.execute(
        "SELECT id FROM produtos WHERE id=%s", (id,)
    )

    if not cursor.fetchone():
        cursor.close()
        conectar.close()
        raise HTTPException(404, "Produto não encontrado")

    campos = []
    valores = []

    for campo, valor in prod_novo.model_dump(exclude_unset=True).items():
        campos.append(f"{campo}=%s")
        valores.append(valor) 


    if not campos:
        cursor.close()
        conectar.close()
        raise HTTPException(400, "Nenhum campo foi atualizado")

    valores.append(id)

    try:
            cursor.execute(
                f"UPDATE produtos SET {', '.join(campos)} WHERE id=%s", valores
            )

            conectar.commit()
            
    except UniqueViolation:
        conectar.rollback()
        raise HTTPException(409, "SKU já em uso")

    finally:
        cursor.close()
        conectar.close()
    
    return {"msg":"Produto Atualizado com sucesso"}


    # for produto in produtos:
    #     if produto["id"] == id :
    #         if any(p["sku"] == prod_novo.sku and p["id"] != id for p in produtos):
    #           raise HTTPException (409, "SKU já em uso") 
    #         produto.update(prod_novo.model_dump())
    #         return produto

    # raise HTTPException(404, "Produto não encontrado")


    # Problemas: 
    #     Corrigir a atualização do SKU, para não atualizar produtos com um SKU existente