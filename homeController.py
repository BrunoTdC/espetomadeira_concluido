from models.HomeDao import select_dados, select_dados_bradesco, update_dados, excluir_valor, excluir_valor2, atualiza_valor


def database_to_home():
    dados = list(select_dados())
    valor = dados[0]
    valor1 = f'R$ {valor:,.2f}'
    valor1 = valor1.replace(",", "/")
    valor1 = valor1.replace(".", ",")
    valor1 = valor1.replace("/", ".")
    dados[0] = valor1
    return dados

def database_to_home_bradesco():
    dados = list(select_dados_bradesco())
    valor = dados[0]
    valor1 = f'R$ {valor:,.2f}'
    valor1 = valor1.replace(",", "/")
    valor1 = valor1.replace(".", ",")
    valor1 = valor1.replace("/", ".")
    dados[0] = valor1
    return dados


def update_home(valor, data):
    dados = select_dados()
    valor_atual = dados[0]

    if data[4] == "-":
        data = data.replace('-', '/')
        dd = data[8:]
        mm = data[4:8]
        aa = data[:4]
        data = dd + mm + aa

    valor_update = valor_atual - valor

    update_dados(valor_update, data)

def update_home2(valor, data):
    dados = select_dados()
    valor_atual = dados[0]

    if data[4] == "-":
        data = data.replace('-', '/')
        dd = data[8:]
        mm = data[4:8]
        aa = data[:4]
        data = dd + mm + aa

    valor_update = valor_atual + valor

    update_dados(valor_update, data)

def exclusao_valor(id):
    excluir_valor(id)

def exclusao_valor2(id):
    excluir_valor2(id)

def atualiza_valor_update(data):
    atualiza_valor(data)
