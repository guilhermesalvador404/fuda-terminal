import json
import socket

# Configurações de rede
DEFAULT_HOST = '0.0.0.0'  # Escuta em todas as interfaces
DEFAULT_PORT = 5555
BUFFER_SIZE = 4096

# Tipos de mensagem
MSG_TYPES = {
    'CREATE_ROOM': 'create_room',
    'JOIN_ROOM': 'join_room',
    'LEAVE_ROOM': 'leave_room',
    'START_VOTING': 'start_voting',
    'SUBMIT_VOTE': 'submit_vote',
    'REVEAL_VOTES': 'reveal_votes',
    'RESET_ROUND': 'reset_round',
    'ROOM_STATUS': 'room_status',
    'ERROR': 'error',
    'SUCCESS': 'success'
}

def create_message(msg_type, data=None):
    """Cria uma mensagem padronizada para envio"""
    return json.dumps({
        'type': msg_type,
        'data': data or {}
    })

def parse_message(message_str):
    """Faz parse de uma mensagem recebida"""
    try:
        return json.loads(message_str)
    except json.JSONDecodeError:
        return None

def send_message(sock, msg_type, data=None):
    """Envia uma mensagem através do socket"""
    message = create_message(msg_type, data)
    sock.send(message.encode('utf-8'))

def receive_message(sock):
    """Recebe e faz parse de uma mensagem do socket"""
    try:
        data = sock.recv(BUFFER_SIZE).decode('utf-8')
        if not data:
            return None
        return parse_message(data)
    except:
        return None