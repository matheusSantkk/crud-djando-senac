from django.db import models


class Aluno(models.Model):
    nome = models.CharField(max_length=100)
    idade = models.IntegerField()
    data_matricula = models.DateField()
    ativo = models.BooleanField(default=True)
    mensalidade = models.DecimalField(max_digits=8, decimal_places=2)

    def __str__(self):
        return self.nome
