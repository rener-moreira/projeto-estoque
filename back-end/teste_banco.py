from banco import conexao

with conexao() as conn:
    resultado = conn.execute("""
        SELECT current_database(), current_schema();
    """).fetchone()

    print(resultado)