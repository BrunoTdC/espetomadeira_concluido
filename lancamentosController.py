from models.LancamentosDao import insert_dados, select_dados, excluir_dados, update_dados, update_dados2


def template_to_database(dados):

    dados['data'] = dados['data'].replace('-', '/')
    dd = dados['data'][8:]
    mm = dados['data'][4:8]
    aa = dados['data'][:4]
    data = dd + mm + aa
    dados['data'] = data
    insert_dados(dados)

def template_update_database(dados):
    update_dados2(dados)

def database_to_template():
    dados = select_dados()

    return dados

def excluir_linha(id):
    excluir_dados(id)


def update_linha(id):
    dados = update_dados(id)

    return dados