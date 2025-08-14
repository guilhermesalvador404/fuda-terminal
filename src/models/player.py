class Player:
    def __init__(self, player_id, name, connection=None):
        self.id = player_id
        self.name = name
        self.connection = connection
        self.current_vote = None
        self.is_host = False
    
    def reset_vote(self):
        """Reseta o voto do jogador para uma nova rodada"""
        self.current_vote = None
    
    def to_dict(self):
        """Converte o jogador para dicionário (sem incluir connection)"""
        return {
            'id': self.id,
            'name': self.name,
            'has_voted': self.current_vote is not None,
            'vote': self.current_vote,
            'is_host': self.is_host
        }