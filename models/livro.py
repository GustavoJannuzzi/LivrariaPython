"""
Model para a entidade Livro
Responsável pela representação e validação dos dados do livro
"""
from datetime import datetime
from dataclasses import dataclass
from typing import Optional

@dataclass
class Livro:
    """Classe que representa um livro no sistema"""
    titulo: str
    autor: str
    ano_publicacao: int
    preco: float
    id: Optional[int] = None
    
    def __post_init__(self):
        """Validações após a inicialização do objeto"""
        self.validar()
    
    def validar(self):
        """Valida os dados do livro"""
        if not self.titulo or not self.titulo.strip():
            raise ValueError("Título não pode estar vazio")
        
        if not self.autor or not self.autor.strip():
            raise ValueError("Autor não pode estar vazio")
        
        if not self._validar_ano(self.ano_publicacao):
            raise ValueError("Ano deve estar entre 1000 e o próximo ano")
        
        if not self._validar_preco(self.preco):
            raise ValueError("Preço deve ser um valor positivo")
    
    def _validar_ano(self, ano: int) -> bool:
        """Valida se o ano é válido"""
        try:
            ano_atual = datetime.now().year
            return 1000 <= ano <= ano_atual + 1
        except (ValueError, TypeError):
            return False
    
    def _validar_preco(self, preco: float) -> bool:
        """Valida se o preço é válido"""
        try:
            return preco >= 0
        except (ValueError, TypeError):
            return False
    
    def to_dict(self) -> dict:
        """Converte o livro para dicionário"""
        return {
            'id': self.id,
            'titulo': self.titulo,
            'autor': self.autor,
            'ano_publicacao': self.ano_publicacao,
            'preco': self.preco
        }
    
    def to_csv_row(self) -> list:
        """Converte o livro para uma linha CSV"""
        return [self.id, self.titulo, self.autor, self.ano_publicacao, self.preco]
    
    @classmethod
    def from_csv_row(cls, row: list) -> 'Livro':
        """Cria um livro a partir de uma linha CSV"""
        if len(row) < 4:
            raise ValueError("Linha CSV deve ter pelo menos 4 campos (título, autor, ano, preço)")
        
        # Se tiver ID, usar; senão, será None
        id_livro = None if len(row) < 5 else (int(row[0]) if row[0] else None)
        
        return cls(
            id=id_livro,
            titulo=str(row[1] if len(row) > 1 else row[0]),
            autor=str(row[2] if len(row) > 2 else row[1]),
            ano_publicacao=int(row[3] if len(row) > 3 else row[2]),
            preco=float(row[4] if len(row) > 4 else row[3])
        )
    
    def __str__(self) -> str:
        """Representação string do livro"""
        return f"{self.titulo} - {self.autor} ({self.ano_publicacao}) - R$ {self.preco:.2f}"
    
    def __repr__(self) -> str:
        """Representação técnica do livro"""
        return f"Livro(id={self.id}, titulo='{self.titulo}', autor='{self.autor}', " \
               f"ano_publicacao={self.ano_publicacao}, preco={self.preco})"