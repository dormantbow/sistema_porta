import paho.mqtt.client as mqtt

BROKER_URL = "localhost"  # Substitua pelo seu broker
BROKER_PORT = 1883

def on_connect(client, userdata, flags, rc):
    print(f"Conectado com código de retorno {rc}")

client = mqtt.Client()
client.on_connect = on_connect
client.connect(BROKER_URL, BROKER_PORT)
client.loop_forever()
