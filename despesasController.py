from models.DespesasDao import select_dados, excluir_dados, update_dados, update_dados2

def despesas_update_database(dados):
    
    try:
        if dados["data"][4] == "-":
            data = dados["data"].replace('-', '/')
            dd = data[8:]
            mm = data[4:8]
            aa = data[:4]
            data = dd + mm + aa
            dados["data"] = data
        
        update_dados2(dados)
    except:
        pass

def database_to_despesas():
    dados = select_dados()

    return dados

def excluir_linha(id):
    excluir_dados(id)

def update_linha(id):
    dados = update_dados(id)

    return dados
