from typing import Dict, Optional
from .player import Player

class Room:
    # Cartas disponíveis no Planning Poker
    VALID_CARDS = ['0', '1', '2', '3', '5', '8', '13', '21', '?', '☕']
    
    def __init__(self, room_id: str, host_player: Player):
        self.id = room_id
        self.players: Dict[str, Player] = {}
        self.host_id = host_player.id
        self.is_voting = False
        self.votes_revealed = False
        self.current_story = ""
        
        # Adiciona o host como primeiro jogador
        host_player.is_host = True
        self.players[host_player.id] = host_player
    
    def add_player(self, player: Player) -> bool:
        """Adiciona um jogador à sala"""
        if player.id not in self.players:
            self.players[player.id] = player
            return True
        return False
    
    def remove_player(self, player_id: str) -> bool:
        """Remove um jogador da sala"""
        if player_id in self.players:
            del self.players[player_id]
            
            # Se o host saiu, transfere para outro jogador
            if player_id == self.host_id and self.players:
                new_host = next(iter(self.players.values()))
                new_host.is_host = True
                self.host_id = new_host.id
            
            return True
        return False
    
    def start_voting(self, story: str = "") -> bool:
        """Inicia uma nova rodada de votação"""
        if not self.is_voting:
            self.is_voting = True
            self.votes_revealed = False
            self.current_story = story
            
            # Reseta votos de todos os jogadores
            for player in self.players.values():
                player.reset_vote()
            
            return True
        return False
    
    def submit_vote(self, player_id: str, vote: str) -> bool:
        """Registra o voto de um jogador"""
        if (player_id in self.players and 
            self.is_voting and 
            not self.votes_revealed and
            vote in self.VALID_CARDS):
            
            self.players[player_id].current_vote = vote
            return True
        return False
    
    def all_voted(self) -> bool:
        """Verifica se todos votaram"""
        if not self.players:
            return False
        return all(p.current_vote is not None for p in self.players.values())
    
    def reveal_votes(self) -> bool:
        """Revela todos os votos"""
        if self.is_voting:
            self.votes_revealed = True
            return True
        return False
    
    def reset_round(self):
        """Reseta a rodada atual"""
        self.is_voting = False
        self.votes_revealed = False
        self.current_story = ""
        for player in self.players.values():
            player.reset_vote()
    
    def get_status(self) -> dict:
        """Retorna o status atual da sala"""
        return {
            'room_id': self.id,
            'host_id': self.host_id,
            'is_voting': self.is_voting,
            'votes_revealed': self.votes_revealed,
            'current_story': self.current_story,
            'players': [p.to_dict() for p in self.players.values()],
            'all_voted': self.all_voted()
        }