from models.conexao import sqlite_connector

def cria_tabelas():

    mydb = sqlite_connector()

    cursor = mydb.cursor()

    cria_tabela_usuario = """CREATE TABLE IF NOT EXISTS usuarios(
                                id integer primary key autoincrement,
                                usuario text unique,
                                senha text
                            )"""

    cria_tabela_lancamentos = """CREATE TABLE IF NOT EXISTS lancamentos(
                                    id integer primary key autoincrement,
                                    data text,
                                    codigo text,
                                    descricao text,
                                    formpgm text,
                                    tipo text,
                                    valor real,
                                    id_user integer,
                                    pago_banco integer,
                                    FOREIGN KEY(id_user) REFERENCES usuarios(id)
                                )"""
    
    cria_tabela_dinheiro = """CREATE TABLE IF NOT EXISTS dinheiro(
                                valor REAL,
                                ultima_atualizacao TEXT
    )"""


    cursor.execute(cria_tabela_dinheiro)
    mydb.commit()

    cursor.execute("select * from dinheiro")

    
    if len(list(cursor.fetchall())) == 0:
        cursor.execute("insert into dinheiro values(0.0, '-')")

    cursor.execute(cria_tabela_usuario)
    mydb.commit()

    cursor.execute(cria_tabela_lancamentos)
    mydb.commit()



    mydb.close()
