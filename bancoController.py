from models.BancoDao import select_dados,update_dados


def database_to_banco():
    dados = select_dados()

    return dados

def banco_update_database(dados):
    if not dados['pago']:
        dados['pago'] = 0

    update_dados(dados)