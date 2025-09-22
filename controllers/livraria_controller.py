"""
Controller principal da aplicação
Responsável por orquestrar as interações entre View e Service
"""
from pathlib import Path
from typing import Dict, Callable

from models.livro import Livro
from services.livraria_service import LivrariaService
from views.console_view import ConsoleView

class LivrariaController:
    """Controller principal que coordena as operações do sistema"""
    
    def __init__(self, base_dir: str = "meu_sistema_livraria"):
        self.service = LivrariaService(base_dir)
        self.view = ConsoleView()
        
        # Mapeamento de opções do menu para métodos
        self.opcoes_menu: Dict[str, Callable] = {
            '1': self.adicionar_livro,
            '2': self.exibir_todos_livros,
            '3': self.atualizar_preco_livro,
            '4': self.remover_livro,
            '5': self.buscar_por_autor,
            '6': self.buscar_por_titulo,
            '7': self.busca_avancada,
            '8': self.exportar_dados_csv,
            '9': self.importar_dados_csv,
            '10': self.fazer_backup_manual,
            '11': self.restaurar_backup,
            '12': self.ver_estatisticas,
            '13': self.gerar_relatorio_completo,
            '14': self.sair
        }
    
    def executar(self):
        """Executa o loop principal da aplicação"""
        self.view.exibir_bem_vindo()
        
        while True:
            try:
                self.view.exibir_menu_principal()
                opcao = self.view.solicitar_opcao_menu()
                
                if opcao in self.opcoes_menu:
                    self.opcoes_menu[opcao]()
                    
                    if opcao == '14':  # Sair
                        break
                else:
                    self.view.exibir_mensagem_erro("Opção inválida! Escolha uma opção de 1 a 14.")
                
                # Pausa após cada operação (exceto sair)
                if opcao != '14':
                    self.view.pausar()
                    
            except KeyboardInterrupt:
                self.view.exibir_mensagem_info("\nSaindo do sistema...")
                break
            except Exception as e:
                self.view.exibir_mensagem_erro(f"Erro inesperado: {e}")
                self.view.pausar()
    
    def adicionar_livro(self):
        """Controlador para adicionar novo livro"""
        try:
            dados = self.view.solicitar_dados_livro()
            
            # Validar e converter dados
            titulo, autor, ano, preco = self.service.validar_entrada_livro(
                dados['titulo'], dados['autor'], dados['ano'], dados['preco']
            )
            
            # Adicionar livro
            livro = self.service.adicionar_livro(titulo, autor, ano, preco)
            
            self.view.exibir_mensagem_sucesso(
                f"Livro '{livro.titulo}' adicionado com sucesso! (ID: {livro.id})"
            )
            
        except ValueError as e:
            self.view.exibir_mensagem_erro(str(e))
        except Exception as e:
            self.view.exibir_mensagem_erro(f"Erro ao adicionar livro: {e}")
    
    def exibir_todos_livros(self):
        """Controlador para exibir todos os livros"""
        try:
            livros = self.service.buscar_todos_livros()
            self.view.exibir_livros(livros, "TODOS OS LIVROS")
            
        except Exception as e:
            self.view.exibir_mensagem_erro(f"Erro ao buscar livros: {e}")
    
    def atualizar_preco_livro(self):
        """Controlador para atualizar preço de um livro"""
        try:
            # Primeiro mostrar todos os livros
            self.exibir_todos_livros()
            
            if not self.service.buscar_todos_livros():
                return
            
            # Solicitar ID do livro
            id_str = self.view.solicitar_id_livro("ID do livro para atualizar preço")
            
            if not id_str.isdigit():
                self.view.exibir_mensagem_erro("ID deve ser um número!")
                return
            
            livro_id = int(id_str)
            
            # Verificar se livro existe e mostrar dados atuais
            livro = self.service.buscar_livro_por_id(livro_id)
            if not livro:
                self.view.exibir_mensagem_erro("Livro não encontrado!")
                return
            
            self.view.exibir_livro_detalhado(livro)
            
            # Solicitar novo preço
            novo_preco_str = self.view.solicitar_novo_preco()
            
            try:
                novo_preco = float(novo_preco_str.replace(',', '.'))
            except ValueError:
                self.view.exibir_mensagem_erro("Preço deve ser um número válido!")
                return
            
            # Atualizar preço
            sucesso = self.service.atualizar_preco_livro(livro_id, novo_preco)
            
            if sucesso:
                self.view.exibir_mensagem_sucesso(
                    f"Preço do livro '{livro.titulo}' atualizado para R$ {novo_preco:.2f}"
                )
            else:
                self.view.exibir_mensagem_erro("Falha ao atualizar preço")
            
        except ValueError as e:
            self.view.exibir_mensagem_erro(str(e))
        except Exception as e:
            self.view.exibir_mensagem_erro(f"Erro ao atualizar preço: {e}")
    
    def remover_livro(self):
        """Controlador para remover um livro"""
        try:
            # Primeiro mostrar todos os livros
            self.exibir_todos_livros()
            
            if not self.service.buscar_todos_livros():
                return
            
            # Solicitar ID do livro
            id_str = self.view.solicitar_id_livro("ID do livro para remover")
            
            if not id_str.isdigit():
                self.view.exibir_mensagem_erro("ID deve ser um número!")
                return
            
            livro_id = int(id_str)
            
            # Verificar se livro existe
            livro = self.service.buscar_livro_por_id(livro_id)
            if not livro:
                self.view.exibir_mensagem_erro("Livro não encontrado!")
                return
            
            # Mostrar dados do livro e confirmar remoção
            self.view.exibir_livro_detalhado(livro)
            
            if not self.view.solicitar_confirmacao(f"Tem certeza que deseja remover '{livro.titulo}'?"):
                self.view.exibir_mensagem_info("Operação cancelada.")
                return
            
            # Remover livro
            sucesso = self.service.remover_livro(livro_id)
            
            if sucesso:
                self.view.exibir_mensagem_sucesso(f"Livro '{livro.titulo}' removido com sucesso!")
            else:
                self.view.exibir_mensagem_erro("Falha ao remover livro")
            
        except ValueError as e:
            self.view.exibir_mensagem_erro(str(e))
        except Exception as e:
            self.view.exibir_mensagem_erro(f"Erro ao remover livro: {e}")
    
    def buscar_por_autor(self):
        """Controlador para buscar livros por autor"""
        try:
            autor = self.view.solicitar_texto("Nome do autor (busca parcial)")
            
            if not autor:
                self.view.exibir_mensagem_erro("Nome do autor não pode estar vazio!")
                return
            
            livros = self.service.buscar_livros_por_autor(autor)
            self.view.exibir_livros(livros, f"LIVROS DO AUTOR '{autor.upper()}'")
            
        except ValueError as e:
            self.view.exibir_mensagem_erro(str(e))
        except Exception as e:
            self.view.exibir_mensagem_erro(f"Erro ao buscar por autor: {e}")
    
    def buscar_por_titulo(self):
        """Controlador para buscar livros por título"""
        try:
            titulo = self.view.solicitar_texto("Título do livro (busca parcial)")
            
            if not titulo:
                self.view.exibir_mensagem_erro("Título não pode estar vazio!")
                return
            
            livros = self.service.buscar_livros_por_titulo(titulo)
            self.view.exibir_livros(livros, f"LIVROS COM TÍTULO '{titulo.upper()}'")
            
        except ValueError as e:
            self.view.exibir_mensagem_erro(str(e))
        except Exception as e:
            self.view.exibir_mensagem_erro(f"Erro ao buscar por título: {e}")
    
    def busca_avancada(self):
        """Controlador para busca avançada com múltiplos filtros"""
        try:
            filtros = self.view.solicitar_filtros_busca_avancada()
            
            if not filtros:
                self.view.exibir_mensagem_aviso("Nenhum filtro especificado!")
                return
            
            livros = self.service.buscar_livros_avancado(filtros)
            
            # Criar descrição dos filtros aplicados
            filtros_str = []
            for chave, valor in filtros.items():
                if chave == 'autor':
                    filtros_str.append(f"Autor: '{valor}'")
                elif chave == 'titulo':
                    filtros_str.append(f"Título: '{valor}'")
                elif chave == 'ano_min':
                    filtros_str.append(f"Ano ≥ {valor}")
                elif chave == 'ano_max':
                    filtros_str.append(f"Ano ≤ {valor}")
                elif chave == 'preco_min':
                    filtros_str.append(f"Preço ≥ R$ {valor:.2f}")
                elif chave == 'preco_max':
                    filtros_str.append(f"Preço ≤ R$ {valor:.2f}")
            
            titulo_busca = f"BUSCA AVANÇADA - {' | '.join(filtros_str)}"
            self.view.exibir_livros(livros, titulo_busca)
            
        except Exception as e:
            self.view.exibir_mensagem_erro(f"Erro na busca avançada: {e}")
    
    def exportar_dados_csv(self):
        """Controlador para exportar dados em CSV"""
        try:
            # Verificar se há livros para exportar
            livros = self.service.buscar_todos_livros()
            if not livros:
                self.view.exibir_mensagem_aviso("Nenhum livro cadastrado para exportar!")
                return
            
            # Perguntar se quer usar nome personalizado
            usar_nome_personalizado = self.view.solicitar_confirmacao(
                "Deseja usar um nome personalizado para o arquivo?"
            )
            
            nome_arquivo = None
            if usar_nome_personalizado:
                nome = self.view.solicitar_texto("Nome do arquivo (sem extensão)")
                if nome:
                    nome_arquivo = f"{nome}.csv"
            
            # Exportar
            csv_path = self.service.exportar_dados_csv(nome_arquivo)
            
            if csv_path:
                self.view.exibir_mensagem_sucesso(
                    f"Dados exportados com sucesso!\n"
                    f"Arquivo: {csv_path.name}\n"
                    f"Total de livros: {len(livros)}"
                )
            else:
                self.view.exibir_mensagem_erro("Falha ao exportar dados")
            
        except ValueError as e:
            self.view.exibir_mensagem_erro(str(e))
        except Exception as e:
            self.view.exibir_mensagem_erro(f"Erro ao exportar dados: {e}")
    
    def importar_dados_csv(self):
        """Controlador para importar dados de CSV"""
        try:
            # Listar arquivos CSV disponíveis
            arquivos_csv = self.service.listar_arquivos_csv()
            
            if not arquivos_csv:
                nome_arquivo = self.view.solicitar_texto(
                    "Nenhum arquivo CSV encontrado. Digite o nome do arquivo"
                )
                csv_path = Path(self.service.file_manager.exports_dir) / nome_arquivo
            else:
                self.view.exibir_arquivos_csv(arquivos_csv)
                
                escolha = self.view.solicitar_escolha_arquivo(len(arquivos_csv))
                
                if escolha.isdigit() and 1 <= int(escolha) <= len(arquivos_csv):
                    csv_path = arquivos_csv[int(escolha) - 1]
                else:
                    csv_path = Path(self.service.file_manager.exports_dir) / escolha
            
            # Validar arquivo antes da importação
            if not csv_path.exists():
                self.view.exibir_mensagem_erro(f"Arquivo não encontrado: {csv_path.name}")
                return
            
            validacao = self.service.validar_arquivo_csv(csv_path)
            if not validacao['valido']:
                self.view.exibir_mensagem_erro(f"Arquivo inválido: {validacao['erro']}")
                return
            
            # Mostrar informações do arquivo
            self.view.exibir_mensagem_info(
                f"Arquivo: {csv_path.name}\n"
                f"Total de linhas: {validacao['total_linhas']}\n"
                f"Linhas válidas: {validacao['linhas_validas']}\n"
                f"Tem cabeçalho: {'Sim' if validacao['tem_cabecalho'] else 'Não'}"
            )
            
            # Confirmar importação
            if not self.view.solicitar_confirmacao("Continuar com a importação?"):
                self.view.exibir_mensagem_info("Importação cancelada.")
                return
            
            # Importar
            livros_importados = self.service.importar_dados_csv(csv_path)
            
            self.view.exibir_mensagem_sucesso(
                f"Importação concluída!\n"
                f"Arquivo: {csv_path.name}\n"
                f"Livros importados: {livros_importados}"
            )
            
        except FileNotFoundError as e:
            self.view.exibir_mensagem_erro(str(e))
        except ValueError as e:
            self.view.exibir_mensagem_erro(str(e))
        except Exception as e:
            self.view.exibir_mensagem_erro(f"Erro ao importar dados: {e}")
    
    def fazer_backup_manual(self):
        """Controlador para criar backup manual"""
        try:
            backup_path = self.service.criar_backup_manual()
            
            if backup_path:
                self.view.exibir_mensagem_sucesso(
                    f"Backup criado com sucesso!\n"
                    f"Arquivo: {backup_path.name}"
                )
                
                # Mostrar total de backups
                backups = self.service.listar_backups()
                self.view.exibir_mensagem_info(f"Total de backups disponíveis: {len(backups)}")
            else:
                self.view.exibir_mensagem_erro("Falha ao criar backup")
            
        except Exception as e:
            self.view.exibir_mensagem_erro(f"Erro ao criar backup: {e}")
    
    def restaurar_backup(self):
        """Controlador para restaurar backup"""
        try:
            # Listar backups disponíveis
            backups = self.service.listar_backups()
            
            if not backups:
                self.view.exibir_mensagem_aviso("Nenhum backup encontrado!")
                return
            
            self.view.exibir_backups(backups)
            
            # Solicitar escolha do backup
            escolha = self.view.solicitar_texto("Número do backup para restaurar")
            
            if not escolha.isdigit() or not (1 <= int(escolha) <= len(backups)):
                self.view.exibir_mensagem_erro("Opção inválida!")
                return
            
            backup_selecionado = backups[int(escolha) - 1]
            
            # Confirmar restauração
            self.view.exibir_mensagem_aviso(
                f"⚠️  ATENÇÃO: Esta operação irá substituir o banco atual!\n"
                f"Backup selecionado: {backup_selecionado['nome']}\n"
                f"Data: {backup_selecionado['data_criacao_str']}"
            )
            
            if not self.view.solicitar_confirmacao("Tem certeza que deseja restaurar este backup?"):
                self.view.exibir_mensagem_info("Restauração cancelada.")
                return
            
            # Restaurar
            sucesso = self.service.restaurar_backup(backup_selecionado['caminho'])
            
            if sucesso:
                self.view.exibir_mensagem_sucesso(
                    f"Backup restaurado com sucesso!\n"
                    f"Arquivo: {backup_selecionado['nome']}"
                )
            else:
                self.view.exibir_mensagem_erro("Falha ao restaurar backup")
            
        except Exception as e:
            self.view.exibir_mensagem_erro(f"Erro ao restaurar backup: {e}")
    
    def ver_estatisticas(self):
        """Controlador para exibir estatísticas"""
        try:
            stats = self.service.obter_estatisticas()
            self.view.exibir_estatisticas(stats)
            
        except Exception as e:
            self.view.exibir_mensagem_erro(f"Erro ao obter estatísticas: {e}")
    
    def gerar_relatorio_completo(self):
        """Controlador para gerar relatório completo"""
        try:
            # Verificar se há dados para relatório
            if self.service.livro_repository.contar_livros() == 0:
                self.view.exibir_mensagem_aviso("Nenhum livro cadastrado para gerar relatório!")
                return
            
            self.view.exibir_mensagem_info("Gerando relatório completo...")
            
            relatorio = self.service.gerar_relatorio_completo()
            self.view.exibir_relatorio_completo(relatorio)
            
        except Exception as e:
            self.view.exibir_mensagem_erro(f"Erro ao gerar relatório: {e}")
    
    def sair(self):
        """Controlador para sair do sistema"""
        self.view.exibir_despedida()