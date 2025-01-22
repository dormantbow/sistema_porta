Resumo do Projeto Até Agora:
O projeto está sendo desenvolvido para controlar e monitorar portas em um sistema distribuído, utilizando MQTT para comunicação entre as portas e o backend em Django. O sistema também inclui um banco de dados MySQL para armazenar informações sobre o estado das portas, agendamentos e históricos de acesso.

O que foi feito até agora:
Criação do Banco de Dados e Models no Django:

Criamos um model Door para armazenar as portas, com os campos status (se está aberta ou fechada) e is_scheduled (se está agendada para uso).
Criamos o model Schedule para representar os agendamentos das portas, incluindo o usuário que fez o agendamento e os horários de início e término.
Criamos o model AccessHistory para registrar o histórico de acessos nas portas.
Desenvolvimento do Backend em Django:

Configuramos um app Django chamado doors, onde implementamos endpoints API para:
Obter status das portas: Endpoint GET para consultar o estado atual das portas.
Atualizar status das portas: Endpoint POST para atualizar o status da porta quando um evento MQTT é recebido.
Integração com MQTT:

Configuramos um cliente MQTT para ouvir os tópicos relacionados ao status das portas.
O cliente MQTT é responsável por processar as mensagens recebidas e atualizar o status das portas no banco de dados.
A lógica de atualização do status inclui verificar se a porta está agendada e registrar o histórico de acessos.
Testes de Funcionalidade:

Testamos o endpoint de atualização de status via Postman, enviando um JSON com o door_id e o novo status.
Realizamos testes de integração do MQTT, verificando se as mensagens publicadas no tópico MQTT atualizam corretamente o status das portas no banco de dados.
Testamos a lógica de agendamento e atualização de is_scheduled.
Como Está Funcionando:
API Backend (Django):
A aplicação Django está configurada para fornecer uma API REST que permite:
Consultar o estado das portas.
Atualizar o status das portas com base nas mensagens MQTT.
Comunicando com o MQTT:
O sistema está configurado para receber atualizações de status das portas via mensagens MQTT publicadas no tópico doors/status/.
Quando uma mensagem é recebida, o cliente MQTT processa a mensagem, atualiza o status da porta no banco de dados e registra um histórico de acesso.
Banco de Dados MySQL:
As portas, agendamentos e históricos de acesso são armazenados no banco de dados MySQL.
As portas podem ser consultadas para verificar seu status atual e se estão agendadas para uso.
Os agendamentos e o histórico de acessos são registrados para cada porta, com os detalhes do usuário que fez o agendamento e o horário do acesso.
para instalação do projeto
pip install -r requirements.txt
