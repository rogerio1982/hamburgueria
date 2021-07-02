#CRUD LOCAL 
#venv python 2

from flask import Flask, json, render_template, request, url_for, redirect, session
from flask_sqlalchemy import SQLAlchemy
import datetime
from random import choice
import string
from sqlalchemy.sql import func
from flask import jsonify, jsonify, make_response
from flask_cors import CORS, cross_origin
import os
from os.path import join, dirname, realpath
from werkzeug.utils import secure_filename
from sqlalchemy.sql import select


app = Flask(__name__)
CORS(app)
app.config["DEBUG"] = True
app.secret_key = "any random string"


app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///hamburgueria2.db'


db = SQLAlchemy(app)

class prod(db.Model):
    __tablename__ = "produtos"
    ID = db.Column(db.Integer, primary_key=True)
    id_cat = db.Column(db.String(4096))
    Nome = db.Column(db.String(4096))
    desc = db.Column(db.String(4096))
    valor = db.Column(db.Float(100))
    imagens = db.Column(db.String(100))

class pedidos(db.Model):
    __tablename__ = "pedidos"
    ID = db.Column(db.Integer, primary_key=True)
    id_venda = db.Column(db.Integer)
    produtos = db.Column(db.String(4096))
    valor = db.Column(db.Float(100))
    qtd = db.Column(db.Integer)
    sub_total = db.Column(db.Float(100))
    data = db.Column(db.DateTime)

class emp(db.Model):
    __tablename__ = "empresa"
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(4096))
    tel = db.Column(db.String(4096))
    imagens = db.Column(db.String(4096))
    login = db.Column(db.String(4096))
    senha = db.Column(db.String(4096))
    
class cat(db.Model):
    __tablename__ = "categoria"
    id = db.Column(db.Integer, primary_key=True)
    categoria = db.Column(db.String(4096))
  
    
      
      
#finalizar pedidos
@app.route("/index", methods=["GET"])
def in0nde():

    return render_template("index.html")      



#principal http://192.168.0.106:5000/2?id_emp=2&id_cat=all 
@app.route("/", methods=["GET"])
def get_product_by_id():    
    
    if not session.get('username'): #if 'username' not in session:
        
        string.ascii_lowercase # abcdefghijklmnopqrstuvwxyz
        string.ascii_uppercase # ABCDEFGHIJKLMNOPQRSTUVWXYZ
        tam = 10
        valores = string.ascii_lowercase + string.ascii_uppercase
        
        #id = empr# 
        #session['emp'] = id #empresa
        

        senha = ''
        for i in range(tam):
            senha += choice(valores)
        
        x = datetime.datetime.now()
        

        session['username'] = senha #last_item
        session['time'] = x #last_item
        
        #senha = session['username']
        #dados = prod.query.filter_by(id_emp=id).all()
        #dados2 = emp.query.filter_by(id=id).all()
        #return render_template("listpedidos.html",a=dados, b=dados2,emp=id, senha=senha)
    
    
    senha = session['username']
    print("senha"+senha)
    dados2 = emp.query.all()
    
    
   # if (cate=='all'):
    #    dados=prod.query.filter_by(id_emp=id).all()
    #else: 
    #    dados = prod.query.filter_by(id_emp=empr,id_cat=cate).all() 
    dados = prod.query.all() 
    catt = cat.query.all()  
    cont = pedidos.query.order_by(pedidos.sub_total).filter_by(id_venda=senha).count()


               
    return render_template("listpedidos.html",a=dados, b=dados2, senha=senha, catt=catt, cont=cont)       
  
  

@app.route("/detalhes", methods=["POST"])
def detalhes():    

    senha = session['username']
    print("senha"+senha)
    dados2 = emp.query.all()
    id = request.form["id"]
    produto= request.form["produtos"]
    
   
    dados = prod.query.filter_by(ID=id).all()
    catt = cat.query.all()  
  
    cont = pedidos.query.order_by(pedidos.sub_total).filter_by(id_venda=senha).count()

          
    return render_template("detalhes.html",a=dados, b=dados2, senha=senha, catt=catt, cont=cont) 


 #carrinho
