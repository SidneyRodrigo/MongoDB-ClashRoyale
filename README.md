# MongoDB-ClashRoyale

Este projeto armazena dados de batalhas de Clash Royale da base de dados em um banco de dados MongoDB e realiza consultas analíticas para auxiliar no balanceamento do jogo. O projeto está dividido em dois arquivos principais:

- **database.py**: Cria o banco de dados e insere os dados das batalhas.
- **queries.py**: Executa consultas sobre os dados armazenados.

## Requisitos

- **Python 3.8 ou superior**
- **Bibliotecas Python**:
  - `pandas`
  - `pymongo`
  
  Você pode instalar as dependências usando o seguinte comando:

```bash
pip install pandas pymongo dnspython
```

- Conta no MongoDB Atlas: Se você ainda não tem uma conta, clique aqui para criar uma gratuitamente e configurar o cluster.

## Configuração

### Passo 1: Clone o repositório

```bash
git clone https://github.com/Ioshua-N/projeto-mongodb-clash-royale.git
cd projeto-mongodb-clash-royale
```

### Passo 2: Crie o banco de dados e insira os dados

1. Abra o arquivo database.py e insira sua url do MongoDB Atlas na variável uri.
2. Adicione o caminho correto para o seu arquivo CSV no código do database.py.
3. Rode o arquivo database.py para criar o banco de dados e inserir os dados das batalhas no MongoDB:
   
   ```bash
   python database.py
   ```

Se tudo estiver correto, a saída será:

```bash
Pinged your deployment. You successfully connected to MongoDB!
Arquivo .csv carregado com sucesso!
Banco criado e dados inseridos com sucesso!
```

### Passo 3: Execute as consultas
Agora que os dados foram inseridos, você pode rodar as consultas no arquivo queries.py.

1. Abra o arquivo queries.py e configure os parâmetros das consultas conforme necessário.
2. Execute o script para ver os resultados das consultas:
   ```bash
   python queries.py
   ```
   Exemplo de saída:
   ```bash
   Porcentagem de vitórias com a carta 26000000: 52.35%
   Decks com mais de 50.0% de vitórias: [...]
   Quantidade de derrotas com o combo de cartas [26000000, 26000010]: 123
   Vitórias com 20% menos troféus, duração < 2 minutos, e 2 torres derrubadas: 5
   Combos de cartas com mais de 60.0% de vitórias: [...]
   ```
### Estrutura dos Arquivos
- `database.py`: Responsável por conectar ao MongoDB Atlas, carregar o arquivo CSV e inserir os dados no banco.
- `queries.py`: Contém consultas analíticas que você pode alterar conforme o que deseja analisar.

## Conclusão
Este projeto permite realizar análises úteis para o balanceamento de jogos de cartas, como Clash Royale, utilizando um banco de dados MongoDB. Sinta-se à vontade para expandir o projeto com novas consultas e análises!
