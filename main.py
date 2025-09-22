"""
Arquivo principal da aplicação
Sistema de Gerenciamento de Livraria - Versão MVC
"""
import sys
from pathlib import Path

# Adicionar o diretório raiz ao path para imports
current_dir = Path(__file__).parent
sys.path.append(str(current_dir))

from controllers.livraria_controller import LivrariaController

def main():
    """Função principal que inicia a aplicação"""
    try:
        # Criar e executar o controller principal
        controller = LivrariaController()
        controller.executar()
        
    except KeyboardInterrupt:
        print("\n\n🛑 Aplicação interrompida pelo usuário.")
        
    except Exception as e:
        print(f"\n💥 Erro crítico na aplicação: {e}")
        print("🔧 Verifique se todas as dependências estão instaladas.")
        
    finally:
        print("👋 Sistema finalizado.")

if __name__ == "__main__":
    main()