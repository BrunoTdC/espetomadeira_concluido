from models.conexao import sqlite_connector

def insert_dados(dados):
    data = dados["data"]
    codigo = dados["codigo"]
    descricao = dados["descricao"]
    forma = dados["formpgm"]
    tipo = dados["tipo"]
    valor = dados["valor"]
    user = dados["user"]
    pago_banco = dados["pago_banco"]
    valor_detalhes = dados["valor_detalhes"]

    mydb = sqlite_connector()
    cursor = mydb.cursor()

    cursor.execute(f'INSERT INTO lancamentos(data,codigo,descricao,formpgm,tipo,valor,id_user,pago_banco, valor_detalhes) VALUES("{data}","{codigo}","{descricao}","{forma}","{tipo}","{valor}","{user}","{pago_banco}","{valor_detalhes}")')
    mydb.commit()
    mydb.close()

def select_dados():

    mydb = sqlite_connector()
    cursor = mydb.cursor()

    resultado = cursor.execute("""SELECT l.id, l.data,l.codigo,l.descricao,l.formpgm,l.tipo,l.valor,u.usuario
                        from lancamentos as l
                        join usuarios u
                        on l.id_user = u.id
                        WHERE l.pago_banco = 0;
                   """)
    return resultado

def excluir_dados(id):
    mydb = sqlite_connector()
    cursor = mydb.cursor()
    cursor.execute(f'DELETE FROM lancamentos where id = "{id}"')
    mydb.commit()
    mydb.close()

def update_dados(id):
    mydb = sqlite_connector()
    cursor = mydb.cursor()
    cursor.execute(f'SELECT id, data, codigo, descricao, formpgm, tipo, valor, valor_detalhes FROM lancamentos where id = "{id}"')
    resultado = cursor.fetchone()
    mydb.close()
    return resultado

def update_dados2(dados):
    id = dados["id"]
    data = dados["data"]
    codigo = dados["codigo"]
    descricao = dados["descricao"]
    forma = dados["formpgm"]
    tipo = dados["tipo"]
    valor = dados["valor"]
    valor_detalhes = dados["valor_detalhes"]

    mydb = sqlite_connector()
    cursor = mydb.cursor()

    cursor.execute(f'UPDATE lancamentos set data = "{data}", codigo = "{codigo}", descricao = "{descricao}",formpgm = "{forma}", tipo = "{tipo}", valor = "{valor}", valor_detalhes = "{valor_detalhes}" WHERE id = "{id}"')
    mydb.commit()
    mydb.close()
