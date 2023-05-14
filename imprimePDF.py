from datetime import datetime
import sqlite3

conn = sqlite3.connect('espeto_madeira.db', check_same_thread=False)
cursor = conn.cursor()

def dict_factory(cursor, row):
    d = {}
    for idx, col in enumerate(cursor.description):
        d[col[0]] = row[idx]
    return d

def pdf(datainicio, datafim):

    if datainicio > datafim:
        troca = datainicio
        datainicio = datafim
        datafim = troca

    cursor.row_factory = dict_factory
    cursor.execute("""select 
                        l.data, c.codigo || ' - ' || c.nome as nome, l.descricao, l.formpgm, l.tipo, l.valor, u.usuario 
                    from lancamentos as l
                    join usuarios as u
                    on l.id_user = u.id
                    join codigos as c
                    on l.codigo = c.codigo
                """)

    dados = cursor.fetchall()

    result = []
    
    for linha in dados:
        ...
        linha["data"] = datetime.strptime(linha["data"], '%d/%m/%Y')

    for item in dados:
                
        if item["data"] >= datainicio and item["data"] <= datafim:
            result.append(item)
            
    return result