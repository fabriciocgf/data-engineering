# Como executar os testes

clone este repositório em uma pasta e instale os módulos necessários:
```
numpy==1.20.1
pandas==1.2.2
PyMySQL==1.0.2
python-dateutil==2.8.1
pytz==2021.1
six==1.15.0
SQLAlchemy==1.3.23
tqdm==4.58.0
```
Instale usando o comando:
```
pip install -r requirements.txt
```
O arquivo [logs.txt](https://drive.google.com/open?id=1GliYD4Q19_f6S88iFsn0dk8dGLhB9YXF) foi dividido em duas partes por limitação de tamanho de arquivos no GitHub

## Executando Como Notebook

### Requisitos:
- MySQL server
- Python
- Jupyter Notebook

Inicialmente execute o servidor do MySQL (Windows):
```
"C:\Program Files\MySQL\MySQL Server 8.0\bin\mysqld"
```

Inicie o MySQL shell:
```
mysql -u root -p "your_root_password"
```

Adicione o usuário que é utilizado em nosso notebook:
```mysql
CREATE USER 'test'@'localhost' IDENTIFIED BY '1234';
```

se desejar alterar o usuario, deve-se alterar a seguinte string no notebook:
```python
user = 'test:1234'
```
onde o nome de usuário "test" e a senha "1234" devem ser alterados, está definição se encontra na célula de criação de tabelas.

abrindo-se o shell na pasta onde o projeto foi clonado, o notebook deve ser aberto usando o comando:
```
jupyter notebook ETL-DataEngineer.ipynb
```

Após esses procedimentos execute cada célula do notebook e confira os dados salvos nas pastas services e consumers.

## Executando como Script Python

### Requisitos:
- MySQL server
- Python

Inicialmente execute o servidor do MySQL (Windows):
```
"C:\Program Files\MySQL\MySQL Server 8.0\bin\mysqld"
```

Inicie o MySQL shell:
```
mysql -u root -p "your_root_password"
```

Adicione o usuário que é utilizado em nosso notebook:
```mysql
CREATE USER 'test'@'localhost' IDENTIFIED BY '1234';
```

se desejar alterar o usuário, deve-se alterar a seguinte string no notebook:
```python
user = 'test:1234'
```
onde o nome de usuário "test" e a senha "1234" devem ser alterados.

Para executar o script abra o shell na pasta onde o repositório foi clonado e execute:
```
python etldataeng.py
```
Após a execução do script confira os dados salvos nas pastas services e consumers.

## Visualize o fluxo de pensamento para resolver este desafio

O fluxo pode ser acessado neste link, mas para visualizar de forma melhor como as ideias se relacionam use o software [Obsidian](https://obsidian.md/) onde pode ser visto de melhor forma e até de forma gráfica como as ideias se conectam. abra a pasta docs como um Vault no obsidian.