from app import app,db,bcrypt,login_manager

from flask import render_template ,flash,redirect,url_for,session

from app.forms import LoginForm,UserForm,CategorieForm,ParfumForm

from app.models import Utilisateur,Categorie,Parfum,Commande

from flask_login import login_user, login_required,logout_user,current_user

from app.parfums import get_parfums_femme,get_parfums_homme,get_parfums_mixte,random_products,get_all,acceuil,acceuilsuite

from flask import Flask, request, jsonify

import sqlite3

articles =[]
cart=[] 


@login_manager.user_loader

def load_user(user_id):
    return Utilisateur.query.get(user_id)


@app.route('/signIn',methods=['POST','GET'])
def loginParfums():
    login_form = LoginForm()
    if login_form.validate_on_submit():
        email = login_form.email.data
        password = login_form.password.data

        user = Utilisateur.query.filter_by(email =email).first()
        print(user)

        if not user:
            flash("Ce mail n'a pas été enregistrer ")
            print("ERROR MAIL NOT EXIST")
            return redirect(url_for('loginParfums'))
        pswd_unshashed = bcrypt.check_password_hash(user.mot_de_passe,password)

        if not pswd_unshashed:
            flash("Mot de passe saisi incorrect")
            print("password incorrect")
            return redirect(url_for('loginParfums'))

        login_user(user)

        flash("Vous etes connecté")

        return redirect(url_for('Acceuil'))

    return render_template('signIn.html',form = login_form)

@app.route('/logout')
@login_required
def logout():

    global cart

    cart =[]
    
    logout_user()
    return redirect(url_for('Acceuil'))


@app.route('/signUp',methods=["POST","GET"])
def signUp():
    signUp_form = UserForm()
    if signUp_form.validate_on_submit():
        nom = signUp_form.nom.data
        prenom = signUp_form.prenom.data
        email = signUp_form.email.data
        
        password = signUp_form.password.data
        psw_hash = bcrypt.generate_password_hash(password).decode("utf8")
        user = Utilisateur(nom=nom,prenom=prenom,email=email,mot_de_passe=psw_hash)

        
        

        db.session.add(user)
        db.session.commit()
        return redirect(url_for('loginParfums'))

    return render_template('signUp.html',form = signUp_form)
""" @app.route('/categorie',methods=["POST","GET"])
def categorie():
    categorie_form = CategorieForm()
    if categorie_form.validate_on_submit():
        nom = categorie_form.nom.data
        description = categorie_form.description.data

        categ = Categorie(nom = nom ,description = description)
        db.session.add(categ)
        db.session.commit()

    return render_template("Categories.html",form = categorie_form) """

@app.route('/',methods=["POST","GET"])
def Acceuil():
    global cart

    """ nom = current_user.nom """

    parf = acceuil()

    accparf = acceuilsuite()

    populaire = random_products()
    
    nombre = len(cart)
    return render_template('Acceuil.html',nombre = nombre,parfums=populaire,par = parf ,parf = accparf)

@app.route('/Homme')
def ParfumsHomme():
    


    parfums = get_parfums_homme()
    print(parfums)
    print(f"Number of parfums: {len(parfums)}")
    nombre = len(cart)
    
    return render_template('Homme.html', parfums=parfums,nombre=nombre)

@app.route('/Femme')
def ParfumsFemme ():
   
    nombre = len(cart)
    ParfumsFemme= get_parfums_femme()
    return render_template('Femme.html',parfums= ParfumsFemme,nombre=nombre)

@app.route('/Mixte')
def ParfumsMixte():
   
    nombre = len(cart)
    parfumsMixte= get_parfums_mixte()
    return render_template('Mixte.html',parfums =parfumsMixte,nombre=nombre)


@app.route('/parfum/<int:parfum_id>')
def parfum(parfum_id):
 
    if not current_user.is_authenticated:
        return redirect(url_for('loginParfums'))
    parfum = Parfum.query.get_or_404(parfum_id)
    categorie = Categorie.query.get_or_404(parfum.categorie_id)
    produits_similaires = Parfum.query.filter_by(categorie_id=parfum.categorie_id).filter(Parfum.id != parfum_id).all()  
    nombre = len(cart) 
    return render_template('Details.html', parfum=parfum, categorie=categorie,produits_similaires=produits_similaires,nombre = nombre)

id = 0
@app.route('/ajouter-au-panier', methods=['POST'])
def ajouter_au_panier():
   
    data = request.get_json()
    id_parfum = data['id']
    quantité_parfum= data['nombre_elements']

    parfum = Parfum.query.get_or_404(id_parfum)

    for item in cart:
        if item['nom'] == parfum.nom:
            # Si le parfum est déjà dans le panier, augmente la quantité
            item['quantite'] += quantité_parfum
            item['prixtotal'] = item['prix'] * item['quantite']
            return redirect(url_for('panier'))
  


    global id
    cart.append({
        'id':id,
        'nom': parfum.nom,
        'image': parfum.image,
        'description': parfum.description,
        'quantite': quantité_parfum,
        'prix': parfum.prix,
        'prixtotal': parfum.prix*quantité_parfum
    })
    id += 1
  
    return redirect(url_for('panier'))
    
