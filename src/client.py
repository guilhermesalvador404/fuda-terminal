"""
Cliente do Planning Poker com suporte a múltiplos idiomas
Interface de terminal para jogadores
"""

import socket
import threading
import json
import time
from typing import Optional

from src.utils.network import (
    DEFAULT_PORT, BUFFER_SIZE,
    MSG_TYPES, parse_message, send_message
)
from src.utils.display import (
    clear_screen, print_header, print_success, print_error, 
    print_info, print_cards, print_room_status, get_input,
    print_menu, print_votes_summary, Fore, Style
)
from src.utils.i18n import t, set_language, save_language_preference, load_language_preference


class PlanningPokerClient:
    def __init__(self):
        self.socket = None
        self.connected = False
        self.room_id = None
        self.player_id = None
        self.player_name = None
        self.room_status = None
        self.is_host = False
        self.running = True
        self.receive_thread = None
        
    def connect(self, host: str, port: int) -> bool:
        """Conecta ao servidor"""
        try:
            self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.socket.connect((host, port))
            self.connected = True
            
            # Inicia thread para receber mensagens
            self.receive_thread = threading.Thread(target=self.receive_messages)
            self.receive_thread.daemon = True
            self.receive_thread.start()
            
            return True
        except Exception as e:
            print_error(t('connection_failed') + f": {e}")
            return False
    
    def receive_messages(self):
        """Recebe mensagens do servidor em background"""
        while self.connected and self.running:
            try:
                data = self.socket.recv(BUFFER_SIZE).decode('utf-8')
                if not data:
                    break
                
                message = parse_message(data)
                if not message:
                    continue
                
                self.handle_server_message(message)
                
            except Exception as e:
                if self.connected:
                    print_error(t('connection_lost') + f": {e}")
                    self.connected = False
                break
    
    def handle_server_message(self, message: dict):
        """Processa mensagem recebida do servidor"""
        msg_type = message.get('type')
        msg_data = message.get('data', {})
        
        if msg_type == MSG_TYPES['SUCCESS']:
            # Atualiza IDs se fornecidos
            if 'room_id' in msg_data:
                self.room_id = msg_data['room_id']
                print(f"[DEBUG] Room ID set to: {self.room_id}")  # Debug
            if 'player_id' in msg_data:
                self.player_id = msg_data['player_id']
                print(f"[DEBUG] Player ID set to: {self.player_id}")  # Debug
            
            # Traduz mensagens do servidor se necessário
            msg_text = msg_data.get('message', t('operation_success'))
            print_success(msg_text)
            
        elif msg_type == MSG_TYPES['ERROR']:
            msg_text = msg_data.get('message', t('error'))
            print_error(msg_text)
            
        elif msg_type == MSG_TYPES['ROOM_STATUS']:
            self.room_status = msg_data
            # Verifica se somos o host
            if self.player_id and msg_data.get('host_id') == self.player_id:
                self.is_host = True
            else:
                self.is_host = False
    
    def create_room(self):
        """Cria uma nova sala"""
        clear_screen()
        print_header(t('create_room_title'))
        
        self.player_name = get_input(t('your_name'))
        if not self.player_name:
            self.player_name = "Player"
        
        send_message(self.socket, MSG_TYPES['CREATE_ROOM'], {
            'player_name': self.player_name
        })
        
        # Aguarda resposta do servidor
        time.sleep(1)  # Aumentado de 0.5 para 1 segundo
        
        if self.room_id:
            print_success(t('room_created', room_id=self.room_id))
            print_info(t('share_code'))
            input(f"\n{t('press_enter')}")
            return True
        else:
            print_error(t('error_creating_room', error='No response from server'))
            input(f"\n{t('press_enter')}")
            return False
    
    def join_room(self):
        """Entra em uma sala existente"""
        clear_screen()
        print_header(t('join_room_title'))
        
        room_code = get_input(t('room_code')).upper()
        if not room_code:
            return False
        
        self.player_name = get_input(t('your_name'))
        if not self.player_name:
            self.player_name = "Player"
        
        send_message(self.socket, MSG_TYPES['JOIN_ROOM'], {
            'room_id': room_code,
            'player_name': self.player_name
        })
        
        # Aguarda resposta do servidor
        time.sleep(1)  # Aumentado de 0.5 para 1 segundo
        
        if self.room_id:
            print_success(t('joined_room', room_id=self.room_id))
            input(f"\n{t('press_enter')}")
            return True
        else:
            print_error(t('room_not_found', room_id=room_code))
            input(f"\n{t('press_enter')}")
            return False
    
    def room_menu(self):
        """Menu principal da sala"""
        while self.connected and self.room_id:
            clear_screen()
            
            # Mostra status da sala
            if self.room_status:
                print_room_status(self.room_status)
                
                # Se há votos revelados, mostra resumo
                if self.room_status.get('votes_revealed'):
                    votes = [p['vote'] for p in self.room_status['players'] if p['vote']]
                    print_votes_summary(votes)
            
            # Opções do menu baseadas no estado e permissões
            print("\n" + "="*50)
            options = []
            
            if self.room_status:
                if not self.room_status.get('is_voting'):
                    if self.is_host:
                        options.append(f"1. {t('start_voting')}")
                elif not self.room_status.get('votes_revealed'):
                    options.append(f"2. {t('vote')}")
                    if self.is_host:
                        options.append(f"3. {t('reveal_votes')}")
                else:
                    if self.is_host:
                        options.append(f"4. {t('new_round')}")
            
            options.append(f"9. {t('leave_room')}")
            options.append("")  # Linha em branco
            options.append(t('refresh_hint'))
            
            for option in options:
                print(option)
            
            # Mudança aqui - sem prompt inline para evitar corte
            print()
            choice = input(f"{Fore.CYAN}{Style.BRIGHT}▶ {Style.RESET_ALL}").strip()
            
            if choice == '1' and self.is_host and not self.room_status.get('is_voting'):
                self.start_voting()
            elif choice == '2' and self.room_status.get('is_voting') and not self.room_status.get('votes_revealed'):
                self.submit_vote()
            elif choice == '3' and self.is_host and self.room_status.get('is_voting'):
                self.reveal_votes()
            elif choice == '4' and self.is_host and self.room_status.get('votes_revealed'):
                self.reset_round()
            elif choice == '9':
                if self.confirm_exit():
                    self.leave_room()
                    break
            
            # Pequena pausa para processar mensagens
            time.sleep(0.1)
    
    def start_voting(self):
        """Inicia uma votação"""
        clear_screen()
        print_header(t('voting_title'))
        
        story = get_input(t('story_prompt'))
        
        send_message(self.socket, MSG_TYPES['START_VOTING'], {
            'story': story
        })
        
        time.sleep(0.5)
    
    def submit_vote(self):
        """Submete um voto"""
        clear_screen()
        print_header(t('vote_title'))
        
        if self.room_status and self.room_status.get('current_story'):
            print(f"{t('story')}: {self.room_status['current_story']}\n")
        
        print_cards()
        
        vote = get_input(f"\n{t('your_vote')}")
        
        # Valida voto
        valid_cards = ['0', '1', '2', '3', '5', '8', '13', '21', '?', '☕']
        if vote not in valid_cards:
            # Tenta mapear entrada alternativa
            if vote.lower() in ['c', 'cafe', 'coffee']:
                vote = '☕'
            elif vote == '??':
                vote = '?'
            else:
                print_error(t('invalid_vote'))
                input(f"\n{t('press_enter')}")
                return
        
        send_message(self.socket, MSG_TYPES['SUBMIT_VOTE'], {
            'vote': vote
        })
        
        time.sleep(0.5)
        print_success(t('vote_registered'))
        input(f"\n{t('press_enter')}")
    
    def reveal_votes(self):
        """Revela os votos"""
        send_message(self.socket, MSG_TYPES['REVEAL_VOTES'], {})
        time.sleep(0.5)
    
    def reset_round(self):
        """Inicia nova rodada"""
        send_message(self.socket, MSG_TYPES['RESET_ROUND'], {})
        time.sleep(0.5)
    
    def leave_room(self):
        """Sai da sala atual"""
        self.room_id = None
        self.room_status = None
        self.is_host = False
        print_info(t('left_room'))
        time.sleep(1)
    
    def confirm_exit(self) -> bool:
        """Confirma saída"""
        response = get_input(t('confirm_exit'))
        # Aceita tanto português quanto inglês
        return response.lower() in ['s', 'sim', 'y', 'yes']
    
    def main_menu(self):
        """Menu principal do cliente"""
        while self.running and self.connected:
            if self.room_id:
                self.room_menu()
            else:
                clear_screen()
                print_header("PLANNING POKER")
                
                # Menu com opção de idioma
                from src.utils.i18n import get_i18n
                current_lang = get_i18n().language
                lang_display = "🇧🇷 PT-BR" if current_lang == 'pt-BR' else "🇺🇸 EN-US"
                
                print(f"  {Fore.CYAN}{Style.BRIGHT}1.{Style.RESET_ALL} {Fore.WHITE}{t('create_room')}{Style.RESET_ALL}")
                print(f"  {Fore.CYAN}{Style.BRIGHT}2.{Style.RESET_ALL} {Fore.WHITE}{t('join_room')}{Style.RESET_ALL}")
                print(f"  {Fore.CYAN}{Style.BRIGHT}3.{Style.RESET_ALL} {Fore.WHITE}{t('change_language')} [{lang_display}]{Style.RESET_ALL}")
                print(f"  {Fore.RED}{Style.BRIGHT}0.{Style.RESET_ALL} {Fore.WHITE}{t('exit')}{Style.RESET_ALL}")
                print()
                
                # Mudança aqui - sem prompt inline para evitar corte
                choice = input(f"{Fore.CYAN}{Style.BRIGHT}▶ {Style.RESET_ALL}").strip()
                
                if choice == '1':
                    self.create_room()
                elif choice == '2':
                    self.join_room()
                elif choice == '3':
                    self.change_language()
                elif choice == '0':
                    if self.confirm_exit():
                        self.running = False
                        break
    
    def change_language(self):
        """Altera o idioma do sistema"""
        from src.utils.i18n import get_i18n, save_language_preference
        
        clear_screen()
        print_header(t('change_language'))
        
        current_lang = get_i18n().language
        print(f"\n{t('current_language')}: {'🇧🇷 Português' if current_lang == 'pt-BR' else '🇺🇸 English'}\n")
        
        print("1. 🇧🇷 Português (BR)")
        print("2. 🇺🇸 English (US)")
        print(f"0. {t('back')}")
        print()
        
        # Mudança aqui também
        choice = input(f"{Fore.CYAN}{Style.BRIGHT}▶ {Style.RESET_ALL}").strip()
        
        if choice == '1':
            set_language('pt-BR')
            save_language_preference('pt-BR')
            print_success(t('language_changed'))
        elif choice == '2':
            set_language('en-US')
            save_language_preference('en-US')
            print_success(t('language_changed'))
        
        if choice in ['1', '2']:
            time.sleep(1)
    
    def disconnect(self):
        """Desconecta do servidor"""
        self.connected = False
        self.running = False
        if self.socket:
            self.socket.close()


