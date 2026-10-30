# UC4 – Atividade 2 – Django no servidor – Equipe 07

Oct 30, 2026 · @Matheus

## Capa

- **Equipe:** 07
- **Integrantes:** \[preencher com os nomes\]
- **Data:** 27/10/2026 (encontro) · entrega: \[preencher\]
- **Tema:** academia (model `Aluno`, app `academia`)
- **Servidor:** PostgreSQL da turma, banco `equipe07`

## 1. O que mudou no projeto

O projeto Django deixou de gravar no arquivo `db.sqlite3` e passou a usar o banco `equipe07` do servidor da turma. A configuração mudou em um arquivo; a view, o template e a rota foram criados para listar os alunos.

| Arquivo | O que foi escrito |
| --- | --- |
| `config/settings.py` | Imports de `os` e `dotenv`, chamada de `load_dotenv()` e novo bloco `DATABASES` com engine PostgreSQL, lendo host, porta, banco, usuário e senha de variáveis de ambiente |
| `.env` (raiz, fora do Git) | As 5 variáveis de conexão: `DB_HOST`, `DB_PORT`, `DB_NAME`, `DB_USER`, `DB_PASSWORD` |
| `.gitignore` | Linhas que impedem o envio de `.env`, `venv/` e `db.sqlite3*` ao GitHub |
| `academia/views.py` | Função `lista_alunos`, que busca os alunos pelo ORM e renderiza o template |
| `academia/templates/academia/lista_alunos.html` | Tabela HTML com um laço `for` sobre os alunos |
| `config/urls.py` | Rota `alunos/` apontando para a view |
| `dados.json` | Exportação dos 5 alunos do SQLite, gerada com `dumpdata` |
| `db.sqlite3` | Renomeado para `db.sqlite3.bak` (não apagado) |

Bloco `DATABASES` (sem a senha, que fica no `.env`):

```python
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': os.getenv('DB_NAME'),
        'USER': os.getenv('DB_USER'),
        'PASSWORD': os.getenv('DB_PASSWORD'),
        'HOST': os.getenv('DB_HOST'),
        'PORT': os.getenv('DB_PORT', '5432'),
    }
}
```

> **\[PRINT 1 – colar aqui\]** `.gitignore` aberto no VS Code, mostrando a linha `.env`.

> **\[PRINT 2 – colar aqui\]** Pasta do projeto no Explorer, mostrando `db.sqlite3.bak` no lugar do `db.sqlite3`.

## 2. As tabelas no servidor

O comando `migrate` criou as tabelas do Django e a tabela do model `Aluno` (`academia_aluno`) dentro do banco `equipe07`, no mesmo banco onde está a tabela `alunos` da Atividade 1.

> **\[PRINT 3 – colar aqui\]** SQLTools conectado em `equipe07`, com a pasta `Tables` aberta mostrando `academia_aluno`, as tabelas `auth_*` e `django_*`, e a tabela `alunos` da Atividade 1. A senha não pode aparecer.

## 3. Os dados

Os 5 alunos foram cadastrados no SQLite, exportados para `dados.json` e importados no PostgreSQL. Comandos na ordem em que foram executados, em `uc4-atividade2`:

| # | Comando | O que faz |
| --- | --- | --- |
| 1 | `python manage.py makemigrations` e `python manage.py migrate` | Criam a tabela do model `Aluno` no SQLite (`settings.py` ainda apontava para ele) |
| 2 | `python test.py` | Script que cadastra 5 alunos no banco atual pelo ORM (`get_or_create`) |
| 3 | `python manage.py dumpdata academia --indent 2 --output dados.json` | Exporta os alunos do SQLite para um arquivo JSON |
| 4 | Troca do `DATABASES` no `settings.py` e `Rename-Item db.sqlite3 db.sqlite3.bak` | O projeto passa a apontar para o PostgreSQL; o arquivo SQLite sai da pasta sem ser apagado |
| 5 | `python manage.py migrate` | Cria as tabelas do Django e a `academia_aluno` no banco `equipe07` |
| 6 | `python manage.py loaddata dados.json` | Grava no PostgreSQL os alunos do JSON. Saída: `Installed 5 object(s) from 1 fixture(s)` |
| 7 | `python manage.py createsuperuser` | Cria um superusuário novo no banco do servidor (o antigo ficou no SQLite) |

**Por que nessa ordem:** \[a equipe escreve com as próprias palavras. Perguntas para guiar: por que o `dumpdata` vem antes da troca do `DATABASES`? Por que o `migrate` vem antes do `loaddata`? Por que o superusuário precisou ser criado de novo?\]

