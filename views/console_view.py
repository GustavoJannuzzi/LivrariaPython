"""
View para interface de console
Responsável pela apresentação e interação com o usuário via console
"""
import os
from typing import List, Optional
from pathlib import Path

from models.livro import Livro

class ConsoleView:
    """Interface de console para o sistema de livraria"""
    
    def __init__(self):
        self.largura_console = 80
    
    def limpar_tela(self):
        """Limpa a tela do console"""
        os.system('cls' if os.name == 'nt' else 'clear')
    
    def exibir_cabecalho(self, titulo: str):
        """Exibe um cabeçalho formatado"""
        print("\n" + "="*self.largura_console)
        print(f"    {titulo.upper()}")
        print("="*self.largura_console)
    
    def exibir_linha_separadora(self):
        """Exibe uma linha separadora"""
        print("-"*self.largura_console)
    
    def exibir_menu_principal(self):
        """Exibe o menu principal do sistema"""
        self.exibir_cabecalho("SISTEMA DE GERENCIAMENTO DE LIVRARIA")
        opcoes = [
            "1. Adicionar novo livro",
            "2. Exibir todos os livros",
            "3. Atualizar preço de um livro",
            "4. Remover um livro",
            "5. Buscar livros por autor",
            "6. Buscar livros por título",
            "7. Busca avançada",
            "8. Exportar dados para CSV",
            "9. Importar dados de CSV",
            "10. Fazer backup do banco de dados",
            "11. Restaurar backup",
            "12. Ver estatísticas",
            "13. Gerar relatório completo",
            "14. Sair"
        ]
        
        for opcao in opcoes:
            print(opcao)
        self.exibir_linha_separadora()
    
    def solicitar_opcao_menu(self) -> str:
        """Solicita a opção do menu ao usuário"""
        return input("Escolha uma opção (1-14): ").strip()
    
    def exibir_submenu(self, titulo: str):
        """Exibe um submenu"""
        print(f"\n--- {titulo} ---")
    
    def solicitar_dados_livro(self) -> dict:
        """Solicita os dados de um livro ao usuário"""
        self.exibir_submenu("DADOS DO LIVRO")
        
        titulo = input("Título: ").strip()
        autor = input("Autor: ").strip()
        ano = input("Ano de publicação: ").strip()
        preco = input("Preço (R$): ").strip()
        
        return {
            'titulo': titulo,
            'autor': autor,
            'ano': ano,
            'preco': preco
        }
    
    def solicitar_id_livro(self, mensagem: str = "ID do livro") -> str:
        """Solicita um ID de livro ao usuário"""
        return input(f"{mensagem}: ").strip()
    
    def solicitar_novo_preco(self) -> str:
        """Solicita um novo preço ao usuário"""
        return input("Novo preço (R$): ").strip()
    
    def solicitar_texto(self, mensagem: str) -> str:
        """Solicita um texto ao usuário"""
        return input(f"{mensagem}: ").strip()
    
    def solicitar_confirmacao(self, mensagem: str) -> bool:
        """Solicita confirmação do usuário"""
        resposta = input(f"{mensagem} (s/N): ").strip().lower()
        return resposta == 's'
    
    def exibir_livros(self, livros: List[Livro], titulo: str = "LIVROS"):
        """Exibe uma lista de livros formatada"""
        if not livros:
            print(f"\n{titulo}: Nenhum livro encontrado.")
            return
        
        self.exibir_submenu(f"{titulo} ({len(livros)} encontrados)")
        
        # Cabeçalho da tabela
        print(f"{'ID':<5} {'Título':<35} {'Autor':<25} {'Ano':<6} {'Preço':<10}")
        self.exibir_linha_separadora()
        
        # Dados dos livros
        for livro in livros:
            titulo_truncado = livro.titulo[:34] + "..." if len(livro.titulo) > 34 else livro.titulo
            autor_truncado = livro.autor[:24] + "..." if len(livro.autor) > 24 else livro.autor
            
            print(f"{livro.id or 'N/A':<5} {titulo_truncado:<35} {autor_truncado:<25} "
                  f"{livro.ano_publicacao:<6} R${livro.preco:<9.2f}")
    
    def exibir_livro_detalhado(self, livro: Livro):
        """Exibe detalhes completos de um livro"""
        self.exibir_submenu("DETALHES DO LIVRO")
        print(f"ID: {livro.id}")
        print(f"Título: {livro.titulo}")
        print(f"Autor: {livro.autor}")
        print(f"Ano de Publicação: {livro.ano_publicacao}")
        print(f"Preço: R$ {livro.preco:.2f}")
    
    def exibir_arquivos_csv(self, arquivos: List[Path]):
        """Exibe lista de arquivos CSV disponíveis"""
        if not arquivos:
            print("Nenhum arquivo CSV encontrado no diretório exports/")
            return
        
        self.exibir_submenu("ARQUIVOS CSV DISPONÍVEIS")
        for i, arquivo in enumerate(arquivos, 1):
            stat = arquivo.stat()
            tamanho_kb = stat.st_size / 1024
            print(f"{i}. {arquivo.name} ({tamanho_kb:.1f} KB)")
    
    def solicitar_escolha_arquivo(self, max_opcoes: int) -> str:
        """Solicita escolha de arquivo ao usuário"""
        return input(f"Escolha um arquivo (1-{max_opcoes}) ou digite o nome: ").strip()
    
    def exibir_backups(self, backups: List[dict]):
        """Exibe lista de backups disponíveis"""
        if not backups:
            print("Nenhum backup encontrado.")
            return
        
        self.exibir_submenu(f"BACKUPS DISPONÍVEIS ({len(backups)} encontrados)")
        print(f"{'#':<3} {'Nome do Arquivo':<35} {'Data/Hora':<20} {'Tamanho':<10}")
        self.exibir_linha_separadora()
        
        for i, backup in enumerate(backups, 1):
            nome = backup['nome'][:34] + "..." if len(backup['nome']) > 34 else backup['nome']
            tamanho_kb = backup['tamanho'] / 1024
            
            print(f"{i:<3} {nome:<35} {backup['data_criacao_str']:<20} {tamanho_kb:.1f} KB")
    
    def exibir_estatisticas(self, stats: dict):
        """Exibe estatísticas do sistema"""
        self.exibir_submenu("ESTATÍSTICAS DO SISTEMA")
        
        print(f"Total de livros: {stats['total_livros']}")
        
        if stats['total_livros'] > 0:
            print(f"Preço médio: R$ {stats['preco_medio']:.2f}")
            print(f"Livro mais caro: R$ {stats['preco_maximo']:.2f}")
            print(f"Livro mais barato: R$ {stats['preco_minimo']:.2f}")
            print(f"Ano mais antigo: {stats['ano_mais_antigo']}")
            print(f"Ano mais recente: {stats['ano_mais_recente']}")
        
        print(f"Total de backups: {stats['total_backups']}")
        print(f"Último backup: {stats['ultimo_backup']}")
    
    def exibir_relatorio_completo(self, relatorio: dict):
        """Exibe relatório completo do sistema"""
        self.exibir_submenu("RELATÓRIO COMPLETO DO SISTEMA")
        
        # Estatísticas gerais
        print("\n📊 ESTATÍSTICAS GERAIS:")
        stats = relatorio['estatisticas_gerais']
        print(f"   • Total de livros: {stats['total_livros']}")
        
        if stats['total_livros'] > 0:
            print(f"   • Preço médio: R$ {stats['preco_medio']:.2f}")
            print(f"   • Faixa de preços: R$ {stats['preco_minimo']:.2f} - R$ {stats['preco_maximo']:.2f}")
            print(f"   • Período: {stats['ano_mais_antigo']} - {stats['ano_mais_recente']}")
        
        # Top autores
        print("\n👥 TOP 5 AUTORES (por quantidade):")
        autores_ordenados = sorted(relatorio['por_autor'].items(), 
                                 key=lambda x: x[1]['quantidade'], reverse=True)[:5]
        
        for autor, dados in autores_ordenados:
            print(f"   • {autor}: {dados['quantidade']} livros (R$ {dados['preco_total']:.2f})")
        
        # Livros mais caros
        print("\n💰 TOP 5 LIVROS MAIS CAROS:")
        for livro in relatorio['livros_mais_caros']:
            print(f"   • {livro.titulo} - {livro.autor} (R$ {livro.preco:.2f})")
        
        # Livros mais antigos
        print("\n📚 TOP 5 LIVROS MAIS ANTIGOS:")
        for livro in relatorio['livros_mais_antigos']:
            print(f"   • {livro.titulo} - {livro.autor} ({livro.ano_publicacao})")
        
        # Distribuição por década
        print("\n🗓️  DISTRIBUIÇÃO POR DÉCADA:")
        decadas_ordenadas = sorted(relatorio['por_decada'].items())
        
        for decada, livros in decadas_ordenadas:
            print(f"   • {decada}s: {len(livros)} livros")
    
    def solicitar_filtros_busca_avancada(self) -> dict:
        """Solicita filtros para busca avançada"""
        self.exibir_submenu("BUSCA AVANÇADA - FILTROS")
        
        print("Digite os filtros desejados (deixe em branco para ignorar):")
        
        filtros = {}
        
        autor = input("Autor (busca parcial): ").strip()
        if autor:
            filtros['autor'] = autor
        
        titulo = input("Título (busca parcial): ").strip()
        if titulo:
            filtros['titulo'] = titulo
        
        ano_min = input("Ano mínimo: ").strip()
        if ano_min:
            try:
                filtros['ano_min'] = int(ano_min)
            except ValueError:
                pass
        
        ano_max = input("Ano máximo: ").strip()
        if ano_max:
            try:
                filtros['ano_max'] = int(ano_max)
            except ValueError:
                pass
        
        preco_min = input("Preço mínimo (R$): ").strip()
        if preco_min:
            try:
                filtros['preco_min'] = float(preco_min.replace(',', '.'))
            except ValueError:
                pass
        
        preco_max = input("Preço máximo (R$): ").strip()
        if preco_max:
            try:
                filtros['preco_max'] = float(preco_max.replace(',', '.'))
            except ValueError:
                pass
        
        return filtros
    
    def exibir_mensagem_sucesso(self, mensagem: str):
        """Exibe uma mensagem de sucesso"""
        print(f"✅ {mensagem}")
    
    def exibir_mensagem_erro(self, mensagem: str):
        """Exibe uma mensagem de erro"""
        print(f"❌ Erro: {mensagem}")
    
    def exibir_mensagem_aviso(self, mensagem: str):
        """Exibe uma mensagem de aviso"""
        print(f"⚠️  {mensagem}")
    
    def exibir_mensagem_info(self, mensagem: str):
        """Exibe uma mensagem informativa"""
        print(f"ℹ️  {mensagem}")
    
    def pausar(self, mensagem: str = "Pressione Enter para continuar..."):
        """Pausa a execução aguardando input do usuário"""
        input(f"\n{mensagem}")
    
    def exibir_bem_vindo(self):
        """Exibe mensagem de boas-vindas"""
        self.limpar_tela()
        print("="*self.largura_console)
        print("🚀 Bem-vindo ao Sistema de Gerenciamento de Livraria!")
        print("📚 Versão 2.0 - Arquitetura MVC")
        print("="*self.largura_console)
    
    def exibir_despedida(self):
        """Exibe mensagem de despedida"""
        print("\n" + "="*self.largura_console)
        print("📚 Obrigado por usar o Sistema de Gerenciamento de Livraria!")
        print("🔄 Até a próxima!")
        print("="*self.largura_console)