def choose_language():
    """Menu para escolher idioma"""
    clear_screen()
    print_header("PLANNING POKER")
    print("\n" + t('choose_language') + "\n")
    print("1. Português (BR)")
    print("2. English (US)")
    print()
    
    choice = input("▶ ").strip()
    
    if choice == '1':
        set_language('pt-BR')
        save_language_preference('pt-BR')
    elif choice == '2':
        set_language('en-US')
        save_language_preference('en-US')
    else:
        # Padrão
        set_language('pt-BR')
        save_language_preference('pt-BR')


def main():
    """Função principal do cliente"""
    # Carrega preferência de idioma ou pergunta
    saved_lang = load_language_preference()
    if saved_lang in ['pt-BR', 'en-US']:
        set_language(saved_lang)
    else:
        choose_language()
    
    clear_screen()
    print_header(t('client_title'))
    
    # Pede informações de conexão
    from src.utils.i18n import get_i18n
    lang = get_i18n().language
    
    if lang == 'en-US':
        print_info("Leave blank for defaults\n")
    else:
        print_info("Deixe em branco para usar valores padrão\n")
    
    host = get_input(t('server_prompt'))
    if not host:
        host = "localhost"
    
    port_str = get_input(t('port_prompt', port=DEFAULT_PORT))
    try:
        port = int(port_str) if port_str else DEFAULT_PORT
    except ValueError:
        if lang == 'en-US':
            print_error("Invalid port! Using default.")
        else:
            print_error("Porta inválida! Usando padrão.")
        port = DEFAULT_PORT
    
    # Conecta ao servidor
    client = PlanningPokerClient()
    
    print_info(t('connecting', host=host, port=port))
    
    if client.connect(host, port):
        print_success(t('connected'))
        time.sleep(1)
        
        try:
            client.main_menu()
        except KeyboardInterrupt:
            pass
        finally:
            client.disconnect()
            print_info(t('goodbye'))
            print(t('thanks'))
    else:
        print_error(t('connection_failed'))
        print_info(t('check_server'))


if __name__ == "__main__":
    main()