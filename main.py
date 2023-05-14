from flask import Flask, render_template, request, session, redirect, url_for
from datetime import datetime
import pdfkit
#from models.conexao import mysql_connector
import sqlite3
from models.database import cria_tabelas
import lancamentosController, bancoController, despesasController, homeController, imprimePDF

app = Flask(__name__)
app.secret_key = "super_secret_key"

cria_tabelas()

# TELA DE LOGIN -------------------------------------------------------------------------------------------
@app.route('/', methods=['GET', 'POST'])
def index():

    if request.method == 'POST':
        usuario = request.form['u']
        senha = request.form['p']

        mydb = sqlite3.connect('espeto_madeira.db')

        #mydb = mysql_connector()
        cursor = mydb.cursor()
        cursor.execute(f'select * from usuarios where usuario = "{usuario}" and senha = "{senha}"')
        user = cursor.fetchone()

        if user:
            session['user_id'] = user[0]
            session['username'] = user[1]
            return redirect(url_for('home'))
        else:
            return render_template("index.html", verifica=True)

    return render_template("index.html")

# FIM DA TELA DE LOGIN -------------------------------------------------------------------------------------------

# LOGOUT --------------------------------------

@app.route('/logout', methods=['GET', 'POST'])
def logout():
    session.clear()
    return redirect(url_for('index'))

# FIM LOGOUT --------------------------------------

# TELA HOME -------------------------------------------------------------------------------------------

@app.route('/home.html', methods=["GET", "POST"])
def home():
    if 'user_id' in session:
        dados = homeController.database_to_home()
        dados_bradesco = homeController.database_to_home_bradesco()
        return render_template("home.html", dados = dados, dados_bradesco = dados_bradesco)
    else:
        return redirect(url_for('index'))

# FIM TELA HOME ----------------------------------------------------------------------------------------

# IMPRESSOES --------------------------------------------------------------------------------------------

@app.route('/pdf', methods=["GET", "POST"])
def pdf():

    if request.method == "POST":
        datainicio = datetime.strptime(request.form.get("datainicio"), '%Y-%m-%d')
        datafim = datetime.strptime(request.form.get("datafim"), '%Y-%m-%d')
        
        dados = imprimePDF.pdf(datainicio, datafim)
        total = 0.0
        for linha in dados:
            if linha["tipo"] == "entrada":
                total += linha["valor"]
            else:
                total -= linha["valor"]
            print(linha)

        total = f'R$ {total:,.2f}'
        total = total.replace(",", "/")
        total = total.replace(".", ",")
        total = total.replace("/", ".")

        return render_template("to_pdf.html", dados = dados, total = total)

    if 'user_id' in session:
        
        return redirect(url_for('home'))
    else:
        return redirect(url_for('index'))

# FIM IMPRESSOES ----------------------------------------------------------------------------------------
# FILTRAR IMPRESSOES --------------------------------------------------------------------------------------------

@app.route('/filter', methods=["GET", "POST"])
def filter():

    def dict_factory(cursor, row):
        d = {}
        for idx, col in enumerate(cursor.description):
            d[col[0]] = row[idx]
        return d

    if request.method == "POST":
       
        codigo = request.form['codigo']
        forma = request.form['forma']
        
        mydb = sqlite3.connect('espeto_madeira.db')

        cursor = mydb.cursor()
        
        cursor.row_factory = dict_factory
        cursor.execute(f"""select 
                        l.data, c.codigo, c.codigo || ' - ' || c.nome as nome, l.descricao, l.formpgm, l.tipo, l.valor, u.usuario 
                    from lancamentos as l
                    join usuarios as u
                    on l.id_user = u.id
                    join codigos as c
                    on l.codigo = c.codigo
                 where l.codigo = '{codigo}' or formpgm = '{forma}'""")
        

        filter1 = cursor.fetchall()

        for linha in filter1:
            print(linha)
        
        total = 0.0
        for linha in filter1:
            if linha['tipo'] == "entrada":
                total += linha['valor']
            else:
                total -= linha['valor']
                print(linha)

        total = f'R$ {total:,.2f}'
        total = total.replace(",", "/")
        total = total.replace(".", ",")
        total = total.replace("/", ".")
        
      
        return render_template("filter.html",total = total, filter1 = filter1)

    if 'user_id' in session:
        
        return redirect(url_for('home'))
    else:
        return redirect(url_for('index'))

# FIM FILTRAR IMPRESSOES ----------------------------------------------------------------------------------------
# TELA DE LANCAMENTO ----------------------------------------------

@app.route('/lancamentos.html', methods=["GET", "POST"])
def lancamentos():

    if request.method == "POST":
        dados = (
            {"data": request.form.get("data"),
             "codigo": request.form.get("codigo"),
             "descricao": request.form.get("descricao"),
             "formpgm": request.form.get("forma"),
             "tipo": request.form.get("tipo"),
             "valor": eval(request.form.get("valor").replace(",",".")),
             "user": session['user_id'],
             "pago_banco" : 0,
             "valor_detalhes": request.form.get("valor"),
            })
        

        lancamentosController.template_to_database(dados)

        result = lancamentosController.database_to_template()

        return render_template("lancamentos.html", result = result)

    if 'user_id' in session:
        result = lancamentosController.database_to_template()
        return render_template("lancamentos.html", result = result)
    else:
        return redirect(url_for('index'))

