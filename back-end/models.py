from pydantic import BaseModel, Field, EmailStr

class ProdutosEntrada(BaseModel):
    nome: str = Field(min_length=1, max_length=80)
    sku: str = Field(min_length=1, max_length=30)
    categoria: str = Field(min_length=1, max_length=40)
    quantidade: int = Field(ge=0)
    preco: float = Field(ge=0)

class Produto(ProdutosEntrada):
    id: int

class CadastroUser(BaseModel):
    nome: str = Field(min_length=1, max_length=80)
    email: EmailStr 
    senha: str = Field(min_length=8, max_length=128)

class Login(BaseModel):
    email: EmailStr
    senha: str = Field(max_length=128)