@app.route("/carrinho", methods=["GET", "POST"])
def car():
    
    if request.method == 'GET':
        senha = session['username']
        print(senha)
        
        dados = pedidos.query.filter_by(id_venda=senha).all()
        results = pedidos.query.order_by(pedidos.sub_total).filter_by(id_venda=senha).all()
        total = sum([pedidos.sub_total for pedidos in results])
        cont = pedidos.query.order_by(pedidos.sub_total).filter_by(id_venda=senha).count()
        print(dados)
      
         ##serialize
        output=[]
        to = {}
        output.append("pedido: "+senha)
        
        for todo in dados:
            
            #to['produtos']=todo.produtos
            #to['valor']=todo.valor
            #to['qtd']=todo.qtd
            #to['sub_total']=todo.sub_total
            #output.append(to)
            
            output.append("produto: "+todo.produtos)
            output.append("valor: "+str(todo.valor))
            output.append("qtd: "+str(todo.qtd))
            output.append("sub total: "+str(todo.sub_total))
            output.append("-----------")
        output.append("TOTAL A PAGAR: R$"+str(total))
        #print(' '.join(map(str, output))) 
        print('\n'.join(map(str, output)))
        out='\n'.join(map(str, output))
        #print(*output, sep = "\n") 
        
        
        dados2 = emp.query.all()
    
        return render_template("carrinho.html", a=dados, val=total, senha=senha, output=out,  b=dados2, cont=cont)    
    

        
#cad pedidos
@app.route("/cadpedidos", methods=["POST"])
def adicionar():
    #dadidos = prod.query.order_by(prod.query.desc()).first()
    senha = session['username']
    x = datetime.datetime.now()

    social = pedidos(id_venda=senha,
                     produtos=request.form["produtos"],
                     valor=request.form["valor"],
                     qtd=request.form["qtd"],
                     sub_total=request.form["subtotal"],
                     data=x
                     ) #desejo form
    db.session.add(social)
    db.session.commit()
    #dados = prod.query.all()
    dados = prod.query.all()
    dados2 = emp.query.all()
    
    catt = prod.query.all() 
    cont = pedidos.query.order_by(pedidos.sub_total).filter_by(id_venda=senha).count()


    return render_template("listpedidos.html", a=dados, b=dados2, catt=catt, cont=cont)
    #return redirect(url_for('index'))


#finalizar pedidos
@app.route("/finalizar", methods=["GET"])
def final():
    #apaga session pedido
    session.pop('username', None)
   
    dados = prod.query.all()
    dados2 = emp.query.all()
    catt = prod.query.all() 

    return render_template("finalizar.html", a=dados, b=dados2, catt=catt)




@app.route("/apagar", methods=["POST"])
def apagar():
    nome = request.form.get("title")
    social = pedidos.query.filter_by(id_venda=nome).first()
    db.session.delete(social)
    db.session.commit()
    
    senha = session['username']
    #dados = pedidos.query.filter_by(id_venda=senha)
    dados = pedidos.query.filter_by(id_venda=senha).all()
    
    ##########################################################
    senha = session['username']
    print(senha)
        
    dados = pedidos.query.filter_by(id_venda=senha).all()
    results = pedidos.query.order_by(pedidos.sub_total).filter_by(id_venda=senha).all()
    total = sum([pedidos.sub_total for pedidos in results])
    print(dados)
      
         ##serialize
    output=[]
    to = {}
    output.append("pedido: "+senha)
        
    for todo in dados:
        output.append("produto: "+todo.produtos)
        output.append("valor: "+str(todo.valor))
        output.append("qtd: "+str(todo.qtd))
        output.append("sub total: "+str(todo.sub_total))
        output.append("-----------")
    output.append("TOTAL A PAGAR: R$"+str(total))
    #print(' '.join(map(str, output))) 
    print('\n'.join(map(str, output)))
    out='\n'.join(map(str, output))
    #print(*output, sep = "\n") 
    
    dados2 = emp.query.all()
    cont = pedidos.query.order_by(pedidos.sub_total).filter_by(id_venda=senha).count()

      
    return render_template("carrinho.html", a=dados, val=total,senha=senha,  output=out,b=dados2, cont=cont)   
   
@app.template_filter()
def currencyFormat(value):
    value = float(value)
    return "R$ {:,.2f}".format(value)


###filtrar
@app.route("/filtrar", methods=["POST"])
def get_filter():    
    select = request.form.get('id_cat')
    print(select)
    
    
    
    if (select=='all'):
        dados=prod.query.all()
    else: 
        dados = prod.query.filter_by(id_cat=select).all() 
        
    dados2 = emp.query.all()
    catt = cat.query.all()         
               
    return render_template("listpedidos.html",a=dados, b=dados2,  catt=catt)      


########cadastrar produtos


app.config["IMAGE_UPLOADS"] = join(dirname(realpath(__file__)), 'static') #/home/gusherokids/mysite/static/images



