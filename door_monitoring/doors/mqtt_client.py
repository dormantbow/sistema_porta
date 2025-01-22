import paho.mqtt.client as mqtt
from .models import Door, AccessHistory
from django.utils.timezone import now

BROKER_URL = "localhost"  # Substitua pelo endereço do seu broker MQTT
BROKER_PORT = 1883  # Porta padrão do MQTT

def on_connect(client, userdata, flags, rc):
    print("Conectado ao MQTT Broker com código de retorno:", rc)
    client.subscribe("doors/status/")  # Substitua pelo tópico correto

def on_message(client, userdata, msg):
    """
    Callback executado quando uma mensagem é recebida no tópico.
    """
    try:
        payload = msg.payload.decode()
        print(f"Mensagem recebida: {payload}")
        
        # Parse da mensagem (JSON esperado)
        import json
        data = json.loads(payload)
        door_id = data.get("door_id")
        status = data.get("status")  # True (aberta), False (fechada)

        # Atualizar o status da porta no banco de dados
        door = Door.objects.get(id=door_id)
        door.status = status
        door.save()

        # Registrar no histórico de acessos
        AccessHistory.objects.create(
            door=door,
            user="MQTT",  # Identificador genérico
            action="open" if status else "close",
            timestamp=now()
        )
    except Exception as e:
        print(f"Erro ao processar mensagem MQTT: {e}")

def start_mqtt_client():
    client = mqtt.Client()
    client.on_connect = on_connect
    client.on_message = on_message

    client.connect(BROKER_URL, BROKER_PORT)
    client.loop_start()
