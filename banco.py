import sqlite3 as sql

banco = sql.connect('vendas.db')
cursor = banco.cursor()

cursor.execute('''CREATE TABLE IF NOT EXISTS cliente (
               idcliente INTEGER PRIMARY KEY, 
               nome TEXT,  
               cidade TEXT, 
               telefone INTEGER, 
               email TEXT,
               data_nasc DATE
               )''')

cursor.execute('''CREATE TABLE IF NOT EXISTS produto (
               idproduto INTEGER PRIMARY KEY, 
               nome TEXT, 
               preco REAL, 
               marca TEXT,
               categoria TEXT,
               quant INTEGER
               )''')

cursor.execute('''CREATE TABLE IF NOT EXISTS venda (
               idvenda INTEGER PRIMARY KEY, 
               data_venda DATE, 
               valor_total REAL, 
               funcionario TEXT,
               idcliente INTEGER, 
               idproduto INTEGER, 

               FOREIGN KEY (idcliente) REFERENCES cliente(idcliente), 
               FOREIGN KEY (idproduto) REFERENCES produto(idproduto)
               )''')

banco.execute("DELETE FROM venda WHERE idvenda > 1")
banco.commit()
banco.close()