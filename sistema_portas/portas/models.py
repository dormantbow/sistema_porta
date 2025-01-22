from django.db import models

class Porta(models.Model):
    nome = models.CharField(max_length=100, unique=True)  # Nome ou número da porta
    status = models.CharField(max_length=10, choices=[('aberta', 'Aberta'), ('fechada', 'Fechada')], default='fechada')
    disponivel = models.BooleanField(default=True)  # Indica se a porta está disponível para agendamento
    #descricao = models.TextField(blank=True, null=True)  # Opcional, para detalhes adicionais

    def __str__(self):
        return self.nome


class Agendamento(models.Model):
    porta = models.ForeignKey(Porta, on_delete=models.CASCADE, related_name='agendamentos')
    usuario = models.CharField(max_length=100)  # Nome ou ID do professor
    inicio = models.DateTimeField()  # Data e hora de início do agendamento
    fim = models.DateTimeField()    # Data e hora do fim do agendamento

    def __str__(self):
        return f"Agendamento de {self.usuario} na porta {self.porta.nome}"

