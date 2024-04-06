from flask import Flask,render_template,redirect,request,url_for,flash
import sqlite3 as sql

app = Flask( __name__ )

@app.route('/')
def index():
    banco = sql.connect('vendas.db')
    cursor = banco.cursor()
    cursor.execute("SELECT * FROM cliente")
    data_cliente = cursor.fetchall()
    cursor.execute("SELECT * FROM produto")
    data_produto = cursor.fetchall()
    cursor.execute("SELECT * FROM venda")
    data_venda = cursor.fetchall()
    return render_template('index.html', data_cliente = data_cliente, data_produto = data_produto, data_venda = data_venda)

#-------------------------------------------|Table Cliente|------------------------------------------------
@app.route('/pageAddCliente') 
def pageAddCliente():
    return render_template('add_cliente.html')

@app.route('/add_cliente', methods = ['POST'])
def add_cliente():
    idcliente = request.form['idcliente']
    nome = request.form['nome']
    cidade = request.form['cidade']
    telefone = request.form['telefone']
    email = request.form['email']
    data_nasc = request.form['data_nasc']

    banco = sql.connect('vendas.db')
    cursor = banco.cursor()
    cursor.execute("INSERT INTO cliente VALUES (?,?,?,?,?,?)", (idcliente,nome,cidade,telefone,email,data_nasc))
    banco.commit()
    return redirect(url_for('index'))

@app.route('/edt_cliente/<string:id>', methods = ['GET','POST'])  
def edt_cliente(id):
    if request.method == 'GET':
        banco = sql.connect('vendas.db')
        cursor = banco.cursor()
        cursor.execute("SELECT * FROM cliente WHERE idcliente=?", (id))
        cliente = cursor.fetchone()
        cursor.close()
        return render_template('edt_cliente.html', cliente = cliente)

    elif request.method == 'POST':
        nome = request.form['nome']
        cidade = request.form['cidade']
        telefone = request.form['telefone']
        email = request.form['email']
        data_nasc = request.form['data_nasc']

        banco = sql.connect('vendas.db')
        cursor = banco.cursor()
        cursor.execute("UPDATE cliente SET nome=?, cidade=?, telefone=?, email=?, data_nasc=? WHERE idcliente=?", (nome,cidade,telefone,email,data_nasc,id))
        banco.commit()
        return redirect(url_for('index'))

@app.route('/del_cliente/<string:id>', methods = ['GET'])
def del_cliente(id):
    banco = sql.connect('vendas.db')
    cursor = banco.cursor()
    cursor.execute("DELETE FROM cliente WHERE idcliente=?", (id))
    banco.commit()
    flash('Dados deletados', 'warning')
    return redirect(url_for('index'))

#----------------------------------------------|Table Produto|----------------------------------------------
@app.route('/pageAddProduto') 
def pageAddProduto():
    return render_template('add_produto.html')

@app.route('/add_produto', methods = ['POST'])
def add_produto():
    idproduto = request.form['idproduto']
    nome = request.form['nome']
    preco = request.form['preco']
    marca = request.form['marca']
    categoria = request.form['categoria']
    quant = request.form['quant']

    banco = sql.connect('vendas.db')
    cursor = banco.cursor()
    cursor.execute("INSERT INTO produto VALUES (?,?,?,?,?,?)", (idproduto,nome,preco,marca,categoria,quant))
    banco.commit()
    return redirect(url_for('index'))

@app.route('/edt_produto/<string:id>', methods = ['GET', 'POST'])
def edt_produto(id):
    if request.method == 'GET':
        banco = sql.connect('vendas.db')
        cursor = banco.cursor()
        cursor.execute("SELECT * FROM produto WHERE idproduto=?", (id))
        produto = cursor.fetchone()
        cursor.close()
        return render_template('edt_produto.html', produto = produto)

    elif request.method == 'POST':
        nome = request.form['nome']
        preco = request.form['preco']
        marca = request.form['marca'] 
        categoria = request.form['categoria']
        quant = request.form['quant']

        banco = sql.connect('vendas.db')
        cursor = banco.cursor()
        cursor.execute("UPDATE produto SET nome=?, preco=?, marca=?, categoria=?, quant=? WHERE idproduto=?", (nome,preco,marca,categoria,quant,id))
        banco.commit()
        return redirect(url_for('index'))

