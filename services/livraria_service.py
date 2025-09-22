"""
Serviço de negócio da livraria
Implementa a lógica de negócio e orquestra as operações entre diferentes componentes
"""
from typing import List, Optional
from pathlib import Path

from models.livro import Livro
from database.database_manager import DatabaseManager, LivroRepository
from services.file_manager import FileManager, CSVManager

class LivrariaService:
    """Serviço principal da livraria que orquestra todas as operações"""
    
    def __init__(self, base_dir: str = "meu_sistema_livraria"):
        # Inicializar gerenciadores
        self.file_manager = FileManager(base_dir)
        self.csv_manager = CSVManager(self.file_manager)
        
        # Inicializar banco de dados
        db_path = self.file_manager.get_database_path()
        self.db_manager = DatabaseManager(db_path)
        self.livro_repository = LivroRepository(self.db_manager)
    
    def _criar_backup_automatico(self) -> Optional[Path]:
        """Cria um backup automático antes de operações críticas"""
        return self.file_manager.criar_backup()
    
    # ==================== OPERAÇÕES CRUD ====================
    
    def adicionar_livro(self, titulo: str, autor: str, ano_publicacao: int, preco: float) -> Livro:
        """Adiciona um novo livro ao sistema"""
        # Criar objeto livro (validação acontece automaticamente)
        livro = Livro(titulo=titulo.strip(), autor=autor.strip(), 
                     ano_publicacao=ano_publicacao, preco=preco)
        
        # Criar backup antes da operação
        backup_path = self._criar_backup_automatico()
        if backup_path:
            self.file_manager._log_info(f"Backup criado antes de adicionar livro: {backup_path.name}")
        
        # Salvar no banco
        livro_salvo = self.livro_repository.criar(livro)
        
        self.file_manager._log_info(f"Livro adicionado: {livro_salvo.titulo} (ID: {livro_salvo.id})")
        return livro_salvo
    
    def buscar_todos_livros(self) -> List[Livro]:
        """Busca todos os livros cadastrados"""
        return self.livro_repository.buscar_todos()
    
    def buscar_livro_por_id(self, livro_id: int) -> Optional[Livro]:
        """Busca um livro específico pelo ID"""
        return self.livro_repository.buscar_por_id(livro_id)
    
    def buscar_livros_por_autor(self, autor: str) -> List[Livro]:
        """Busca livros por autor (busca parcial)"""
        if not autor.strip():
            raise ValueError("Nome do autor não pode estar vazio")
        
        return self.livro_repository.buscar_por_autor(autor.strip())
    
    def buscar_livros_por_titulo(self, titulo: str) -> List[Livro]:
        """Busca livros por título (busca parcial)"""
        if not titulo.strip():
            raise ValueError("Título não pode estar vazio")
        
        return self.livro_repository.buscar_por_titulo(titulo.strip())
    
    def atualizar_livro(self, livro: Livro) -> bool:
        """Atualiza um livro completo"""
        if not livro.id:
            raise ValueError("Livro deve ter um ID para ser atualizado")
        
        # Verificar se o livro existe
        livro_existente = self.livro_repository.buscar_por_id(livro.id)
        if not livro_existente:
            raise ValueError(f"Livro com ID {livro.id} não encontrado")
        
        # Criar backup antes da operação
        backup_path = self._criar_backup_automatico()
        if backup_path:
            self.file_manager._log_info(f"Backup criado antes de atualizar livro: {backup_path.name}")
        
        # Atualizar
        sucesso = self.livro_repository.atualizar(livro)
        
        if sucesso:
            self.file_manager._log_info(f"Livro atualizado: {livro.titulo} (ID: {livro.id})")
        
        return sucesso
    
    def atualizar_preco_livro(self, livro_id: int, novo_preco: float) -> bool:
        """Atualiza apenas o preço de um livro"""
        # Verificar se o livro existe
        livro = self.livro_repository.buscar_por_id(livro_id)
        if not livro:
            raise ValueError(f"Livro com ID {livro_id} não encontrado")
        
        # Validar preço
        if novo_preco < 0:
            raise ValueError("Preço deve ser um valor positivo")
        
        # Criar backup antes da operação
        backup_path = self._criar_backup_automatico()
        if backup_path:
            self.file_manager._log_info(f"Backup criado antes de atualizar preço: {backup_path.name}")
        
        # Atualizar preço
        sucesso = self.livro_repository.atualizar_preco(livro_id, novo_preco)
        
        if sucesso:
            self.file_manager._log_info(f"Preço atualizado: {livro.titulo} - R$ {novo_preco:.2f}")
        
        return sucesso
    
    def remover_livro(self, livro_id: int) -> bool:
        """Remove um livro do sistema"""
        # Verificar se o livro existe
        livro = self.livro_repository.buscar_por_id(livro_id)
        if not livro:
            raise ValueError(f"Livro com ID {livro_id} não encontrado")
        
        # Criar backup antes da operação
        backup_path = self._criar_backup_automatico()
        if backup_path:
            self.file_manager._log_info(f"Backup criado antes de remover livro: {backup_path.name}")
        
        # Remover
        sucesso = self.livro_repository.deletar(livro_id)
        
        if sucesso:
            self.file_manager._log_info(f"Livro removido: {livro.titulo} (ID: {livro_id})")
        
        return sucesso
    
    # ==================== OPERAÇÕES DE ARQUIVO ====================
    
    def exportar_dados_csv(self, nome_arquivo: Optional[str] = None) -> Optional[Path]:
        """Exporta todos os livros para um arquivo CSV"""
        livros = self.buscar_todos_livros()
        
        if not livros:
            raise ValueError("Nenhum livro encontrado para exportar")
        
        csv_path = self.csv_manager.exportar_livros(livros, nome_arquivo)
        
        if csv_path:
            self.file_manager._log_info(f"Dados exportados: {len(livros)} livros para {csv_path.name}")
        
        return csv_path
    
    def importar_dados_csv(self, csv_path: Path) -> int:
        """Importa livros de um arquivo CSV"""
        if not csv_path.exists():
            raise FileNotFoundError(f"Arquivo não encontrado: {csv_path}")
        
        # Validar arquivo antes da importação
        validacao = self.csv_manager.validar_arquivo_csv(csv_path)
        if not validacao['valido']:
            raise ValueError(f"Arquivo CSV inválido: {validacao['erro']}")
        
        # Criar backup antes da importação
        backup_path = self._criar_backup_automatico()
        if backup_path:
            self.file_manager._log_info(f"Backup criado antes de importar CSV: {backup_path.name}")
        
        # Importar livros
        livros = self.csv_manager.importar_livros(csv_path)
        
        # Salvar no banco
        livros_salvos = 0
        erros = []
        
        for livro in livros:
            try:
                # Remove ID para evitar conflitos (será gerado automaticamente)
                livro.id = None
                self.livro_repository.criar(livro)
                livros_salvos += 1
            except Exception as e:
                erros.append(f"Erro ao salvar '{livro.titulo}': {e}")
        
        # Log do resultado
        self.file_manager._log_info(f"Importação concluída: {livros_salvos} livros salvos")
        
        if erros:
            error_msg = "Erros durante importação:\n" + "\n".join(erros)
            self.file_manager._log_error(error_msg)
        
        return livros_salvos
    
    def listar_arquivos_csv(self) -> List[Path]:
        """Lista arquivos CSV disponíveis para importação"""
        return self.csv_manager.listar_arquivos_csv()
    
    def validar_arquivo_csv(self, csv_path: Path) -> dict:
        """Valida um arquivo CSV"""
        return self.csv_manager.validar_arquivo_csv(csv_path)
    
    # ==================== OPERAÇÕES DE BACKUP ====================
    
    def criar_backup_manual(self) -> Optional[Path]:
        """Cria um backup manual do banco de dados"""
        backup_path = self.file_manager.criar_backup()
        
        if backup_path:
            self.file_manager._log_info(f"Backup manual criado: {backup_path.name}")
        
        return backup_path
    
    def listar_backups(self) -> List[dict]:
        """Lista todos os backups disponíveis com informações"""
        backups = self.file_manager.listar_backups()
        
        backup_info = []
        for backup in backups:
            stat = backup.stat()
            backup_info.append({
                'nome': backup.name,
                'caminho': backup,
                'tamanho': stat.st_size,
                'data_criacao': stat.st_mtime,
                'data_criacao_str': backup.name.split('_')[-1].replace('.db', '').replace('-', '/').replace('_', ' ')
            })
        
        return backup_info
    
    def restaurar_backup(self, backup_path: Path) -> bool:
        """Restaura um backup específico"""
        sucesso = self.file_manager.restaurar_backup(backup_path)
        
        if sucesso:
            # Recriar conexão com o banco após restauração
            self.db_manager = DatabaseManager(self.file_manager.get_database_path())
            self.livro_repository = LivroRepository(self.db_manager)
            
            self.file_manager._log_info(f"Backup restaurado: {backup_path.name}")
        
        return sucesso
    
    # ==================== ESTATÍSTICAS E RELATÓRIOS ====================
    
    def obter_estatisticas(self) -> dict:
        """Obtém estatísticas gerais do sistema"""
        stats_livros = self.livro_repository.buscar_estatisticas()
        backups = self.listar_backups()
        
        return {
            **stats_livros,
            'total_backups': len(backups),
            'ultimo_backup': backups[0]['data_criacao_str'] if backups else 'Nenhum'
        }
    
    def gerar_relatorio_completo(self) -> dict:
        """Gera um relatório completo do sistema"""
        livros = self.buscar_todos_livros()
        stats = self.obter_estatisticas()
        
        # Agrupar por autor
        autores = {}
        for livro in livros:
            if livro.autor not in autores:
                autores[livro.autor] = {
                    'quantidade': 0,
                    'preco_total': 0,
                    'livros': []
                }
            
            autores[livro.autor]['quantidade'] += 1
            autores[livro.autor]['preco_total'] += livro.preco
            autores[livro.autor]['livros'].append(livro.titulo)
        
        # Agrupar por década
        decadas = {}
        for livro in livros:
            decada = (livro.ano_publicacao // 10) * 10
            if decada not in decadas:
                decadas[decada] = []
            decadas[decada].append(livro)
        
        return {
            'estatisticas_gerais': stats,
            'por_autor': autores,
            'por_decada': decadas,
            'livros_mais_caros': sorted(livros, key=lambda x: x.preco, reverse=True)[:5],
            'livros_mais_baratos': sorted(livros, key=lambda x: x.preco)[:5],
            'livros_mais_antigos': sorted(livros, key=lambda x: x.ano_publicacao)[:5],
            'livros_mais_recentes': sorted(livros, key=lambda x: x.ano_publicacao, reverse=True)[:5]
        }
    
    # ==================== VALIDAÇÕES E UTILITÁRIOS ====================
    
    def validar_entrada_livro(self, titulo: str, autor: str, ano_str: str, preco_str: str) -> tuple:
        """Valida e converte entradas para criação/atualização de livro"""
        # Validar título
        if not titulo or not titulo.strip():
            raise ValueError("Título não pode estar vazio")
        
        # Validar autor
        if not autor or not autor.strip():
            raise ValueError("Autor não pode estar vazio")
        
        # Validar ano
        try:
            ano = int(ano_str)
        except ValueError:
            raise ValueError("Ano deve ser um número inteiro")
        
        # Validar preço
        try:
            preco = float(preco_str.replace(',', '.'))  # Aceitar vírgula como separador decimal
        except ValueError:
            raise ValueError("Preço deve ser um número válido")
        
        # Criar objeto temporário para validação completa
        livro_temp = Livro(titulo=titulo.strip(), autor=autor.strip(), 
                          ano_publicacao=ano, preco=preco)
        
        return titulo.strip(), autor.strip(), ano, preco
    
    def buscar_livros_avancado(self, filtros: dict) -> List[Livro]:
        """Busca avançada com múltiplos filtros"""
        livros = self.buscar_todos_livros()
        
        # Aplicar filtros
        if 'autor' in filtros and filtros['autor']:
            livros = [l for l in livros if filtros['autor'].lower() in l.autor.lower()]
        
        if 'titulo' in filtros and filtros['titulo']:
            livros = [l for l in livros if filtros['titulo'].lower() in l.titulo.lower()]
        
        if 'ano_min' in filtros and filtros['ano_min']:
            livros = [l for l in livros if l.ano_publicacao >= filtros['ano_min']]
        
        if 'ano_max' in filtros and filtros['ano_max']:
            livros = [l for l in livros if l.ano_publicacao <= filtros['ano_max']]
        
        if 'preco_min' in filtros and filtros['preco_min']:
            livros = [l for l in livros if l.preco >= filtros['preco_min']]
        
        if 'preco_max' in filtros and filtros['preco_max']:
            livros = [l for l in livros if l.preco <= filtros['preco_max']]
        
        return livros