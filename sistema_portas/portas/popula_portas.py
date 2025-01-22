import os
import django

# Configurar o ambiente do Django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "sistema_portas.settings")
django.setup()

from portas.models import Porta

# Dados das portas
portas_iniciais = [
    {"nome": "Porta 1", "status": "fechada", "disponivel": True},
    {"nome": "Porta 2", "status": "fechada", "disponivel": True},
    {"nome": "Porta 3", "status": "fechada", "disponivel": True},
    {"nome": "Porta 4", "status": "fechada", "disponivel": True},
    {"nome": "Porta 5", "status": "fechada", "disponivel": True},
    {"nome": "Porta 6", "status": "fechada", "disponivel": True},
    {"nome": "Porta 7", "status": "fechada", "disponivel": True},
    {"nome": "Porta 8", "status": "fechada", "disponivel": True},
    {"nome": "Porta 9", "status": "fechada", "disponivel": True},
    {"nome": "Porta 10", "status": "fechada", "disponivel": True},
]

# Inserir portas no banco de dados
for porta in portas_iniciais:
    obj, created = Porta.objects.get_or_create(nome=porta["nome"], defaults=porta)
    if created:
        print(f"Porta '{porta['nome']}' criada com sucesso!")
    else:
        print(f"Porta '{porta['nome']}' já existe.")
