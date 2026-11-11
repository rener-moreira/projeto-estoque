from fastapi import APIRouter, HTTPException
from argon2 import PasswordHasher
from argon2.exceptions import VerifyMismatchError
from models import CadastroUser, Login
from psycopg.errors import UniqueViolation
from banco import conexao
import os
import jwt
from datetime import datetime, timedelta, timezone

router = APIRouter()

hasher = PasswordHasher()

@router.post("/cadastro", status_code=201)
def criar_conta(user: CadastroUser):
    email_tratado = user.email.strip() 
    email = email_tratado.lower()
    senha_hash = hasher.hash(user.senha)

    conectar = conexao()
    cursor = conectar.cursor()

    try:
        cursor.execute(
            "INSERT INTO usuarios (nome, email, senha) VALUES (%s, %s, %s)", (user.nome, email, senha_hash)
        )
        conectar.commit()

    except UniqueViolation:
        conectar.rollback()
        raise HTTPException(409, "Este e-mail já existe")
    finally:
        cursor.close()
        conectar.close()

    return {"msg":"Email Cadastrado com Sucesso"} 


@router.post("/login")
def login(login: Login):
    email = login.email.strip()
    email_tratado = email.lower()

    conectar = conexao()
    cursor = conectar.cursor()

    try:
        cursor.execute(
            "SELECT id, nome, senha FROM usuarios WHERE email=%s", (email_tratado,)
        )

        resultado = cursor.fetchone()
     
    finally:
        cursor.close()
        conectar.close()

    if resultado is None:
        raise HTTPException(401, "Email ou senha incorretos")

    try:
        hasher.verify(resultado["senha"],login.senha)
    except VerifyMismatchError:
        raise HTTPException(401, "Email ou senha incorretos")


    payload = {
        'sub': str(resultado['id']),
        'exp': datetime.now(timezone.utc) + timedelta(hours=1)
        }  

    token = jwt.encode(payload, os.environ["JWT_SECRET"], algorithm="HS256")

    return {
    "access_token": token,
    "token_type": "bearer",
    "nome": resultado["nome"],
    }