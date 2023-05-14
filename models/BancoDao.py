from models.conexao import sqlite_connector

def select_dados():

    mydb = sqlite_connector()
    cursor = mydb.cursor()

    cursor.execute("""SELECT l.id,l.data,l.codigo,l.descricao,l.formpgm,l.tipo,l.valor,u.usuario
                        from lancamentos as l
                        join usuarios u
                        on l.id_user = u.id
                        WHERE l.pago_banco = 0;

                   """)

    resultado = cursor.fetchall()
    mydb.close()
    return resultado

def update_dados(dados):
    id = dados['id']
    pago = dados['pago']

    mydb = sqlite_connector()
    cursor = mydb.cursor()

    cursor.execute(f'UPDATE lancamentos SET pago_banco = "{pago}" WHERE id = "{id}"')
    mydb.commit()
    mydb.close()