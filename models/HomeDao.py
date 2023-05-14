from models.conexao import sqlite_connector

def select_dados():

    mydb = sqlite_connector()
    cursor = mydb.cursor()

    dinheiro = cursor.execute("""
        select * from lancamentos where formpgm = 'Dinheiro' and pago_banco = 1
    """)

    entradas = 0.0
    saidas = 0.0

    for linha in dinheiro:
        if linha[5] == 'entrada':
            entradas += linha[6]
        else:
            saidas += linha[6]

    total = entradas - saidas

    cursor.execute(f"update dinheiro set valor = {total}")
    

    resultado = cursor.execute("select * from dinheiro")

    dado = 0
    for item in resultado:
        dado = item


    mydb.close()
    return dado

def select_dados_bradesco():

    mydb = sqlite_connector()
    cursor = mydb.cursor()

    dinheiro = cursor.execute("""
        select * from lancamentos where formpgm != 'Dinheiro' and pago_banco = 1
    """)

    entradas = 0.0
    saidas = 0.0

    for linha in dinheiro:
        if linha[5] == 'entrada':
            entradas += linha[6]
        else:
            saidas += linha[6]

    total = entradas - saidas

    cursor.execute(f"update dinheiro set valor = {total}")
    

    resultado = cursor.execute("select * from dinheiro")

    dado = 0
    for item in resultado:
        dado = item


    mydb.close()
    return dado

def update_dados(valor, data):
    mydb = sqlite_connector()
    cursor = mydb.cursor()

    cursor.execute(f"UPDATE dinheiro set valor = {valor}, ultima_atualizacao = '{data}'")
    mydb.commit()
    mydb.close()

def excluir_valor(id):
    mydb = sqlite_connector()
    cursor = mydb.cursor()
    dados = list(cursor.execute(f'SELECT data, valor, tipo from lancamentos where id = "{id}"'))

    if dados[0][2] == "saida":
        valor = list(select_dados())
        valor_atual = float(valor[0])
        valor_update = 0.0
        
        for item in dados:
            valor_update = float(item[1])

        data_update = dados[0][0]
        new_valor = valor_atual + valor_update
        update_dados(new_valor, data_update)

    if dados[0][2] == "entrada":
        valor = list(select_dados())
        valor_atual = float(valor[0])
        valor_update = 0.0
        
        for item in dados:
            valor_update = float(item[1])

        data_update = dados[0][0]
        new_valor = valor_atual - valor_update
        update_dados(new_valor, data_update)

def excluir_valor2(id):
    mydb = sqlite_connector()
    cursor = mydb.cursor()
    dados = list(cursor.execute(f'SELECT data, valor, tipo from lancamentos where id = "{id}"'))

    if dados[0][2] == "entrada":
        valor = list(select_dados())
        valor_atual = float(valor[0])
        valor_update = 0.0
        
        for item in dados:
            valor_update = float(item[1])

        data_update = dados[0][0]
        new_valor = valor_atual - valor_update
        update_dados(new_valor, data_update)

def atualiza_valor(data):
    mydb = sqlite_connector()
    cursor = mydb.cursor()

    cursor.execute("""SELECT l.id,l.data,l.codigo,l.descricao,l.tipo,l.valor,u.usuario
                        from lancamentos as l
                        join usuarios u
                        on l.id_user = u.id
                        WHERE l.pago_banco = 1;

                   """)
    
    resultado = cursor.fetchall()

    entradas = 0.0
    saidas = 0.0
    for item in resultado:
        if item[4] == "entrada":
            entradas += float(item[5])
        else:
            saidas += float(item[5])
    
    valor_update = entradas - saidas
    
    cursor.execute("select * from dinheiro")
    resultado2 = cursor.fetchone()

    data_atual = data
    

    if valor_update != float(resultado2[0]) or data_atual != resultado2[1]:
        update_dados(valor_update, data_atual)
    
    
