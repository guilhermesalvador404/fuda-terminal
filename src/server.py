"""
Servidor do Planning Poker
Gerencia salas, jogadores e comunicação entre clientes
"""

import socket
import threading
import json
import uuid
from datetime import datetime
from typing import Dict, Optional

from src.models.room import Room
from src.models.player import Player
from src.utils.network import (
    DEFAULT_HOST, DEFAULT_PORT, BUFFER_SIZE,
    MSG_TYPES, parse_message, send_message
)
from src.utils.display import print_header, print_success, print_error, print_info


class PlanningPokerServer:
    def __init__(self, host=DEFAULT_HOST, port=DEFAULT_PORT):
        self.host = host
        self.port = port
        self.server_socket = None
        self.rooms: Dict[str, Room] = {}
        self.clients: Dict[socket.socket, Player] = {}
        self.running = False
        self.lock = threading.Lock()
        
    def start(self):
        """Inicia o servidor"""
        try:
            self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            self.server_socket.bind((self.host, self.port))
            self.server_socket.listen(5)
            self.running = True
            
            print_header("PLANNING POKER - SERVIDOR")
            print_success(f"Servidor rodando em {self.host}:{self.port}")
            print_info("Pressione Ctrl+C para parar o servidor\n")
            
            # Thread para aceitar conexões
            accept_thread = threading.Thread(target=self.accept_connections)
            accept_thread.daemon = True
            accept_thread.start()
            
            # Thread para mostrar status
            status_thread = threading.Thread(target=self.print_status)
            status_thread.daemon = True
            status_thread.start()
            
            # Mantém o servidor rodando
            try:
                while self.running:
                    threading.Event().wait(1)
            except KeyboardInterrupt:
                self.stop()
                
        except Exception as e:
            print_error(f"Erro ao iniciar servidor: {e}")
            self.stop()
    
    def accept_connections(self):
        """Aceita novas conexões de clientes"""
        while self.running:
            try:
                client_socket, address = self.server_socket.accept()
                print_success(f"Nova conexão de {address[0]}:{address[1]}")
                
                # Cria thread para lidar com o cliente
                client_thread = threading.Thread(
                    target=self.handle_client,
                    args=(client_socket, address)
                )
                client_thread.daemon = True
                client_thread.start()
                
            except Exception as e:
                if self.running:
                    print_error(f"Erro ao aceitar conexão: {e}")
    
    def handle_client(self, client_socket: socket.socket, address):
        """Gerencia a comunicação com um cliente específico"""
        player = None
        try:
            while self.running:
                data = client_socket.recv(BUFFER_SIZE).decode('utf-8')
                if not data:
                    break
                
                message = parse_message(data)
                if not message:
                    continue
                
                msg_type = message.get('type')
                msg_data = message.get('data', {})
                
                # Processa mensagem baseado no tipo
                if msg_type == MSG_TYPES['CREATE_ROOM']:
                    player = self.create_room(client_socket, msg_data)
                    
                elif msg_type == MSG_TYPES['JOIN_ROOM']:
                    player = self.join_room(client_socket, msg_data)
                    
                elif msg_type == MSG_TYPES['START_VOTING']:
                    self.start_voting(client_socket, msg_data)
                    
                elif msg_type == MSG_TYPES['SUBMIT_VOTE']:
                    self.submit_vote(client_socket, msg_data)
                    
                elif msg_type == MSG_TYPES['REVEAL_VOTES']:
                    self.reveal_votes(client_socket)
                    
                elif msg_type == MSG_TYPES['RESET_ROUND']:
                    self.reset_round(client_socket)
                    
        except Exception as e:
            print_error(f"Erro com cliente {address}: {e}")
        finally:
            self.disconnect_client(client_socket)
    
    def create_room(self, client_socket: socket.socket, data: dict) -> Optional[Player]:
        """Cria uma nova sala"""
        with self.lock:
            try:
                player_name = data.get('player_name', 'Jogador')
                room_id = self.generate_room_id()
                player_id = str(uuid.uuid4())[:8]
                
                # Cria jogador e sala
                player = Player(player_id, player_name, client_socket)
                room = Room(room_id, player)
                
                self.rooms[room_id] = room
                self.clients[client_socket] = player
                
                # Envia confirmação
                send_message(client_socket, MSG_TYPES['SUCCESS'], {
                    'room_id': room_id,
                    'player_id': player_id,
                    'message': f'Sala {room_id} criada com sucesso!'
                })
                
                # Envia status da sala
                self.broadcast_room_status(room_id)
                
                print_info(f"Sala {room_id} criada por {player_name}")
                return player
                
            except Exception as e:
                send_message(client_socket, MSG_TYPES['ERROR'], {
                    'message': f'Erro ao criar sala: {e}'
                })
                return None
    
    def join_room(self, client_socket: socket.socket, data: dict) -> Optional[Player]:
        """Adiciona jogador a uma sala existente"""
        with self.lock:
            try:
                room_id = data.get('room_id', '').upper()
                player_name = data.get('player_name', 'Jogador')
                
                if room_id not in self.rooms:
                    send_message(client_socket, MSG_TYPES['ERROR'], {
                        'message': f'Sala {room_id} não encontrada!'
                    })
                    return None
                
                room = self.rooms[room_id]
                player_id = str(uuid.uuid4())[:8]
                player = Player(player_id, player_name, client_socket)
                
                if room.add_player(player):
                    self.clients[client_socket] = player
                    
                    send_message(client_socket, MSG_TYPES['SUCCESS'], {
                        'room_id': room_id,
                        'player_id': player_id,
                        'message': f'Entrou na sala {room_id}!'
                    })
                    
                    self.broadcast_room_status(room_id)
                    print_info(f"{player_name} entrou na sala {room_id}")
                    return player
                else:
                    send_message(client_socket, MSG_TYPES['ERROR'], {
                        'message': 'Erro ao entrar na sala!'
                    })
                    return None
                    
            except Exception as e:
                send_message(client_socket, MSG_TYPES['ERROR'], {
                    'message': f'Erro ao entrar na sala: {e}'
                })
                return None
    
    def start_voting(self, client_socket: socket.socket, data: dict):
        """Inicia uma rodada de votação"""
        with self.lock:
            player = self.clients.get(client_socket)
            if not player:
                return
            
            room = self.find_player_room(player.id)
            if not room:
                send_message(client_socket, MSG_TYPES['ERROR'], {
                    'message': 'Você não está em nenhuma sala!'
                })
                return
            
            # Verifica se é o host
            if player.id != room.host_id:
                send_message(client_socket, MSG_TYPES['ERROR'], {
                    'message': 'Apenas o host pode iniciar a votação!'
                })
                return
            
            story = data.get('story', '')
            if room.start_voting(story):
                self.broadcast_room_status(room.id)
                print_info(f"Votação iniciada na sala {room.id}: {story[:50]}")
            else:
                send_message(client_socket, MSG_TYPES['ERROR'], {
                    'message': 'Votação já está em andamento!'
                })
    
    def submit_vote(self, client_socket: socket.socket, data: dict):
        """Registra o voto de um jogador"""
        with self.lock:
            player = self.clients.get(client_socket)
            if not player:
                return
            
            room = self.find_player_room(player.id)
            if not room:
                return
            
            vote = data.get('vote')
            if room.submit_vote(player.id, vote):
                send_message(client_socket, MSG_TYPES['SUCCESS'], {
                    'message': 'Voto registrado!'
                })
                
                # Se todos votaram, revela automaticamente
                if room.all_voted():
                    room.reveal_votes()
                    print_info(f"Todos votaram na sala {room.id} - revelando votos")
                
                self.broadcast_room_status(room.id)
            else:
                send_message(client_socket, MSG_TYPES['ERROR'], {
                    'message': 'Erro ao registrar voto!'
                })
    
    def reveal_votes(self, client_socket: socket.socket):
        """Revela todos os votos"""
        with self.lock:
            player = self.clients.get(client_socket)
            if not player:
                return
            
            room = self.find_player_room(player.id)
            if not room:
                return
            
            # Verifica se é o host
            if player.id != room.host_id:
                send_message(client_socket, MSG_TYPES['ERROR'], {
                    'message': 'Apenas o host pode revelar os votos!'
                })
                return
            
            if room.reveal_votes():
                self.broadcast_room_status(room.id)
                print_info(f"Votos revelados na sala {room.id}")
            else:
                send_message(client_socket, MSG_TYPES['ERROR'], {
                    'message': 'Nenhuma votação em andamento!'
                })
    
    def reset_round(self, client_socket: socket.socket):
        """Reseta a rodada atual"""
        with self.lock:
            player = self.clients.get(client_socket)
            if not player:
                return
            
            room = self.find_player_room(player.id)
            if not room:
                return
            
            # Verifica se é o host
            if player.id != room.host_id:
                send_message(client_socket, MSG_TYPES['ERROR'], {
                    'message': 'Apenas o host pode resetar a rodada!'
                })
                return
            
            room.reset_round()
            self.broadcast_room_status(room.id)
            print_info(f"Rodada resetada na sala {room.id}")
    
    def broadcast_room_status(self, room_id: str):
        """Envia status da sala para todos os jogadores"""
        if room_id not in self.rooms:
            return
        
        room = self.rooms[room_id]
        status = room.get_status()
        
        # Envia para todos os jogadores da sala
        for player in room.players.values():
            if player.connection:
                try:
                    send_message(player.connection, MSG_TYPES['ROOM_STATUS'], status)
                except:
                    pass
    
    def disconnect_client(self, client_socket: socket.socket):
        """Remove cliente desconectado"""
        with self.lock:
            if client_socket not in self.clients:
                return
            
            player = self.clients[client_socket]
            room = self.find_player_room(player.id)
            
            if room:
                room.remove_player(player.id)
                print_info(f"{player.name} saiu da sala {room.id}")
                
                # Remove sala vazia
                if not room.players:
                    del self.rooms[room.id]
                    print_info(f"Sala {room.id} removida (vazia)")
                else:
                    self.broadcast_room_status(room.id)
            
            del self.clients[client_socket]
            client_socket.close()
    
    def find_player_room(self, player_id: str) -> Optional[Room]:
        """Encontra a sala de um jogador"""
        for room in self.rooms.values():
            if player_id in room.players:
                return room
        return None
    
    def generate_room_id(self) -> str:
        """Gera ID único para sala"""
        import random
        import string
        while True:
            room_id = ''.join(random.choices(string.ascii_uppercase + string.digits, k=6))
            if room_id not in self.rooms:
                return room_id
    
    def print_status(self):
        """Imprime status do servidor periodicamente"""
        import time
        while self.running:
            time.sleep(30)  # A cada 30 segundos
            with self.lock:
                print(f"\n[STATUS] Salas ativas: {len(self.rooms)} | Jogadores online: {len(self.clients)}")
                for room_id, room in self.rooms.items():
                    print(f"  Sala {room_id}: {len(room.players)} jogadores")
    
    def stop(self):
        """Para o servidor"""
        print_info("\nEncerrando servidor...")
        self.running = False
        
        with self.lock:
            # Desconecta todos os clientes
            for client in list(self.clients.keys()):
                client.close()
            
            if self.server_socket:
                self.server_socket.close()
        
        print_success("Servidor encerrado.")


def main():
    """Função principal do servidor"""
    import sys
    
    # Permite especificar porta via linha de comando
    port = DEFAULT_PORT
    if len(sys.argv) > 1:
        try:
            port = int(sys.argv[1])
        except ValueError:
            print_error(f"Porta inválida: {sys.argv[1]}")
            sys.exit(1)
    
    server = PlanningPokerServer(port=port)
    server.start()


if __name__ == "__main__":
    main()