montant_a_retirer= 0

@app.route('/supprimer',methods =['POST'])
def supprimer():
    
    data = request.get_json()
    print("nom",data)
    id_cart = int(data['id'])  # Convert id_cart to an integer
    item = cart[id_cart]
    
    cart.pop(id_cart)
    

    
   
  
    return jsonify(cart)

prixtotal=0
@app.route('/panier')
def panier():
    global prixtotal
   
    total = 0
    nombre = len(cart)
    for i in cart:
        total +=i['prixtotal']
    prixtotal=total
    return render_template('panier.html',parfums = cart , totaly = total ,nombre = nombre )



@app.route('/ContactUs')
def contactUs():
    
    nombre = len(cart)
    return render_template('ContactUs.html',nombre = nombre)

@app.route('/About')
def about():
  
    nombre = len(cart)
    return render_template('About.html',nombre = nombre)

@app.route('/payement')
def payement():
    global cart
    nom = current_user.nom
    nombre = len(cart)
    global prixtotal
    
    
    if prixtotal == 0:
        prix=0
    else:
        prix = prixtotal+300
    return render_template('payement.html',parfums = cart, nombre = nombre ,prixtotal = prix,prixu = prixtotal,nom= nom)
@app.route('/deleteparfum/<int:id>', methods=['POST'])
def deleteparfum(id):
    parfum = Parfum.query.get_or_404(id)
    db.session.delete(parfum)
    db.session.commit()
    return redirect(url_for('index'))

@app.route('/deleteuser/<int:id>',methods=['POST'])
def deleteUser(id):
    user = Utilisateur.query.get_or_404(id)
    db.session.delete(user)
    db.session.commit()
    return redirect(url_for('admin'))


@app.route('/admin',methods=["POST","GET"])
def admin():
    categorie_form = CategorieForm()
    if categorie_form.validate_on_submit():
        nom = categorie_form.nom.data
        description = categorie_form.description.data
        categ = Categorie(nom = nom ,description = description)
        db.session.add(categ)
        db.session.commit()

    Categories = Categorie.query.all()
    parfums = get_all()
    ListeUser = Utilisateur.query.all()

    add = ParfumForm()
    add.categorie_id.choices = [(c.id, c.nom) for c in Categories]
    if add.validate_on_submit():
       nom = add.nom.data 
       description = add.description.data
       prix = add.prix.data
       image = add.image.data
       categorie_id = add.categorie_id.data
       parfumse = Parfum(nom= nom,description= description,prix = prix,image = image,categorie_id = categorie_id)
       db.session.add(parfumse)
       db.session.commit()

    return render_template('Admin.html',form = categorie_form,forms = add,parfums = parfums,categorie=Categories,User = ListeUser)


""" @app.route('/panier')
def panier():
    parfums = get_parfums_homme()
  
    for parfum in parfums:
        cart.append({
            'nom': parfum.nom,
            'image': parfum.image,
            'description': parfum.description,
            'prix': parfum.prix,
        })
    print(cart)
    return render_template('panier.html', parfums=cart) """
'''@app.route("/index",methods =['POST','GET'])
def index():

    article = [
        {   
            'date':"28 decembre 2020",
            'title':"Caffe latee",
            'description':" Lorem ipsum dolor sit amet, consectetur adipisicing elit sed do eiusmod \
                tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim\
                veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea\
                commodo consequat."
        },
        {
            'date':"28 decembre 2020",
            'title':"Caffe latee",
            'description':" Lorem ipsum dolor sit amet, consectetur adipisicing elit sed do eiusmod \
                tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim\
                veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea\
                commodo consequat."
        },{
            'date':"28 decembre 2020",
            'title':"Caffe latee",
            'description':" Lorem ipsum dolor sit amet, consectetur adipisicing elit sed do eiusmod 
                tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim
                veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea
                commodo consequat."
        }
       
    ]
 

    return render_template('index.html',articles=article)'''
'''@app.route('/categories',methods=['POST','GET'])
def categories ():

    categories = Categories()
    if categories.validate_on_submit():
        name_categories = categories.categorie_name.data

    return render_template('categories.html',form = categories, ajout = categories.categorie_name.data )'''
'''
@app.route('/article',methods=['POST','GET'])
def article():
    
    article_form = Ajout_article()
    comment_form = commentaires()
    if article_form.validate_on_submit():
        nom = article_form.nom_article.data
        description = article_form.description_article.data
        date = article_form.Date.data

        articles.append({
            'date': date,
            'title': nom,
            'description': description,
            'comments': []  # Ajoutez une liste de commentaires à chaque article
        })
    if comment_form.validate_on_submit():
        comment = comment_form.comment.data
        # Ajoutez le commentaire à l'article approprié
        # Vous devrez identifier l'article d'une manière ou d'une autre
        # Par exemple, vous pouvez utiliser l'index de l'article dans la liste
        """ articles[article_index]['comments'].append(comment) """
    return render_template('index.html',form = article_form, comment_form=comment_form)'''
