from pydantic import BaseModel, Field
from typing import Literal

class ProdutosEntrada(BaseModel):
    nome: str = Field(min_length=1, max_length=80)
    sku: str = Field(min_length=1, max_length=30)
    categoria: str = Field(min_length=1, max_length=40)
    quantidade: int = Field(ge=0)
    preco: float = Field(ge=0)

class Produto(ProdutosEntrada):
    id: int