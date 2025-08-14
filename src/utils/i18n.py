"""
Sistema de internacionalização para Planning Poker
Suporta Português (pt-BR) e Inglês (en-US)
"""

import json
import os

class I18n:
    """Gerenciador de traduções"""
    
    def __init__(self, language='pt-BR'):
        self.language = language
        self.translations = {
            'pt-BR': {
                # Mensagens gerais
                'welcome': 'BEM-VINDO AO PLANNING POKER',
                'server_title': 'PLANNING POKER - SERVIDOR',
                'client_title': 'PLANNING POKER - CLIENTE',
                'choose_language': 'Escolha o idioma / Choose language',
                
                # Menu principal
                'main_menu': 'Menu Principal',
                'create_room': 'Criar sala',
                'join_room': 'Entrar em sala',
                'exit': 'Sair',
                'choose': 'escolha',
                'change_language': 'Alterar idioma',
                'current_language': 'Idioma atual',
                'language_changed': 'Idioma alterado com sucesso!',
                'back': 'Voltar',
                
                # Conexão
                'server_prompt': 'Servidor (padrão: localhost)',
                'port_prompt': 'Porta (padrão: {port})',
                'connecting': 'Conectando a {host}:{port}...',
                'connected': 'Conectado ao servidor!',
                'connection_failed': 'Não foi possível conectar ao servidor',
                'connection_lost': 'Conexão perdida!',
                'check_server': 'Verifique se o servidor está rodando',
                
                # Servidor
                'server_running': 'Servidor rodando em {host}:{port}',
                'stop_server': 'Pressione Ctrl+C para parar o servidor',
                'new_connection': 'Nova conexão de {address}',
                'server_stopping': 'Encerrando servidor...',
                'server_stopped': 'Servidor encerrado.',
                
                # Criação de sala
                'create_room_title': 'CRIAR SALA',
                'your_name': 'Seu nome',
                'room_created': 'Sala criada! Código: {room_id}',
                'share_code': 'Compartilhe este código com sua equipe',
                'room_removed': 'Sala {room_id} removida (vazia)',
                
                # Entrada em sala
                'join_room_title': 'ENTRAR NA SALA',
                'room_code': 'Código da sala',
                'joined_room': 'Você entrou na sala {room_id}!',
                'room_not_found': 'Sala {room_id} não encontrada!',
                'player_joined': '{name} entrou na sala {room_id}',
                'player_left': '{name} saiu da sala {room_id}',
                
                # Status da sala
                'room': 'Sala',
                'story': 'História',
                'none': 'Nenhuma',
                'status': 'Status',
                'waiting': 'Aguardando',
                'voting_progress': 'Votação em Andamento',
                'votes_revealed': 'Votos Revelados',
                'players': 'Jogadores',
                'all_voted': 'Todos votaram! Host pode revelar os votos.',
                
                # Votação
                'start_voting': 'Iniciar votação',
                'vote': 'Votar',
                'reveal_votes': 'Revelar votos',
                'new_round': 'Nova rodada',
                'reset_round': 'Resetar rodada',
                'voting_title': 'INICIAR VOTAÇÃO',
                'story_prompt': 'Descrição da história/tarefa (ou ENTER para pular)',
                'vote_title': 'VOTAR',
                'your_vote': 'Seu voto',
                'vote_registered': 'Voto registrado!',
                'invalid_vote': 'Voto inválido!',
                'voting_started': 'Votação iniciada na sala {room_id}: {story}',
                'votes_revealed_msg': 'Votos revelados na sala {room_id}',
                'round_reset': 'Rodada resetada na sala {room_id}',
                
                # Permissões
                'host_only_start': 'Apenas o host pode iniciar a votação!',
                'host_only_reveal': 'Apenas o host pode revelar os votos!',
                'host_only_reset': 'Apenas o host pode resetar a rodada!',
                'already_voting': 'Votação já está em andamento!',
                'no_voting': 'Nenhuma votação em andamento!',
                'not_in_room': 'Você não está em nenhuma sala!',
                
                # Cartas
                'available_cards': 'Cartas disponíveis',
                
                # Estatísticas
                'votes_summary': 'Resumo dos Votos',
                'statistics': 'Estatísticas',
                'average': 'Média',
                'minimum': 'Mínimo',
                'maximum': 'Máximo',
                'range': 'Amplitude',
                'consensus_analysis': 'Análise de Consenso',
                'total_consensus': 'Consenso TOTAL! Todos votaram igual!',
                'close_consensus': 'Consenso muito próximo!',
                'reasonable_consensus': 'Consenso razoável.',
                'moderate_divergence': 'Divergência moderada - considere discutir.',
                'high_divergence': 'Grande divergência! Recomenda-se mais discussão.',
                'special_votes': 'Votos especiais',
                'uncertainty': 'Incerteza/Necessita esclarecimento',
                'coffee_break': 'Pausa para café necessária!',
                'no_votes': 'Nenhum voto registrado ainda.',
                
                # Interface
                'leave_room': 'Sair da sala',
                'refresh_hint': '💡 Pressione ENTER para atualizar a tela',
                'press_enter': 'Pressione ENTER para continuar...',
                'confirm_exit': 'Tem certeza que deseja sair? (s/n)',
                'left_room': 'Você saiu da sala',
                'goodbye': '👋 Até a próxima sprint!',
                'thanks': 'Obrigado por usar o Planning Poker Terminal.',
                
                # Erros
                'error': 'Erro',
                'error_creating_room': 'Erro ao criar sala: {error}',
                'error_joining_room': 'Erro ao entrar na sala: {error}',
                'error_voting': 'Erro ao registrar voto!',
                'operation_success': 'Operação realizada com sucesso!',
                
                # Status do servidor
                'status_header': '[STATUS] Salas ativas: {rooms} | Jogadores online: {players}',
                'room_status': 'Sala {room_id}: {count} jogadores',
            },
            
            'en-US': {
                # General messages
                'welcome': 'WELCOME TO PLANNING POKER',
                'server_title': 'PLANNING POKER - SERVER',
                'client_title': 'PLANNING POKER - CLIENT',
                'choose_language': 'Choose language / Escolha o idioma',
                
                # Main menu
                'main_menu': 'Main Menu',
                'create_room': 'Create room',
                'join_room': 'Join room',
                'exit': 'Exit',
                'choose': 'choose',
                'change_language': 'Change language',
                'current_language': 'Current language',
                'language_changed': 'Language changed successfully!',
                'back': 'Back',
                
                # Connection
                'server_prompt': 'Server (default: localhost)',
                'port_prompt': 'Port (default: {port})',
                'connecting': 'Connecting to {host}:{port}...',
                'connected': 'Connected to server!',
                'connection_failed': 'Could not connect to server',
                'connection_lost': 'Connection lost!',
                'check_server': 'Check if the server is running',
                
                # Server
                'server_running': 'Server running on {host}:{port}',
                'stop_server': 'Press Ctrl+C to stop the server',
                'new_connection': 'New connection from {address}',
                'server_stopping': 'Shutting down server...',
                'server_stopped': 'Server stopped.',
                
                # Room creation
                'create_room_title': 'CREATE ROOM',
                'your_name': 'Your name',
                'room_created': 'Room created! Code: {room_id}',
                'share_code': 'Share this code with your team',
                'room_removed': 'Room {room_id} removed (empty)',
                
                # Room joining
                'join_room_title': 'JOIN ROOM',
                'room_code': 'Room code',
                'joined_room': 'You joined room {room_id}!',
                'room_not_found': 'Room {room_id} not found!',
                'player_joined': '{name} joined room {room_id}',
                'player_left': '{name} left room {room_id}',
                
                # Room status
                'room': 'Room',
                'story': 'Story',
                'none': 'None',
                'status': 'Status',
                'waiting': 'Waiting',
                'voting_progress': 'Voting in Progress',
                'votes_revealed': 'Votes Revealed',
                'players': 'Players',
                'all_voted': 'Everyone voted! Host can reveal votes.',
                
                # Voting
                'start_voting': 'Start voting',
                'vote': 'Vote',
                'reveal_votes': 'Reveal votes',
                'new_round': 'New round',
                'reset_round': 'Reset round',
                'voting_title': 'START VOTING',
                'story_prompt': 'Story/task description (or ENTER to skip)',
                'vote_title': 'VOTE',
                'your_vote': 'Your vote',
                'vote_registered': 'Vote registered!',
                'invalid_vote': 'Invalid vote!',
                'voting_started': 'Voting started in room {room_id}: {story}',
                'votes_revealed_msg': 'Votes revealed in room {room_id}',
                'round_reset': 'Round reset in room {room_id}',
                
                # Permissions
                'host_only_start': 'Only the host can start voting!',
                'host_only_reveal': 'Only the host can reveal votes!',
                'host_only_reset': 'Only the host can reset the round!',
                'already_voting': 'Voting already in progress!',
                'no_voting': 'No voting in progress!',
                'not_in_room': 'You are not in any room!',
                
                # Cards
                'available_cards': 'Available cards',
                
                # Statistics
                'votes_summary': 'Votes Summary',
                'statistics': 'Statistics',
                'average': 'Average',
                'minimum': 'Minimum',
                'maximum': 'Maximum',
                'range': 'Range',
                'consensus_analysis': 'Consensus Analysis',
                'total_consensus': 'TOTAL consensus! Everyone voted the same!',
                'close_consensus': 'Very close consensus!',
                'reasonable_consensus': 'Reasonable consensus.',
                'moderate_divergence': 'Moderate divergence - consider discussing.',
                'high_divergence': 'High divergence! More discussion recommended.',
                'special_votes': 'Special votes',
                'uncertainty': 'Uncertainty/Needs clarification',
                'coffee_break': 'Coffee break needed!',
                'no_votes': 'No votes registered yet.',
                
                # Interface
                'leave_room': 'Leave room',
                'refresh_hint': '💡 Press ENTER to refresh screen',
                'press_enter': 'Press ENTER to continue...',
                'confirm_exit': 'Are you sure you want to exit? (y/n)',
                'left_room': 'You left the room',
                'goodbye': '👋 See you next sprint!',
                'thanks': 'Thank you for using Planning Poker Terminal.',
                
                # Errors
                'error': 'Error',
                'error_creating_room': 'Error creating room: {error}',
                'error_joining_room': 'Error joining room: {error}',
                'error_voting': 'Error registering vote!',
                'operation_success': 'Operation completed successfully!',
                
                # Server status
                'status_header': '[STATUS] Active rooms: {rooms} | Online players: {players}',
                'room_status': 'Room {room_id}: {count} players',
            }
        }
    
    def set_language(self, language):
        """Define o idioma atual"""
        if language in self.translations:
            self.language = language
            return True
        return False
    
    def get(self, key, **kwargs):
        """Obtém uma tradução com parâmetros opcionais"""
        text = self.translations[self.language].get(key, key)
        if kwargs:
            return text.format(**kwargs)
        return text
    
    def __call__(self, key, **kwargs):
        """Permite usar i18n('key') diretamente"""
        return self.get(key, **kwargs)

# Instância global
_i18n = None

def get_i18n():
    """Retorna a instância global de i18n"""
    global _i18n
    if _i18n is None:
        _i18n = I18n()
    return _i18n

def set_language(language):
    """Define o idioma globalmente"""
    return get_i18n().set_language(language)

def t(key, **kwargs):
    """Função de tradução rápida"""
    return get_i18n().get(key, **kwargs)

def save_language_preference(language):
    """Salva a preferência de idioma em arquivo"""
    try:
        with open('.language_preference', 'w') as f:
            f.write(language)
    except:
        pass

def load_language_preference():
    """Carrega a preferência de idioma do arquivo"""
    try:
        with open('.language_preference', 'r') as f:
            return f.read().strip()
    except:
        return 'pt-BR'  # Padrão