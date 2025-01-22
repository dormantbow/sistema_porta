from django.shortcuts import render
from django.http import JsonResponse
import datetime
from .models import Porta, Agendamento
import json
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import get_object_or_404

import logging

logger = logging.getLogger(__name__)


#listando portas dispoviveis
def listar_portas(request):
    portas = Porta.objects.filter(disponivel=True)
    logger.info(f"Portas disponíveis: {list(portas)}")
    data = [{"id": porta.id, "nome": porta.nome, "status": porta.status} for porta in portas]
    print(portas)
    return JsonResponse(data, safe=False)

#agendando portas@csrf_exempt   
@csrf_exempt
def agendar_porta(request):
    if request.method == "POST":
        try:
            # Carregar JSON
            try:
                dados = json.loads(request.body)
            except json.JSONDecodeError:
                return JsonResponse({"erro": "JSON inválido."}, status=400)

            # Extrair dados
            porta_id = dados.get("porta_id")
            usuario = dados.get("usuario")
            inicio = dados.get("inicio")
            fim = dados.get("fim")

            # Validar campos obrigatórios
            if not all([porta_id, usuario, inicio, fim]):
                return JsonResponse({"erro": "Todos os campos são obrigatórios."}, status=400)

            # Validar formato das datas
            try:
                inicio_data = datetime.datetime.fromisoformat(inicio)
                fim_data = datetime.datetime.fromisoformat(fim)
            except ValueError:
                return JsonResponse({"erro": "Formato de data inválido. Use ISO 8601."}, status=400)

            # Recuperar porta
            try:
                porta = Porta.objects.get(id=porta_id)
            except Porta.DoesNotExist:
                return JsonResponse({"erro": f"Porta com ID {porta_id} não encontrada."}, status=404)

            # Verificar disponibilidade
            if not porta.disponivel:
                return JsonResponse({"erro": "Porta indisponível."}, status=400)

            # Criar agendamento
            agendamento = Agendamento.objects.create(
                porta=porta,
                usuario=usuario,
                inicio=inicio_data,
                fim=fim_data
            )

            # Atualizar disponibilidade da porta
            porta.disponivel = False
            porta.save()

            return JsonResponse({"mensagem": "Agendamento realizado com sucesso."})

        except Exception as e:
            return JsonResponse({"erro": f"Ocorreu um erro inesperado: {str(e)}"}, status=500)

    return JsonResponse({"erro": "Método não permitido."}, status=405)

