"""
Gerenciador de banco de dados SQLite
Implementa o padrão Repository para acesso aos dados
"""
import sqlite3
from pathlib import Path
from typing import List, Optional
from contextlib import contextmanager

from models.livro import Livro

class DatabaseManager:
    """Gerenciador de banco de dados com padrão Repository"""
    
    def __init__(self, db_path: Path):
        self.db_path = db_path
        self._criar_tabelas()
    
    @contextmanager
    def get_connection(self):
        """Context manager para conexões com o banco"""
        conn = sqlite3.connect(self.db_path)
        try:
            conn.row_factory = sqlite3.Row  # Para acessar colunas por nome
            yield conn
            conn.commit()
        except Exception:
            conn.rollback()
            raise
        finally:
            conn.close()
    
    def _criar_tabelas(self):
        """Cria as tabelas necessárias no banco de dados"""
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS livros (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    titulo TEXT NOT NULL,
                    autor TEXT NOT NULL,
                    ano_publicacao INTEGER NOT NULL,
                    preco REAL NOT NULL,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            ''')
            
            # Criar trigger para atualizar updated_at
            cursor.execute('''
                CREATE TRIGGER IF NOT EXISTS update_livros_timestamp 
                AFTER UPDATE ON livros
                FOR EACH ROW
                BEGIN
                    UPDATE livros SET updated_at = CURRENT_TIMESTAMP WHERE id = NEW.id;
                END
            ''')

class LivroRepository:
    """Repository para operações CRUD com livros"""
    
    def __init__(self, db_manager: DatabaseManager):
        self.db_manager = db_manager
    
    def criar(self, livro: Livro) -> Livro:
        """Cria um novo livro no banco de dados"""
        livro.validar()  # Valida antes de inserir
        
        with self.db_manager.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute('''
                INSERT INTO livros (titulo, autor, ano_publicacao, preco)
                VALUES (?, ?, ?, ?)
            ''', (livro.titulo, livro.autor, livro.ano_publicacao, livro.preco))
            
            livro.id = cursor.lastrowid
            return livro
    
    def buscar_por_id(self, livro_id: int) -> Optional[Livro]:
        """Busca um livro pelo ID"""
        with self.db_manager.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute('SELECT * FROM livros WHERE id = ?', (livro_id,))
            row = cursor.fetchone()
            
            if row:
                return self._row_to_livro(row)
            return None
    
    def buscar_todos(self) -> List[Livro]:
        """Busca todos os livros"""
        with self.db_manager.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute('SELECT * FROM livros ORDER BY titulo')
            rows = cursor.fetchall()
            
            return [self._row_to_livro(row) for row in rows]
    
    def buscar_por_autor(self, autor: str) -> List[Livro]:
        """Busca livros por autor (busca parcial)"""
        with self.db_manager.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute('''
                SELECT * FROM livros 
                WHERE autor LIKE ? 
                ORDER BY titulo
            ''', (f'%{autor}%',))
            rows = cursor.fetchall()
            
            return [self._row_to_livro(row) for row in rows]
    
    def buscar_por_titulo(self, titulo: str) -> List[Livro]:
        """Busca livros por título (busca parcial)"""
        with self.db_manager.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute('''
                SELECT * FROM livros 
                WHERE titulo LIKE ? 
                ORDER BY titulo
            ''', (f'%{titulo}%',))
            rows = cursor.fetchall()
            
            return [self._row_to_livro(row) for row in rows]
    
    def atualizar(self, livro: Livro) -> bool:
        """Atualiza um livro existente"""
        if not livro.id:
            raise ValueError("Livro deve ter um ID para ser atualizado")
        
        livro.validar()  # Valida antes de atualizar
        
        with self.db_manager.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute('''
                UPDATE livros 
                SET titulo = ?, autor = ?, ano_publicacao = ?, preco = ?
                WHERE id = ?
            ''', (livro.titulo, livro.autor, livro.ano_publicacao, livro.preco, livro.id))
            
            return cursor.rowcount > 0
    
    def atualizar_preco(self, livro_id: int, novo_preco: float) -> bool:
        """Atualiza apenas o preço de um livro"""
        if novo_preco < 0:
            raise ValueError("Preço deve ser positivo")
        
        with self.db_manager.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute('''
                UPDATE livros SET preco = ? WHERE id = ?
            ''', (novo_preco, livro_id))
            
            return cursor.rowcount > 0
    
    def deletar(self, livro_id: int) -> bool:
        """Deleta um livro pelo ID"""
        with self.db_manager.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute('DELETE FROM livros WHERE id = ?', (livro_id,))
            
            return cursor.rowcount > 0
    
    def contar_livros(self) -> int:
        """Conta o total de livros cadastrados"""
        with self.db_manager.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute('SELECT COUNT(*) FROM livros')
            return cursor.fetchone()[0]
    
    def buscar_estatisticas(self) -> dict:
        """Retorna estatísticas dos livros"""
        with self.db_manager.get_connection() as conn:
            cursor = conn.cursor()
            
            # Contar total
            cursor.execute('SELECT COUNT(*) FROM livros')
            total = cursor.fetchone()[0]
            
            # Preço médio
            cursor.execute('SELECT AVG(preco) FROM livros')
            preco_medio = cursor.fetchone()[0] or 0
            
            # Livro mais caro
            cursor.execute('SELECT MAX(preco) FROM livros')
            preco_maximo = cursor.fetchone()[0] or 0
            
            # Livro mais barato
            cursor.execute('SELECT MIN(preco) FROM livros')
            preco_minimo = cursor.fetchone()[0] or 0
            
            # Ano mais antigo e mais recente
            cursor.execute('SELECT MIN(ano_publicacao), MAX(ano_publicacao) FROM livros')
            anos = cursor.fetchone()
            ano_min = anos[0] or 0
            ano_max = anos[1] or 0
            
            return {
                'total_livros': total,
                'preco_medio': preco_medio,
                'preco_maximo': preco_maximo,
                'preco_minimo': preco_minimo,
                'ano_mais_antigo': ano_min,
                'ano_mais_recente': ano_max
            }
    
    def _row_to_livro(self, row) -> Livro:
        """Converte uma linha do banco para objeto Livro"""
        return Livro(
            id=row['id'],
            titulo=row['titulo'],
            autor=row['autor'],
            ano_publicacao=row['ano_publicacao'],
            preco=row['preco']
        )