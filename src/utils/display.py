import os
import platform
from colorama import init, Fore, Style, Back

# Inicializa colorama para funcionar no Windows também
init(autoreset=True)

def clear_screen():
    """Limpa a tela do terminal (cross-platform)"""
    if platform.system() == 'Windows':
        os.system('cls')
    else:
        os.system('clear')

def print_header(text):
    """Imprime um cabeçalho destacado"""
    print(f"\n{Fore.CYAN}{Style.BRIGHT}{'='*50}")
    print(f"{text:^50}")
    print(f"{'='*50}{Style.RESET_ALL}\n")

def print_success(text):
    """Imprime mensagem de sucesso"""
    print(f"{Fore.GREEN}{Style.BRIGHT}✓ {text}{Style.RESET_ALL}")

def print_error(text):
    """Imprime mensagem de erro"""
    print(f"{Fore.RED}{Style.BRIGHT}✗ {text}{Style.RESET_ALL}")

def print_info(text):
    """Imprime mensagem informativa"""
    print(f"{Fore.YELLOW}ℹ {text}{Style.RESET_ALL}")

def print_cards():
    """Exibe as cartas disponíveis com cores"""
    cards = ['0', '1', '2', '3', '5', '8', '13', '21', '?', '☕']
    
    print(f"\n{Fore.CYAN}{Style.BRIGHT}Cartas disponíveis:{Style.RESET_ALL}")
    print(f"{Fore.WHITE}┌────┬────┬────┬────┬────┬────┬────┬────┬────┬────┐")
    print(f"{Fore.WHITE}│", end="")
    
    for card in cards:
        # Cores diferentes para tipos de cartas
        if card == '?':
            color = Fore.MAGENTA
        elif card == '☕':
            color = Fore.YELLOW
        elif card in ['0', '1', '2', '3']:
            color = Fore.GREEN
        elif card in ['5', '8']:
            color = Fore.YELLOW
        else:  # 13, 21
            color = Fore.RED
        
        print(f"{color} {card:^2} {Fore.WHITE}│", end="")
    
    print(f"\n{Fore.WHITE}└────┴────┴────┴────┴────┴────┴────┴────┴────┴────┘{Style.RESET_ALL}")

def print_room_status(status):
    """Exibe o status da sala com cores e formatação"""
    # Cabeçalho da sala
    print(f"\n{Fore.CYAN}{Style.BRIGHT}╔{'═'*48}╗")
    print(f"║ Sala: {status['room_id']:^40} ║")
    print(f"╚{'═'*48}╝{Style.RESET_ALL}")
    
    # História/Task
    story = status.get('current_story', '')
    if story:
        print(f"{Fore.WHITE}📋 História: {Fore.YELLOW}{story}{Style.RESET_ALL}")
    else:
        print(f"{Fore.WHITE}📋 História: {Style.DIM}Nenhuma{Style.RESET_ALL}")
    
    # Status da votação
    if status['is_voting']:
        if status['votes_revealed']:
            status_text = f"{Fore.GREEN}Votos Revelados"
        else:
            status_text = f"{Fore.YELLOW}Votação em Andamento"
    else:
        status_text = f"{Style.DIM}Aguardando{Style.NORMAL}"
    
    print(f"{Fore.WHITE}📊 Status: {status_text}{Style.RESET_ALL}")
    
    # Lista de jogadores
    print(f"\n{Fore.CYAN}{Style.BRIGHT}Jogadores:{Style.RESET_ALL}")
    print(f"{Fore.WHITE}{'─'*30}{Style.RESET_ALL}")
    
    for player in status['players']:
        # Indicadores
        host_marker = f" {Fore.YELLOW}👑{Style.RESET_ALL}" if player['is_host'] else ""
        
        # Status do voto
        if player['has_voted']:
            vote_status = f"{Fore.GREEN}●{Style.RESET_ALL}"
        else:
            vote_status = f"{Fore.RED}○{Style.RESET_ALL}"
        
        # Nome do jogador
        name_display = f"{Fore.WHITE}{player['name']}{Style.RESET_ALL}"
        
        # Mostra voto se revelado
        if status['votes_revealed'] and player['vote']:
            # Cor do voto baseado no valor
            if player['vote'] in ['0', '1', '2', '3']:
                vote_color = Fore.GREEN
            elif player['vote'] in ['5', '8']:
                vote_color = Fore.YELLOW
            elif player['vote'] in ['13', '21']:
                vote_color = Fore.RED
            elif player['vote'] == '?':
                vote_color = Fore.MAGENTA
            else:  # ☕
                vote_color = Fore.CYAN
            
            print(f"  {vote_status} {name_display}{host_marker}: {vote_color}{Style.BRIGHT}[{player['vote']}]{Style.RESET_ALL}")
        else:
            print(f"  {vote_status} {name_display}{host_marker}")
    
    # Indicador se todos votaram
    if status.get('all_voted') and not status['votes_revealed']:
        print(f"\n{Fore.GREEN}{Style.BRIGHT}✓ Todos votaram! Host pode revelar os votos.{Style.RESET_ALL}")

def get_input(prompt):
    """Obtém input do usuário com formatação colorida"""
    return input(f"{Fore.CYAN}{Style.BRIGHT}▶ {prompt}: {Style.RESET_ALL}").strip()

