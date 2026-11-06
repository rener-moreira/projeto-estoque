from fastapi import FastAPI, HTTPException
from models import ProdutosEntrada, Produto
from psycopg.errors import UniqueViolation
from banco import conexao

app = FastAPI()

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