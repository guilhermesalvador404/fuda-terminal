"""
Script para iniciar o cliente do Planning Poker
"""
import sys
from src.client import main

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\nCliente encerrado.")
        sys.exit(0)