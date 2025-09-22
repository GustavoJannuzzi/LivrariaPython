# 📚 Sistema de Gerenciamento de Livraria - MVC

> Sistema completo de gerenciamento de livraria com arquitetura MVC, SQLite, CSV e gerenciamento avançado de arquivos.

## 🚀 Visão Geral

Este sistema foi desenvolvido seguindo o padrão arquitetural **MVC (Model-View-Controller)** e implementa **padrões de projeto** como Repository, Service Layer e Dependency Injection para criar uma solução robusta e bem estruturada.

### ✨ Características Principais

- 🏗️ **Arquitetura MVC** bem definida
- 🗄️ **SQLite** para persistência de dados
- 📄 **Importação/Exportação CSV** inteligente
- 💾 **Sistema de backup automático**
- 🔍 **Busca avançada** com múltiplos filtros
- 📊 **Relatórios e estatísticas** detalhados
- 🛡️ **Validação robusta** de dados
- 📝 **Sistema de logs** completo

## 📁 Estrutura do Projeto

```
meu_sistema_livraria/
├── main.py                          # Arquivo principal
├── requirements.txt                  # Dependências
├── README.md                        # Documentação
│
├── models/                          # Camada Model
│   ├── __init__.py
│   └── livro.py                     # Entidade Livro
│
├── views/                           # Camada View
│   ├── __init__.py
│   └── console_view.py              # Interface de console
│
├── controllers/                     # Camada Controller
│   ├── __init__.py
│   └── livraria_controller.py       # Controller principal
│
├── services/                        # Camada de Serviços
│   ├── __init__.py
│   ├── livraria_service.py          # Lógica de negócio
│   └── file_manager.py              # Gerenciamento de arquivos
│
├── database/                        # Camada de Dados
│   ├── __init__.py
│   └── database_manager.py          # Repository e DB Manager
│
└── meu_sistema_livraria/           # Diretório de dados (criado automaticamente)
    ├── data/
    │   └── livraria.db             # Banco SQLite
    ├── backups/                    # Backups automáticos
    ├── exports/                    # Arquivos CSV exportados
    └── logs/                       # Logs do sistema
```

## 🎯 Funcionalidades

### 📖 Gerenciamento de Livros (CRUD)
- ✅ **Adicionar** novos livros
- 📋 **Listar** todos os livros
- 💰 **Atualizar** preços
- 🗑️ **Remover** livros
- 🔍 **Buscar** por autor ou título
- 🔎 **Busca avançada** com filtros múltiplos

### 📊 Relatórios e Estatísticas
- 📈 **Estatísticas gerais** (total, preços, anos)
- 👥 **Top autores** por quantidade
- 💎 **Livros mais caros/baratos**
- 📅 **Distribuição por década**
- 📋 **Relatório completo** formatado

### 💾 Gerenciamento de Dados
- 📤 **Exportação para CSV** com timestamp
- 📥 **Importação de CSV** inteligente
- 🔄 **Backup automático** antes de modificações
- 🗂️ **Limpeza automática** de backups antigos
- 🔧 **Restauração** de backups

### 🛡️ Recursos Avançados
- ✅ **Validação completa** de dados
- 📝 **Sistema de logs** detalhado
- 🔍 **Detecção automática** de delimitadores CSV
- 🚫 **Tratamento robusto** de erros
- 💾 **Context managers** para conexões seguras

## 🚀 Como Executar

```bash
python main.py
```

### Primeira Execução
- O sistema criará automaticamente toda a estrutura de diretórios
- O banco de dados SQLite será inicializado
- Você verá o menu principal com todas as opções

## 🏗️ Arquitetura MVC

### 📋 Model (`models/`)
**Responsabilidade**: Representar dados e regras de negócio

- `Livro`: Entidade principal com validações automáticas
- Validação de dados integrada
- Conversão para diferentes formatos (CSV, dict)

### 👁️ View (`views/`)
**Responsabilidade**: Interface com o usuário

- `ConsoleView`: Interface de console rica e interativa
- Formatação avançada de tabelas
- Mensagens coloridas e informativas
- Coleta de dados validada

### 🎮 Controller (`controllers/`)
**Responsabilidade**: Orquestrar interações entre Model e View

- `LivrariaController`: Controller principal
- Mapeamento de opções do menu
- Tratamento de erros robusto
- Fluxo de controle da aplicação