> **\[PRINT 4 – colar aqui\]** Terminal mostrando `Installed 5 object(s) from 1 fixture(s)`.

> **\[PRINT 5 – colar aqui\]** SQLTools com `SELECT * FROM academia_aluno;` mostrando os 5 alunos (já enviado: print do resultado com Ana, Bruno, Carla, Diego e Elisa).

> **\[PRINT 6 – colar aqui\]** Painel admin (`/admin/`) listando os alunos, logado com o superusuário novo.

## 4. A página

A página `http://127.0.0.1:8000/alunos/` lista os alunos lidos da tabela `academia_aluno` do servidor.

> **\[PRINT 7 – colar aqui\]** Navegador em `127.0.0.1:8000/alunos/` com a tabela dos 5 alunos (já enviado).

**View** (`academia/views.py`):

```python
from django.shortcuts import render

from .models import Aluno


def lista_alunos(request):
    alunos = Aluno.objects.all().order_by("nome")
    return render(request, "academia/lista_alunos.html", {"alunos": alunos})
```

**Rota** (`config/urls.py`):

```python
path("alunos/", views.lista_alunos, name="lista_alunos"),
```

**Template** (`academia/templates/academia/lista_alunos.html`):

```html
<h1>Alunos da academia</h1>
<table border="1" cellpadding="6">
    <tr>
        <th>Nome</th><th>Idade</th><th>Matrícula</th><th>Ativo</th><th>Mensalidade</th>
    </tr>
    {% for a in alunos %}
    <tr>
        <td>{{ a.nome }}</td>
        <td>{{ a.idade }}</td>
        <td>{{ a.data_matricula }}</td>
        <td>{{ a.ativo|yesno:"Sim,Não" }}</td>
        <td>R$ {{ a.mensalidade }}</td>
    </tr>
    {% empty %}
    <tr><td colspan="5">Nenhum aluno cadastrado.</td></tr>
    {% endfor %}
</table>
```

## 5. Explicação – sem IA

**\[A equipe escreve esta seção com as próprias palavras, no mínimo 15 linhas. Apague este aviso e as perguntas abaixo depois de escrever.\]**

Perguntas que o texto deve responder, seguindo o caminho de um clique até a tabela e de volta:

1. O que acontece quando o navegador pede `/alunos/`? Qual arquivo recebe o pedido primeiro?
2. O que a view faz com esse pedido? Onde entra o ORM (`Aluno.objects.all()`)?
3. O que o ORM entrega ao PostgreSQL, e o que o servidor devolve?
4. Como os dados chegam ao template e viram a tabela HTML?
5. O que mudou no projeto ao trocar SQLite por PostgreSQL, e o que não mudou (model, view, template)? Por quê?
6. Por que a senha está no `.env` e não no `settings.py`?

&#91;escrever aqui\]

## 6. Dificuldades e diário de IA

### Dificuldades

| Problema | Mensagem ou sintoma | Como resolvemos |
| --- | --- | --- |
| Comando rodado na pasta errada | `can't open file '...\\manage.py': [Errno 2] No such file or directory` | O `manage.py` fica em `uc4-atividade2`; entramos na pasta com `cd uc4-atividade2` |
| `dados.json` vazio | O arquivo continha apenas `[]` | O `dumpdata` rodou antes de haver alunos no SQLite; cadastramos 5 alunos (script `test.py`) e exportamos de novo |
| `makemigrations` sem efeito | `No changes detected` | A migração `0001_initial.py` já existia; conferimos com `ls academia\\migrations` e `showmigrations` |
| Renomear o SQLite | `Não é possível renomear porque o item em 'db.sqlite3' não existe` | O arquivo já estava como `db.sqlite3.bak` |
| Superusuário repetido | `Error: That username is already taken.` | O `admin` já existia no banco do servidor; criamos outro usuário |
| Página não encontrada | `Page not found (404)` em `http://127.0.0.1:8000/` | Só existem as rotas `admin/` e `alunos/`; abrimos `/alunos/` |
| Template não encontrado | `TemplateDoesNotExist at /alunos/` | A pasta estava como `template`; o Django procura `templates`, então renomeamos |

### Diário de IA

- **O que perguntamos:** \[preencher com as perguntas feitas à IA\]
- **O que usamos:** o passo a passo da Atividade 1, o script `atividade1_crud.py`, o roteiro da Atividade 2, o `settings.py` com PostgreSQL e o script `test.py`.
- **O que alteramos ou descartamos, e por quê:** \[a equipe preenche\]