@app.route('/update', methods=['GET', 'POST'])
def update():

    if request.method == "POST":
        id = request.form.get("id")
        dados = lancamentosController.update_linha(id)

        return render_template("update.html", dados=dados)

    if not 'user_id' in session:
        return redirect(url_for('index'))

@app.route('/update2', methods=['GET', 'POST'])
def update2():
    if request.method == "POST":
        dados = (
            {"id": request.form.get("id"),
             "data": request.form.get("data"),
             "codigo": request.form.get("codigo"),
             "descricao": request.form.get("descricao"),
             "formpgm": request.form.get("forma"),
             "tipo": request.form.get("tipo"),
             "valor": eval(request.form.get("valor").replace(",",".")),
             "valor_detalhes": request.form.get("valor"),
            })
        lancamentosController.template_update_database(dados)
    return redirect(url_for('lancamentos'))

@app.route('/excluir', methods=['GET', 'POST'])
def excluir():


    if request.method == "POST":

        id = request.form.get("id")
        lancamentosController.excluir_linha(id)
        
        return redirect(url_for('lancamentos'))

    if 'user_id' in session:
        return redirect(url_for('excluir'))
    else:
        return redirect(url_for('index'))

# FIM TELA DE LANCAMENTO ----------------------------------------------

# TELA DE DESPESAS ----------------------------------------------------

@app.route('/despesas.html', methods=['GET', 'POST'])
def despesas():

    if request.method == "POST":
        dados = (
            {"data": request.form.get("data"),
             "codigo": request.form.get("codigo"),
             "descricao": request.form.get("descricao"),
             "formpgm": request.form.get("forma"),
             "tipo": request.form.get("tipo"),
             "valor": request.form.get("valor"),
             "user": session['user_id'],
             "pago_banco" : 0,
            })
        
        return render_template("despesas.html", result = result)

    if 'user_id' in session:
        result = despesasController.database_to_despesas()

        return render_template("despesas.html", result = result)
    else:
        return redirect(url_for('index'))

@app.route('/updateDespesas', methods=['GET', 'POST'])
def updateDespesas():

    if request.method == "POST":
        id = request.form.get("id")
        
        dados = despesasController.update_linha(id)
        return render_template("updateDespesas.html", dados=dados)

    if not 'user_id' in session:
        return redirect(url_for('index'))

@app.route('/updateDespesas2', methods=['GET', 'POST'])
def updateDespesas2():
    if request.method == "POST":
        dados = (
            {"id": request.form.get("id"),
             "data": request.form.get("data"),
             "codigo": request.form.get("codigo"),
             "descricao": request.form.get("descricao"),
             "formpgm": request.form.get("forma"),
             "tipo": request.form.get("tipo"),
             "valor": eval(request.form.get("valor").replace(",",".")),
             "valor_detalhes": request.form.get("valor"),
            })
        nova_data = dados["data"]
        despesasController.despesas_update_database(dados)
        homeController.atualiza_valor_update(nova_data)
    return redirect(url_for('despesas'))

@app.route('/excluirDespesas', methods=['GET', 'POST'])
def excluirDespesas():

    if request.method == "POST":
        id = request.form.get("id")
        homeController.exclusao_valor(id)
        despesasController.excluir_linha(id)
        return redirect(url_for('despesas'))

    if 'user_id' in session:
        return redirect(url_for('excluirDespesas'))
    else:
        return redirect(url_for('index'))

# FIM TELA DE DESPESAS ------------------------------------------------

# CONFIRMAÇÕES --------------------------------------------------------------------------------------------
@app.route('/confirma', methods=['GET', 'POST'])
def confirma():
    id = request.form.get("id")

    if 'user_id' in session:
        return render_template("confirma.html", id=id)
    else:
        if request.method == 'POST':
            id = request.form.get("id")
            
            return redirect(url_for('excluirDespesas'))
    

    
    
# FIM CONFIRMAÇÕES ----------------------------------------------------------------------------------------

# TELA DE BANCO -------------------------------------------------------

@app.route('/banco.html', methods=['GET', 'POST'])
def banco():

    if request.method == "POST":
        dados = (
            {"id": request.form.get("id"),
             "pago": request.form.get("check"),
             "tipo": request.form.get("tipo"),
             "valor": request.form.get("valor"),
             "data": request.form.get("data"),
            })
        
        if dados["tipo"] == "saida":
            homeController.update_home(float(dados["valor"]), dados["data"])

        if dados["tipo"] == "entrada":
            homeController.update_home2(float(dados["valor"]), dados["data"])

        bancoController.banco_update_database(dados)
        result = bancoController.database_to_banco()
        return render_template("banco.html", result = result)

    if 'user_id' in session:
        result = bancoController.database_to_banco()
        return render_template("banco.html", result = result)
    else:
        return redirect(url_for('index'))

# FIM TELA DE BANCO ---------------------------------------------------

cria_tabelas()

if __name__ == "__main__":
    app.run(debug=True)