@app.route('/del_produto/<string:id>', methods = ['GET'])
def del_produto(id):
    banco = sql.connect('vendas.db')
    cursor = banco.cursor()
    cursor.execute("DELETE FROM produto WHERE idproduto=?", (id))
    banco.commit()
    flash('Dados deletados', 'warning')
    return redirect(url_for('index'))

#----------------------------------------------|Table Venda|----------------------------------------------
@app.route('/pageAddVenda')
def pageAddVenda():
    return render_template('add_venda.html')

@app.route('/add_venda', methods = ['POST'])
def add_venda():
    idvenda = request.form['idvenda']
    data_venda = request.form['data_venda'] 
    valor_total = request.form['valor_total']
    funcionario = request.form['funcionario']
    idcliente = request.form['idcliente']
    idproduto = request.form['idproduto']

    banco = sql.connect('vendas.db')
    cursor = banco.cursor()
    cursor.execute("SELECT idcliente FROM cliente")
    dataCliente = [numero for tupla in cursor.fetchall() for numero in tupla]
    cursor.execute("SELECT idproduto FROM produto")
    dataProduto = [numero for tupla in cursor.fetchall() for numero in tupla]

    idcliente_temp = int(idcliente)
    idproduto_temp = int(idproduto)

    if idcliente_temp in dataCliente and idproduto_temp in dataProduto:
        cursor.execute("INSERT INTO venda VALUES(?,?,?,?,?,?)", (idvenda,data_venda,valor_total,funcionario,idcliente,idproduto))
        banco.commit()
        return redirect(url_for('index'))
    else:
        return 'ID do Cliente ou ID do Produto não existente, por favor digite novamente.'

@app.route('/edt_venda/<string:id>', methods = ['GET', 'POST'])
def edt_venda(id):
    if request.method == 'GET':
        banco = sql.connect('vendas.db')
        cursor = banco.cursor()
        cursor.execute("SELECT * FROM venda WHERE idvenda=?", (id))
        venda = cursor.fetchone()
        cursor.close()
        return render_template('edt_venda.html', venda = venda)
    
    elif request.method == 'POST':
        data_venda = request.form['data_venda']
        valor_total = request.form['valor_total']
        funcionario = request.form['funcionario']
        idcliente = request.form['idcliente']
        idproduto = request.form['idproduto']

        banco = sql.connect('vendas.db')
        cursor = banco.cursor()
        cursor.execute("SELECT idcliente FROM cliente")
        dataCliente = [numero for tupla in cursor.fetchall() for numero in tupla]
        cursor.execute("SELECT idproduto FROM produto")
        dataProduto = [numero for tupla in cursor.fetchall() for numero in tupla]
        
        idcliente_temp = int(idcliente)
        idproduto_temp = int(idproduto)

        if idcliente_temp in dataCliente and idproduto_temp in dataProduto:
            cursor.execute("UPDATE venda SET data_venda=?, valor_total=?, funcionario=?, idcliente=?, idproduto=? WHERE idvenda=?", (data_venda,valor_total,funcionario,idcliente,idproduto,id))
            banco.commit()
            return redirect(url_for('index'))
        else:
            return 'ID do Cliente ou ID do Produto não existente, por favor digite novamente.'

@app.route('/del_venda/<string:id>', methods = ['GET'])
def del_venda(id):
    banco = sql.connect('vendas.db')
    cursor = banco.cursor()
    cursor.execute("DELETE FROM venda WHERE idvenda=?", (id))
    banco.commit()
    flash('Dados deletados', 'warning')
    return redirect(url_for('index'))

if  __name__ == '__main__':
    app.secret_key = 'admin123'
    app.run(debug=True)