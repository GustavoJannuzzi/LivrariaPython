"""
Serviço para gerenciamento de arquivos, backups e operações CSV
Implementa o padrão Service para lógica de negócio relacionada a arquivos
"""
import csv
import os
import shutil
from datetime import datetime
from pathlib import Path
from typing import List, Optional

from models.livro import Livro

class FileManager:
    """Gerenciador de arquivos e diretórios do sistema"""
    
    def __init__(self, base_dir: str = "meu_sistema_livraria"):
        self.base_dir = Path(base_dir)
        self.data_dir = self.base_dir / "data"
        self.backups_dir = self.base_dir / "backups"
        self.exports_dir = self.base_dir / "exports"
        self.logs_dir = self.base_dir / "logs"
        
        self._criar_estrutura_diretorios()
    
    def _criar_estrutura_diretorios(self):
        """Cria a estrutura de diretórios necessária"""
        directories = [self.data_dir, self.backups_dir, self.exports_dir, self.logs_dir]
        
        for directory in directories:
            os.makedirs(directory, exist_ok=True)
    
    def get_database_path(self) -> Path:
        """Retorna o caminho do banco de dados"""
        return self.data_dir / "livraria.db"
    
    def criar_backup(self, source_path: Optional[Path] = None) -> Optional[Path]:
        """Cria um backup do banco de dados"""
        if source_path is None:
            source_path = self.get_database_path()
        
        if not source_path.exists():
            return None
        
        timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
        backup_path = self.backups_dir / f"backup_livraria_{timestamp}.db"
        
        try:
            shutil.copy2(source_path, backup_path)
            self._limpar_backups_antigos()
            return backup_path
        except Exception as e:
            self._log_error(f"Erro ao criar backup: {e}")
            return None
    
    def _limpar_backups_antigos(self, manter: int = 5):
        """Mantém apenas os N backups mais recentes"""
        try:
            backups = list(self.backups_dir.glob("backup_livraria_*.db"))
            backups.sort(key=lambda x: x.stat().st_mtime, reverse=True)
            
            for backup in backups[manter:]:
                backup.unlink()
                self._log_info(f"Backup antigo removido: {backup.name}")
                
        except Exception as e:
            self._log_error(f"Erro ao limpar backups: {e}")
    
    def listar_backups(self) -> List[Path]:
        """Lista todos os backups disponíveis"""
        backups = list(self.backups_dir.glob("backup_livraria_*.db"))
        return sorted(backups, key=lambda x: x.stat().st_mtime, reverse=True)
    
    def restaurar_backup(self, backup_path: Path) -> bool:
        """Restaura um backup específico"""
        if not backup_path.exists():
            return False
        
        try:
            # Fazer backup do banco atual antes de restaurar
            self.criar_backup()
            
            # Restaurar o backup
            db_path = self.get_database_path()
            shutil.copy2(backup_path, db_path)
            
            self._log_info(f"Backup restaurado: {backup_path.name}")
            return True
            
        except Exception as e:
            self._log_error(f"Erro ao restaurar backup: {e}")
            return False
    
    def _log_info(self, message: str):
        """Registra uma mensagem de informação"""
        self._write_log("INFO", message)
    
    def _log_error(self, message: str):
        """Registra uma mensagem de erro"""
        self._write_log("ERROR", message)
    
    def _write_log(self, level: str, message: str):
        """Escreve uma mensagem no log"""
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        log_entry = f"[{timestamp}] {level}: {message}\n"
        
        log_file = self.logs_dir / f"sistema_{datetime.now().strftime('%Y-%m-%d')}.log"
        
        try:
            with open(log_file, 'a', encoding='utf-8') as f:
                f.write(log_entry)
        except Exception:
            pass  # Se não conseguir escrever no log, ignora silenciosamente