@app.route("/cad_produto", methods=["GET", "POST"])
def upload_image():
   
    dados2 = emp.query.all()
    catt = cat.query.all() 
    dados = prod.query.all() 
        
    if request.method == "POST":
        
        f = request.files['file']
        filename = secure_filename(f.filename)
        url = filename
        f.save(os.path.join(app.config['IMAGE_UPLOADS'], filename))
        print("Image saved")
        print(url)
        select = request.form.get('id_cat')
        print(select)        
        
        social = prod(id_cat=select,
                      Nome=request.form["produto"],
                      desc=request.form["desc"],
                      valor=request.form["valor"],
                      imagens="/static/"+url) 
        db.session.add(social)
        db.session.commit()
        
    '''
    tam=request.form.getlist("users")
    tam2 = ','.join(tam)
    print ("tam2: "+tam2)
    '''
    dados = prod.query.all()

    return render_template("cad_produto.html", a=dados, b=dados2, catt=catt)


@app.route("/apagarprod", methods=["POST"])
def apagarprod():
    nome = request.form.get("title")
    social = prod.query.filter_by(ID=nome).first()
    db.session.delete(social)
    db.session.commit()
    
    dados = prod.query.all()
    dados2 = emp.query.all()
    catt = cat.query.all() 

    return render_template("cad_produto.html", a=dados, b=dados2, catt=catt)



####categori

@app.route("/cad_categoria", methods=["GET", "POST"])
def cat_categoria():
    
    dados = prod.query.all()
    dados2 = emp.query.all()
    
    
    if request.method == "POST":
               
        social = cat(
                      categoria=request.form["categoria"]
                      ) 
        db.session.add(social)
        db.session.commit()
    
    catt = cat.query.all() 

    return render_template("cad_categoria.html", a=dados, b=dados2, catt=catt)




@app.route("/apagarcat", methods=["POST"])
def apagarcat():
   
    dados = prod.query.all()
    dados2 = emp.query.all()  
    
    if request.method == "POST":
        nome = request.form.get("title")
        social = cat.query.filter_by(id=nome).first()
        db.session.delete(social)
        db.session.commit()
    
    catt = cat.query.all() 
    
    return render_template("cad_categoria.html", a=dados, b=dados2, catt=catt)


##pedidos

@app.route("/cad_pedidos", methods=["GET", "POST"])
def cat_pedid():
    if not session.get('logged_in'):
            dados = prod.query.all()
            dados2 = emp.query.all()
            catt = cat.query.all()
            return render_template("login.html", a=dados, b=dados2, catt=catt)
    else:
        dados = pedidos.query.all()
        
        
        dados2 = emp.query.all()
        catt = cat.query.all() 
        return render_template("cad_pedidos.html", a=dados, b=dados2, catt=catt)



#ferenciar
@app.route("/gerenciar", methods=["GET", "POST"])
def gerenciar():
    if not session.get('logged_in'):
            dados = prod.query.all()
            dados2 = emp.query.all()
            catt = cat.query.all()
            return render_template("login.html", a=dados, b=dados2, catt=catt)
    else:
        dados = prod.query.all()
        dados2 = emp.query.all()
        catt = cat.query.all() 
        return render_template("gerenciar.html", a=dados, b=dados2, catt=catt)
    

##logout

@app.route('/sair', methods=['GET', 'POST'])
def log():
    if request.method == 'GET':
        session['logged_in'] = False
        dados = prod.query.all()
        dados2 = emp.query.all()
        catt = cat.query.all() 
        return render_template("login.html", a=dados, b=dados2, catt=catt)
    
##login

@app.route('/login', methods=['GET', 'POST'])
def login():
    """Login Form"""
    if request.method == 'GET':
        return render_template("login.html")
    else:
        name = request.form['username']
        passw = request.form['password']
        data = emp.query.filter_by(login=name, senha=passw).first()
        data2 = emp.query.filter_by(login=name, senha=passw).all()
        if data is not None:
            session['logged_in'] = True
            dados = prod.query.all()
            dados2 = emp.query.all()
            catt = cat.query.all() 
            return render_template("gerenciar.html", a=dados, b=dados2,catt=catt)
        else:
            
            dados = prod.query.all()
            dados2 = emp.query.all()
            catt = cat.query.all() 
            return render_template("login.html", a=dados, b=dados2, catt=catt)





app.run(debug=True,host='0.0.0.0', port='8080')
app.secret_key = "123"