def print_menu(title, options):
    """Exibe um menu de opções com cores"""
    print_header(title)
    for i, option in enumerate(options, 1):
        print(f"  {Fore.CYAN}{Style.BRIGHT}{i}.{Style.RESET_ALL} {Fore.WHITE}{option}{Style.RESET_ALL}")
    print(f"  {Fore.RED}{Style.BRIGHT}0.{Style.RESET_ALL} {Fore.WHITE}Voltar/Sair{Style.RESET_ALL}")
    print()

def print_votes_summary(votes):
    """Exibe um resumo dos votos com gráfico colorido"""
    if not votes:
        print_info("Nenhum voto registrado ainda.")
        return
    
    # Conta ocorrências de cada voto
    vote_count = {}
    for vote in votes:
        if vote in vote_count:
            vote_count[vote] += 1
        else:
            vote_count[vote] = 1
    
    print(f"\n{Fore.CYAN}{Style.BRIGHT}📊 Resumo dos Votos:{Style.RESET_ALL}")
    print(f"{Fore.WHITE}{'─' * 35}{Style.RESET_ALL}")
    
    # Ordena por valor do voto (exceto especiais)
    sorted_votes = sorted(vote_count.items(), key=lambda x: (
        x[0] not in ['?', '☕'],  # Especiais por último
        float(x[0]) if x[0].isdigit() else float('inf')
    ))
    
    # Encontra o máximo para escalar o gráfico
    max_count = max(vote_count.values()) if vote_count else 1
    
    for vote, count in sorted_votes:
        # Cor baseada no valor
        if vote in ['0', '1', '2', '3']:
            color = Fore.GREEN
        elif vote in ['5', '8']:
            color = Fore.YELLOW
        elif vote in ['13', '21']:
            color = Fore.RED
        elif vote == '?':
            color = Fore.MAGENTA
        else:  # ☕
            color = Fore.CYAN
        
        # Barra proporcional
        bar_length = int((count / max_count) * 20)
        bar = "█" * bar_length + "░" * (20 - bar_length)
        
        print(f"  {color}{vote:>3}{Style.RESET_ALL}: {color}{bar}{Style.RESET_ALL} {Fore.WHITE}({count}){Style.RESET_ALL}")
    
    # Estatísticas
    print(f"\n{Fore.CYAN}{Style.BRIGHT}📈 Estatísticas:{Style.RESET_ALL}")
    print(f"{Fore.WHITE}{'─' * 35}{Style.RESET_ALL}")
    
    # Calcula métricas apenas para votos numéricos
    numeric_votes = [int(v) for v in votes if v.isdigit()]
    
    if numeric_votes:
        avg = sum(numeric_votes) / len(numeric_votes)
        min_vote = min(numeric_votes)
        max_vote = max(numeric_votes)
        
        print(f"  {Fore.WHITE}Média: {Fore.YELLOW}{avg:.1f}{Style.RESET_ALL}")
        print(f"  {Fore.WHITE}Mínimo: {Fore.GREEN}{min_vote}{Style.RESET_ALL}")
        print(f"  {Fore.WHITE}Máximo: {Fore.RED}{max_vote}{Style.RESET_ALL}")
        print(f"  {Fore.WHITE}Amplitude: {Fore.MAGENTA}{max_vote - min_vote}{Style.RESET_ALL}")
        
        # Análise de consenso
        print(f"\n{Fore.CYAN}{Style.BRIGHT}🎯 Análise de Consenso:{Style.RESET_ALL}")
        
        if len(set(numeric_votes)) == 1:
            print(f"  {Fore.GREEN}{Style.BRIGHT}✓ Consenso TOTAL! Todos votaram igual!{Style.RESET_ALL}")
        elif max_vote - min_vote <= 1:
            print(f"  {Fore.GREEN}✓ Consenso muito próximo!{Style.RESET_ALL}")
        elif max_vote - min_vote <= 3:
            print(f"  {Fore.YELLOW}~ Consenso razoável.{Style.RESET_ALL}")
        elif max_vote - min_vote <= 8:
            print(f"  {Fore.YELLOW}⚠ Divergência moderada - considere discutir.{Style.RESET_ALL}")
        else:
            print(f"  {Fore.RED}⚠ Grande divergência! Recomenda-se mais discussão.{Style.RESET_ALL}")
    
    # Contagem de votos especiais
    special_votes = [v for v in votes if v in ['?', '☕']]
    if special_votes:
        print(f"\n{Fore.MAGENTA}Votos especiais: {len(special_votes)}{Style.RESET_ALL}")
        if '?' in special_votes:
            print(f"  {Fore.MAGENTA}? = Incerteza/Necessita esclarecimento{Style.RESET_ALL}")
        if '☕' in special_votes:
            print(f"  {Fore.CYAN}☕ = Pausa para café necessária!{Style.RESET_ALL}")

def print_welcome():
    """Tela de boas-vindas animada"""
    clear_screen()
    print(f"\n{Fore.CYAN}{Style.BRIGHT}")
    print(r"""
    ╔═══════════════════════════════════════════════╗
    ║                                               ║
    ║   🎯  PLANNING POKER - FUDA TERMINAL  🎯      ║
    ║                                               ║
    ║          BY: Guilherme Salvador               ║
    ║                                               ║
    ╚═══════════════════════════════════════════════╝
    """)
    print(f"{Style.RESET_ALL}")

def print_goodbye():
    """Mensagem de despedida"""
    print(f"\n{Fore.CYAN}{Style.BRIGHT}👋 Até a próxima sprint!{Style.RESET_ALL}")
    print(f"{Fore.WHITE}Obrigado por usar o Planning Poker Terminal.{Style.RESET_ALL}\n")