class CSVManager:
    """Gerenciador para operações de importação e exportação CSV"""
    
    def __init__(self, file_manager: FileManager):
        self.file_manager = file_manager
    
    def exportar_livros(self, livros: List[Livro], nome_arquivo: Optional[str] = None) -> Optional[Path]:
        """Exporta uma lista de livros para CSV"""
        if not livros:
            return None
        
        if nome_arquivo is None:
            timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
            nome_arquivo = f"livros_exportados_{timestamp}.csv"
        
        csv_path = self.file_manager.exports_dir / nome_arquivo
        
        try:
            with open(csv_path, 'w', newline='', encoding='utf-8') as csvfile:
                writer = csv.writer(csvfile, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
                
                # Escrever cabeçalho
                writer.writerow(['ID', 'Título', 'Autor', 'Ano de Publicação', 'Preço'])
                
                # Escrever dados dos livros
                for livro in livros:
                    writer.writerow(livro.to_csv_row())
            
            self.file_manager._log_info(f"Exportação CSV concluída: {csv_path.name}")
            return csv_path
            
        except Exception as e:
            self.file_manager._log_error(f"Erro ao exportar CSV: {e}")
            return None
    
    def importar_livros(self, csv_path: Path) -> List[Livro]:
        """Importa livros de um arquivo CSV"""
        if not csv_path.exists():
            raise FileNotFoundError(f"Arquivo não encontrado: {csv_path}")
        
        livros = []
        linhas_com_erro = []
        
        try:
            with open(csv_path, 'r', newline='', encoding='utf-8') as csvfile:
                # Detectar automaticamente o delimitador
                sample = csvfile.read(1024)
                csvfile.seek(0)
                
                sniffer = csv.Sniffer()
                delimiter = sniffer.sniff(sample).delimiter
                
                reader = csv.reader(csvfile, delimiter=delimiter)
                
                # Pular cabeçalho se existir
                primeira_linha = next(reader, None)
                if primeira_linha and self._is_header(primeira_linha):
                    pass  # Já pulou o cabeçalho
                else:
                    # Se não for cabeçalho, processar como dados
                    if primeira_linha:
                        try:
                            livro = Livro.from_csv_row(primeira_linha)
                            livros.append(livro)
                        except Exception as e:
                            linhas_com_erro.append((1, primeira_linha, str(e)))
                
                # Processar o restante das linhas
                for linha_num, linha in enumerate(reader, start=2):
                    if not linha or all(not cell.strip() for cell in linha):
                        continue  # Pular linhas vazias
                    
                    try:
                        livro = Livro.from_csv_row(linha)
                        livros.append(livro)
                    except Exception as e:
                        linhas_com_erro.append((linha_num, linha, str(e)))
            
            # Log de erros se houver
            if linhas_com_erro:
                error_msg = f"Erros na importação de {csv_path.name}:\n"
                for linha_num, linha, erro in linhas_com_erro:
                    error_msg += f"  Linha {linha_num}: {linha} - {erro}\n"
                self.file_manager._log_error(error_msg)
            
            self.file_manager._log_info(
                f"Importação CSV: {len(livros)} livros importados, {len(linhas_com_erro)} erros"
            )
            
            return livros
            
        except Exception as e:
            self.file_manager._log_error(f"Erro ao importar CSV {csv_path.name}: {e}")
            raise
    
    def _is_header(self, linha: List[str]) -> bool:
        """Verifica se uma linha é um cabeçalho"""
        if not linha:
            return False
        
        # Indicadores comuns de cabeçalho
        headers_indicators = ['id', 'título', 'title', 'autor', 'author', 'ano', 'year', 'preço', 'price']
        primeira_celula = linha[0].lower().strip()
        
        return any(indicator in primeira_celula for indicator in headers_indicators)
    
    def listar_arquivos_csv(self) -> List[Path]:
        """Lista todos os arquivos CSV disponíveis para importação"""
        return list(self.file_manager.exports_dir.glob("*.csv"))
    
    def validar_arquivo_csv(self, csv_path: Path) -> dict:
        """Valida um arquivo CSV e retorna informações sobre ele"""
        if not csv_path.exists():
            return {'valido': False, 'erro': 'Arquivo não encontrado'}
        
        try:
            with open(csv_path, 'r', newline='', encoding='utf-8') as csvfile:
                sample = csvfile.read(1024)
                csvfile.seek(0)
                
                # Detectar delimitador
                sniffer = csv.Sniffer()
                delimiter = sniffer.sniff(sample).delimiter
                
                reader = csv.reader(csvfile, delimiter=delimiter)
                linhas = list(reader)
                
                if not linhas:
                    return {'valido': False, 'erro': 'Arquivo vazio'}
                
                # Contar linhas válidas
                linhas_validas = 0
                tem_cabecalho = self._is_header(linhas[0])
                inicio = 1 if tem_cabecalho else 0
                
                for linha in linhas[inicio:]:
                    if linha and len(linha) >= 4:  # Pelo menos título, autor, ano, preço
                        linhas_validas += 1
                
                return {
                    'valido': True,
                    'total_linhas': len(linhas),
                    'linhas_validas': linhas_validas,
                    'tem_cabecalho': tem_cabecalho,
                    'delimitador': delimiter,
                    'tamanho_arquivo': csv_path.stat().st_size
                }
                
        except Exception as e:
            return {'valido': False, 'erro': str(e)}