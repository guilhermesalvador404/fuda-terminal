"""
Script para iniciar o servidor do Planning Poker
"""
import sys
from src.server import main

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\nServidor encerrado.")
        sys.exit(0)