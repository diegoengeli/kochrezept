# app/routes.py
# code used from microblog [Miguel Grinberg]
from datetime import datetime
from flask import render_template, flash, redirect, url_for, request
from app import app, db
from app.forms import LoginForm, RegistrationForm, EditProfileForm, RecipeForm, EmptyForm, PostForm
from flask_login import current_user, login_user, logout_user, login_required
from app.models import User, Recipe
from werkzeug.urls import url_parse


@app.before_request
def before_request():
    if current_user.is_authenticated:
        current_user.last_seen = datetime.utcnow()
        db.session.commit()


@app.route('/', methods=['GET', 'POST'])
@app.route('/index', methods=['GET', 'POST'])
def index():
    # Retrieve all recipes to display on the index page
    recipes = Recipe.query.all()
    return render_template('index.html', title='Home', recipes=recipes)

# code by marcel based on microblog [Miguel Grinberg]
@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user is None or not user.check_password(form.password.data):
            flash('Invalid email or password')
            return redirect(url_for('login'))
        login_user(user, remember=form.remember_me.data)
        next_page = request.args.get('next')
        if not next_page or url_parse(next_page).netloc != '':
            next_page = url_for('index')
        return redirect(next_page)
    return render_template('login.html', title='Sign In', form=form)


@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))

# code by marcel based on microblog [Miguel Grinberg]
@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(email=form.email.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('Congratulations, you are now a registered user!')
        return redirect(url_for('login'))
    return render_template('register.html', title='Register', form=form)

# code used from microblog [Miguel Grinberg]
@app.route('/edit_profile', methods=['GET', 'POST'])
@login_required
def edit_profile():
    form = EditProfileForm(current_user.email)
    if form.validate_on_submit():
        current_user.username = form.username.data
        current_user.first_name = form.first_name.data
        current_user.last_name = form.last_name.data
        current_user.street = form.street.data
        current_user.city = form.city.data
        current_user.postal_code = form.postal_code.data
        current_user.country = form.country.data
        current_user.email = form.email.data
        if form.password.data:
            current_user.set_password(form.password.data)
        db.session.commit()
        flash('Your profile has been updated.')
        return redirect(url_for('edit_profile'))
    elif request.method == 'GET':
        form.username.data = current_user.username
        form.first_name.data = current_user.first_name
        form.last_name.data = current_user.last_name
        form.street.data = current_user.street
        form.city.data = current_user.city
        form.postal_code.data = current_user.postal_code
        form.country.data = current_user.country
        form.email.data = current_user.email
    return render_template('edit_profile.html', title='Edit Profile', form=form)

# code by marcel based on microblog [Miguel Grinberg]
@app.route('/post_recipe', methods=['GET', 'POST'])
@login_required
def post_recipe():
    form = RecipeForm()
    if form.validate_on_submit():
        recipe = Recipe(title=form.title.data, ingredients=form.ingredients.data, instructions=form.instructions.data, author=current_user)
        recipe = db.session.merge(recipe) # Was neccessary to avoid the error "sqlalchemy.exc.InvalidRequestError: Object '<Recipe at 0x1bfe0204bd0>' is already attached to session '23' (this is '24')""
        if form.image.data:
            recipe.image = form.image.data.read()  # ?? Why does this not work?
        db.session.add(recipe)
        db.session.commit()
        flash('Your recipe has been posted!')
        return redirect(url_for('index'))
    return render_template('post_recipe.html', title='Post Recipe', form=form)