### 🔧 Services (`services/`)
**Responsabilidade**: Lógica de negócio e orquestração

- `LivrariaService`: Serviço principal de negócio
- `FileManager`: Gerenciamento de arquivos e diretórios
- `CSVManager`: Operações específicas de CSV

### 🗄️ Database (`database/`)
**Responsabilidade**: Acesso e persistência de dados

- `DatabaseManager`: Gerenciador de conexões SQLite
- `LivroRepository`: Padrão Repository para operações CRUD

## 🎨 Padrões de Projeto Implementados

### 🏪 Repository Pattern
- Abstração do acesso a dados
- Interface consistente para operações CRUD
- Facilita testes e manutenção

### 🔧 Service Layer
- Lógica de negócio centralizada
- Orquestração entre diferentes componentes
- Transações e validações complexas

### 🏭 Dependency Injection
- Baixo acoplamento entre componentes
- Facilita testes unitários
- Flexibilidade na configuração

### 🔒 Context Manager
- Gerenciamento seguro de recursos
- Conexões de banco automáticas
- Cleanup garantido

## 📊 Exemplo de Uso

### Adicionando um Livro
```
1. Adicionar novo livro
Título: O Senhor dos Anéis
Autor: J.R.R. Tolkien
Ano: 1954
Preço: 45.90
✅ Livro 'O Senhor dos Anéis' adicionado com sucesso! (ID: 1)
```

### Busca Avançada
```
7. Busca avançada
Autor: Tolkien
Ano mínimo: 1950
Preço máximo: 50.00

BUSCA AVANÇADA - Autor: 'Tolkien' | Ano ≥ 1950 | Preço ≤ R$ 50.00
ID    Título                    Autor           Ano    Preço
1     O Senhor dos Anéis       J.R.R. Tolkien  1954   R$ 45.90
```

## 🔧 Configuração e Customização

### Alterando Diretório Base
```python
# No main.py
controller = LivrariaController("meu_diretorio_personalizado")
```

### Configurando Retenção de Backups
```python
# No file_manager.py, método _limpar_backups_antigos
def _limpar_backups_antigos(self, manter: int = 10):  # Manter 10 em vez de 5
```

## 🧪 Testes e Validação

### Testando Validações
O sistema inclui validações robustas:
- **Anos**: Entre 1000 e ano atual + 1
- **Preços**: Valores positivos
- **Textos**: Campos obrigatórios não vazios
- **CSV**: Detecção automática de formato

### Testando Imports CSV
1. Exporte dados para CSV
2. Modifique o arquivo CSV
3. Importe de volta
4. Verifique logs para erros

## 🐛 Troubleshooting

### Problemas Comuns

**Erro de permissão ao criar diretórios:**
- Verifique permissões de escrita no diretório
- Execute como administrador se necessário

**Banco de dados bloqueado:**
- Feche outras instâncias do programa
- Verifique se há processos SQLite rodando

**Erro ao importar CSV:**
- Verifique formato do arquivo
- Confirme encoding UTF-8
- Veja logs para detalhes específicos

**Performance lenta:**
- Considere reindexar o banco SQLite
- Verifique espaço em disco
- Limpe logs antigos se necessário

## 📝 Logs e Monitoramento

### Sistema de Logs
O sistema mantém logs detalhados em `meu_sistema_livraria/logs/`:

```
sistema_2024-01-15.log
[2024-01-15 10:30:15] INFO: Livro adicionado: Dom Casmurro (ID: 1)
[2024-01-15 10:31:22] INFO: Backup criado: backup_livraria_2024-01-15_10-31-22.db
[2024-01-15 10:35:45] ERROR: Erro ao importar CSV teste.csv: Formato inválido
```

### Monitoramento
- 📊 **Estatísticas** de uso em tempo real
- 🔄 **Histórico** de backups
- ⚡ **Performance** de operações
- 🚨 **Alertas** de erro automáticos

## 🔒 Segurança e Backup

### Estratégia de Backup
1. **Backup automático** antes de cada modificação
2. **Retenção** dos 5 backups mais recentes
3. **Limpeza automática** de arquivos antigos
4. **Restauração** simples via menu

### Integridade dos Dados
- ✅ **Transações SQLite** para consistência
- 🔒 **Context managers** para cleanup
- 🛡️ **Validação** em múltiplas camadas
- 📝 **Logs** para auditoria

## 📚 Documentação da API Interna

