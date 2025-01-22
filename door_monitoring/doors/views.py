from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import Door, AccessHistory, Schedule
from django.utils.timezone import now
from django.shortcuts import get_object_or_404

# Monitoramento em tempo real
class DoorStatusView(APIView):
    def get(self, request):
        """
        Retorna o status atual de todas as portas.
        """
        doors = Door.objects.all()
        data = [
            {
                "id": door.id,
                "name": door.name,
                "status": "Aberta" if door.status else "Fechada",
                "is_scheduled": door.is_scheduled
            }
            for door in doors
        ]
        return Response(data, status=status.HTTP_200_OK)

# Histórico de acessos
class AccessHistoryView(APIView):
    def get(self, request):
        """
        Retorna o histórico de acessos com filtros opcionais.
        """
        door_id = request.query_params.get('door_id')
        user = request.query_params.get('user')
        
        queryset = AccessHistory.objects.all()

        # Filtrando por porta, se especificado
        if door_id:
            queryset = queryset.filter(door__id=door_id)
        
        # Filtrando por usuário, se especificado
        if user:
            queryset = queryset.filter(user=user)
        
        # Serializando o histórico
        data = [
            {
                "door": history.door.name,
                "user": history.user,
                "action": history.action,
                "timestamp": history.timestamp.strftime("%Y-%m-%d %H:%M:%S"),
            }
            for history in queryset
        ]
        return Response(data, status=status.HTTP_200_OK)

# Agendamentos
class ScheduleView(APIView):
    def get(self, request):
        """
        Retorna a lista de agendamentos existentes.
        """
        schedules = Schedule.objects.all()
        data = [
            {
                "id": schedule.id,
                "door": schedule.door.name,
                "user": schedule.user,
                "start_time": schedule.start_time.strftime("%Y-%m-%d %H:%M:%S"),
                "end_time": schedule.end_time.strftime("%Y-%m-%d %H:%M:%S"),
            }
            for schedule in schedules
        ]
        return Response(data, status=status.HTTP_200_OK)

    def post(self, request):
        """
        Cria um novo agendamento para uma porta.
        """
        door_id = request.data.get('door_id')
        user = request.data.get('user')
        start_time = request.data.get('start_time')
        end_time = request.data.get('end_time')

        # Validando porta
        door = get_object_or_404(Door, id=door_id)

        # Criando agendamento
        schedule = Schedule.objects.create(
            door=door,
            user=user,
            start_time=start_time,
            end_time=end_time
        )
        return Response({"message": "Agendamento criado com sucesso!"}, status=status.HTTP_201_CREATED)

# Atualizar status da porta via MQTT
class UpdateDoorStatusView(APIView):
    def post(self, request):
        """
        Atualiza o status de uma porta (aberta/fechada).
        Essa funcionalidade seria acionada pelo sistema MQTT.
        """
        door_id = request.data.get('door_id')
        status_value = request.data.get('status')  # True para aberta, False para fechada

        door = get_object_or_404(Door, id=door_id)
        door.status = status_value
        door.save()

        # Registrar no histórico de acessos
        AccessHistory.objects.create(
            door=door,
            user="MQTT",  # Identificador genérico
            action="open" if status_value else "close",
            timestamp=now()
        )
        return Response({"message": "Status da porta atualizado com sucesso!"}, status=status.HTTP_200_OK)
