"""Atividade 1 - CRUD em Python no PostgreSQL da turma (tema: academia)."""
import os

import psycopg
from dotenv import load_dotenv

load_dotenv()  # lê o arquivo .env (que está no .gitignore)

conn = psycopg.connect(
    host=os.getenv("DB_HOST"),
    port=os.getenv("DB_PORT", "5432"),
    dbname=os.getenv("DB_NAME"),
    user=os.getenv("DB_USER"),
    password=os.getenv("DB_PASSWORD"),
)
cur = conn.cursor()
print("Conectado ao banco:", os.getenv("DB_NAME"))


def pausa(msg):
    input(f"\n>>> {msg} Tire o print no SQLTools e aperte Enter... ")


def mostrar(titulo, linhas):
    print(f"\n--- {titulo} ---")
    for linha in linhas:
        print(linha)


# ---------- Tabela ----------
cur.execute("DROP TABLE IF EXISTS alunos")
cur.execute(
    """
    CREATE TABLE alunos (
        id SERIAL PRIMARY KEY,
        nome VARCHAR(100) NOT NULL,
        idade INTEGER,
        data_matricula DATE,
        ativo BOOLEAN DEFAULT TRUE,
        mensalidade NUMERIC(8, 2)
    )
    """
)
conn.commit()
pausa("Tabela criada (print da estrutura).")

# ---------- CREATE ----------
alunos = [
    ("Ana Souza", 25, "2026-01-10", True, 99.90),
    ("Bruno Lima", 31, "2026-02-03", True, 99.90),
    ("Carla Dias", 19, "2026-03-15", False, 79.90),
    ("Diego Alves", 42, "2025-11-20", True, 129.90),
    ("Elisa Rocha", 28, "2026-04-01", True, 99.90),
]
cur.executemany(
    "INSERT INTO alunos (nome, idade, data_matricula, ativo, mensalidade) "
    "VALUES (%s, %s, %s, %s, %s)",
    alunos,
)
conn.commit()
print("CREATE: 5 alunos inseridos")
pausa("CREATE feito.")

# ---------- READ ----------
cur.execute("SELECT * FROM alunos")
mostrar("READ: todos", cur.fetchall())

cur.execute("SELECT * FROM alunos WHERE ativo = %s", (True,))
mostrar("READ: só ativos (WHERE)", cur.fetchall())

cur.execute("SELECT * FROM alunos ORDER BY idade DESC")
mostrar("READ: por idade, do mais velho (ORDER BY)", cur.fetchall())
pausa("READ feito (print do terminal).")

# ---------- UPDATE ----------
cur.execute("SELECT * FROM alunos WHERE nome = %s", ("Carla Dias",))
mostrar("UPDATE: antes", cur.fetchall())
pausa("Print ANTES do update.")
cur.execute(
    "UPDATE alunos SET ativo = %s, mensalidade = %s WHERE nome = %s",
    (True, 99.90, "Carla Dias"),
)
conn.commit()
cur.execute("SELECT * FROM alunos WHERE nome = %s", ("Carla Dias",))
mostrar("UPDATE: depois", cur.fetchall())
pausa("Print DEPOIS do update.")

# ---------- DELETE ----------
cur.execute("SELECT * FROM alunos ORDER BY id")
mostrar("DELETE: antes", cur.fetchall())
pausa("Print ANTES do delete.")
cur.execute("DELETE FROM alunos WHERE nome = %s", ("Diego Alves",))
conn.commit()
cur.execute("SELECT * FROM alunos ORDER BY id")
mostrar("DELETE: depois", cur.fetchall())
pausa("Print DEPOIS do delete.")

cur.close()
conn.close()
print("\nConexão fechada.")