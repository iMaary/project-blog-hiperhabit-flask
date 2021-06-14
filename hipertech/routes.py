from hipertech import db, app
from flask import render_template, flash, request
from werkzeug.security import generate_password_hash, check_password_hash
from hipertech.forms import UserForm, PasswordForm, PostForm
from hipertech.models import Users, Posts

# Show Posts Page


@app.route('/posts')
def posts():
    # Grab all the Posts from the database
    posts = Posts.query.order_by(Posts.date_posted)
    # Redirect to Webpage
    return render_template("posts.html", posts=posts)


# Add Post Page
@app.route('/add-post', methods=['GET', 'POST'])
def add_post():
    form = PostForm()

    if form.validate_on_submit():
        post = Posts(title=form.title.data, content=form.content.data,
                     author=form.author.data, slug=form.slug.data)
        # Clear The Form
        form.title.data = ''
        form.content.data = ''
        form.author.data = ''
        form.slug.data = ''

        # Add post data to database
        db.session.add(post)
        db.session.commit()

        # Return a Message
        flash('Postado com Sucesso!')

    # Redirect to Webpage
    return render_template("add_post.html", form=form)


# JASON Thing
@app.route('/date')
def get_current_date():
    favorite_pizza = {
        "Mary": "4 Queijos",
        "Carla": "Calabresa"
    }
    return favorite_pizza
    # return {"Date": date.today()}


@app.route('/delete/<int:id>')
def delete(id):
    user_to_delete = Users.query.get_or_404(id)
    name = None
    form = UserForm()

    try:
        db.session.delete(user_to_delete)
        db.session.commit()
        flash("Usuário deletado com sucesso!")

        our_users = Users.query.order_by(Users.date_added)
        return render_template("add_user.html", name=name,
                               form=form,
                               our_users=our_users)
    except:
        flash("Opa, aconteceu algo de errado ao tentar deletar esse usuário... tente novamente!")
        return render_template("add_user.html",
                               name=name, form=form, our_users=our_users)


# Update Database Record
@app.route('/update/<int:id>', methods=['GET', 'POST'])
def update(id):
    form = UserForm()
    name_to_update = Users.query.get_or_404(id)
    if request.method == "POST":
        name_to_update.name = request.form['name']
        name_to_update.email = request.form['email']
        name_to_update.favorite_color = request.form['favorite_color']
        try:
            db.session.commit()
            flash("Usuário Atualizado com Sucesso")
            return render_template("update.html",
                                   form=form,
                                   name_to_update=name_to_update,
                                   id=id)
        except:
            flash("ERRO! Parece que ocorreu algum problema... tente novamente")
            return render_template("update.html",
                                   form=form,
                                   name_to_update=name_to_update,
                                   id=id)
    else:
        return render_template("update.html",
                               form=form,
                               name_to_update=name_to_update,
                               id=id)


# Create a route decorate (it's how ...url.../home.html)
@app.route('/')  # it works when there ins't route name
def index():
    first_name = "Maria"
    stuff = "Essa é minha <strong>Lista</strong>"
    flash("Seja Bem Vindo(a)!")
    favorites_pizza = ["Caminhar", "Diminuir Sal", "Dormir 8h+", "Beber água"]
    return render_template("index.html",
                           first_name=first_name,
                           stuff=stuff,
                           favorites_pizza=favorites_pizza)

# Local create user register


@app.route('/user/add', methods=['GET', 'POST'])
def add_user():
    name = None
    form = UserForm()
    # Validate Form if it was Submited
    if form.validate_on_submit():
        user = Users.query.filter_by(email=form.email.data).first()
        if user is None:
            # Hash the password!
            hashed_pw = generate_password_hash(
                form.password_hash.data, "sha256")
            user = Users(name=form.name.data, email=form.email.data,
                         favorite_color=form.favorite_color.data, password_hash=hashed_pw)
            db.session.add(user)
            db.session.commit()
        name = form.name.data
        form.name.data = ''
        form.email.data = ''
        form.favorite_color.data = ''
        form.password_hash.data = ''
        flash("Usuário Adicionado Com Sucesso!")
    our_users = Users.query.order_by(Users.date_added)
    return render_template("add_user.html", name=name,
                           form=form,
                           our_users=our_users)

# Create Password Test Page


@app.route('/test_pw', methods=['GET', 'POST'])
def test_pw():
    email = None
    password = None
    pw_to_check = None
    passed = None
    form = PasswordForm()

    # Validate Form if it was Submited
    if form.validate_on_submit():
        email = form.email.data
        password = form.password_hash.data

        # Clear Form
        form.email.data = ''
        form.password_hash.data = ''

        # Look Up User By Email Adress
        pw_to_check = Users.query.filter_by(email=email).first()

        # Check Hash Password
        passed = check_password_hash(pw_to_check.password_hash, password)

    return render_template("test_pw.html", email=email,
                           password=password,
                           pw_to_check=pw_to_check,
                           passed=passed,
                           form=form)

# Create Custom Error Page

# invalid url


@app.errorhandler(404)
def page_not_fount(e):
    return render_template("404.html")

# internal server error


@app.errorhandler(500)
def page_not_workig(e):
    return render_template("500.html")