### Model: Livro

```python
from models.livro import Livro

# Criar livro
livro = Livro(
    titulo="1984",
    autor="George Orwell", 
    ano_publicacao=1949,
    preco=29.90
)

# Validação automática
livro.validar()  # Levanta ValueError se inválido

# Conversões
dict_livro = livro.to_dict()
csv_row = livro.to_csv_row()
```

### Service: LivrariaService

```python
from services.livraria_service import LivrariaService

service = LivrariaService()

# CRUD operations
livro = service.adicionar_livro("Título", "Autor", 2024, 39.90)
livros = service.buscar_todos_livros()
service.atualizar_preco_livro(1, 45.00)
service.remover_livro(1)

# Operações de arquivo
service.exportar_dados_csv()
service.importar_dados_csv(Path("arquivo.csv"))
service.criar_backup_manual()
```

### Repository: LivroRepository

```python
from database.database_manager import DatabaseManager, LivroRepository

db_manager = DatabaseManager(Path("livraria.db"))
repo = LivroRepository(db_manager)

# Operações de banco
livro = repo.criar(livro_obj)
livros = repo.buscar_todos()
livro = repo.buscar_por_id(1)
repo.atualizar(livro_obj)
repo.deletar(1)
```

## 🎓 Conceitos Educacionais

### Para Estudantes de Programação

Este projeto apresenta conceitos importantes:

**Arquitetura de Software:**
- 🏗️ Separação de responsabilidades (MVC)
- 🔧 Injeção de dependência
- 🎯 Single Responsibility Principle
- 🔒 Encapsulamento

**Padrões de Projeto:**
- 🏪 Repository Pattern
- 🏭 Factory Pattern (implícito)
- 🔧 Service Layer
- 🎯 Strategy Pattern (validações)

**Banco de Dados:**
- 🗄️ SQLite com Python
- 🔒 Context managers
- 📋 CRUD operations
- 🔄 Transações

**Manipulação de Arquivos:**
- 📁 pathlib para caminhos
- 📄 CSV parsing inteligente
- 💾 Backup e restore
- 🗂️ Estrutura de diretórios


### Diretrizes de Código

```python
# Use type hints
def buscar_livro(self, id: int) -> Optional[Livro]:
    pass

# Docstrings descritivas
def validar(self):
    """Valida os dados do livro conforme regras de negócio"""
    pass

# Tratamento de erro robusto
try:
    livro = self.repository.buscar(id)
except DatabaseError as e:
    self.logger.error(f"Erro ao buscar livro: {e}")
    raise ServiceError("Falha na busca") from e
```

## 📞 Suporte

### Obtendo Ajuda

- 📚 **Documentação**: Leia este README completo
- 🐛 **Issues**: Reporte bugs no repositório
- 💡 **Features**: Sugira melhorias
- 📧 **Contato**: Entre em contato para dúvidas

### FAQ

**P: Posso usar outro banco de dados?**
R: Sim! Modifique o `DatabaseManager` para usar PostgreSQL, MySQL, etc.

**P: Como adicionar novos campos ao livro?**
R: Atualize a classe `Livro` e execute migração no banco.

**P: É possível fazer interface gráfica?**
R: Absolutamente! Crie uma nova view (ex: `tkinter_view.py`)

**P: Suporta múltiplos usuários?**
R: Atualmente não, mas pode ser implementado facilmente.

## 📄 Licença

Este projeto foi desenvolvido para fins educacionais. Sinta-se livre para usar, modificar e distribuir conforme necessário para seus estudos e projetos.

---

## 🎉 Conclusão

Este sistema demonstra como construir uma aplicação robusta e bem estruturada usando Python puro. A arquitetura MVC facilita manutenção, testes e extensões futuras.

### 🎯 Objetivos Alcançados

- ✅ **Arquitetura MVC** bem implementada
- ✅ **CRUD completo** com SQLite
- ✅ **Manipulação de arquivos** avançada
- ✅ **Sistema de backup** automático
- ✅ **Importação/Exportação** CSV
- ✅ **Validação robusta** de dados
- ✅ **Interface de usuário** intuitiva
- ✅ **Tratamento de erros** completo
- ✅ **Documentação** detalhada
- ✅ **Padrões de projeto** aplicados

**🚀 Ready to use! Bons estudos e desenvolvimento!** 

---

*Desenvolvido com ❤️ para fins educacionais*