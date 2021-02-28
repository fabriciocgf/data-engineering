## Como executar os testes

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

Adicione o usuario que é utilizado em nosso notebook:
```mysql
CREATE USER 'test'@'localhost' IDENTIFIED BY '1234';
```

se desejar alterar o usuario, deve-se alterar a seguinte string no notebook:
```python
user = 'test:1234'
```
onde o nome de usuario "test" e a senha "1234" devem ser alterados, está definição se encontra na célula de criação de tabelas.

```
certifi==2020.12.5
numpy==1.20.1
pandas==1.2.2
PyMySQL==1.0.2
python-dateutil==2.8.1
pytz==2021.1
six==1.15.0
SQLAlchemy==1.3.23
tqdm==4.58.0
wincertstore==0.2
```

