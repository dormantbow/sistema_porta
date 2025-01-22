import paho.mqtt.client as mqtt

BROKER = "broker.hivemq.com"
PORT = 1883
TOPICOS = ["sistema/portas/status", "sistema/portas/agendamentos"]

def on_message(client, userdata, msg):
    print(f"Tópico: {msg.topic}, Mensagem: {msg.payload.decode()}")

client = mqtt.Client()
client.on_message = on_message

client.connect(BROKER, PORT, 60)
for topico in TOPICOS:
    client.subscribe(topico)

print("Cliente MQTT rodando. Pressione Ctrl+C para sair.")
client.loop_forever()
