"""Cadastra 5 alunos no banco atual do projeto (rode ainda com o SQLite)."""
import os
from datetime import date
from decimal import Decimal

import django

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")
django.setup()

from academia.models import Aluno  # noqa: E402  (precisa vir depois do setup)

alunos = [
    ("Ana Souza", 25, date(2026, 1, 10), True, Decimal("99.90")),
    ("Bruno Lima", 31, date(2026, 2, 3), True, Decimal("99.90")),
    ("Carla Dias", 19, date(2026, 3, 15), False, Decimal("79.90")),
    ("Diego Alves", 42, date(2025, 11, 20), True, Decimal("129.90")),
    ("Elisa Rocha", 28, date(2026, 4, 1), True, Decimal("99.90")),
]

for nome, idade, data_matricula, ativo, mensalidade in alunos:
    aluno, criado = Aluno.objects.get_or_create(
        nome=nome,
        defaults={
            "idade": idade,
            "data_matricula": data_matricula,
            "ativo": ativo,
            "mensalidade": mensalidade,
        },
    )
    print(("Criado: " if criado else "Já existia: ") + aluno.nome)

print("Total de alunos no banco:", Aluno.objects.count())