# MongoDB-ClashRoyale

Este projeto armazena dados de batalhas de Clash Royale da base de dados em um banco de dados MongoDB e realiza consultas analíticas para auxiliar no balanceamento do jogo. O projeto está dividido em dois arquivos principais:

- **database.py**: Cria o banco de dados e insere os dados das batalhas.
- **queries.py**: Executa consultas sobre os dados armazenados.

## Requisitos

- **Python 3.8 ou superior**
- **Bibliotecas Python**:
  - `pandas`
  - `pymongo`
  - `dnspython` (para conexão com MongoDB Atlas)
  
  Você pode instalar as dependências usando o seguinte comando:

```bash
pip install pandas pymongo dnspython
```
