from app import app, db
from flask import render_template, request, redirect, flash, url_for, json, jsonify
from app.models import User, Post, Pokemon
from app.forms import RegisterForm, LoginForm, PostForm, PokemonCatcherForm
from flask_login import current_user, login_user, logout_user, login_required
from random import randint
import requests

@app.route('/')
def index():
   return render_template('home.jinja', title='Home')

@app.route('/register', methods= ["GET", "POST"])
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        username= form.username.data
        email= form.email.data
        password= form.password.data
        u = User(username= username, email = email, password_hash = '')
        user_match = User.query.filter_by(username=username).first()
        email_match = User.query.filter_by(email=email).first()
        if user_match:
        # db.session.add(u)
        # db.session.commit()
            flash(f' Username {username} already exists, try again!')
            return redirect('/register')
        
        elif email_match:
            flash(f' Email {email} already exists, try again!')
            return redirect('/register')
        else:
            u.hash_password(password)
            u.commit()
            flash(f'Request to register {username} successful')
            return redirect('/')

    return render_template('register.jinja', form=form, title = 'Register')


      
@app.route('/login', methods= ['GET', 'Post'])
def login():
    form=LoginForm()
    if form.validate_on_submit():
        username= form.username.data
        password= form.password.data
        user_match= User.query.filter_by(username=username).first()
        if not user_match or not user_match.check_password(password):
            flash(f'Username or Password does not work, try again!')
            return redirect('/login')
        flash(f'{username} successfully logged in!')
        login_user(user_match, remember=form.remember_me.data)
        return redirect('/')
    return render_template("login.jinja", login_form=form, title='Login')

# @app.route('/posts')
# def posts():
#    return render_template('posts.jinja', title='Posts')

# @app.route('/find_pokemon')
# def find_pokemon():
#    pass
#    return render_template('find_pokemon.jinja', title= 'Pokemon Collection' )

@app.route('/logout')
@login_required
def log_out():
    logout_user()
    return redirect('/')

@app.route('/posts')
def post():
    form = PostForm()
    if form.validate_on_submit():
        heading=form.heading.data
        body = form.body.data
        p=Post(heading=heading, body=body, user_id=current_user.id)
        p.commit()
        return redirect(url_for('app.user', username=current_user.username))
        flash(f'Your post went through!')
    return render_template('posts.jinja', postform=form)

@app.route('/user/<username>')
def user(username):
    user_match = User.query.filter_by(username=username).first()
    print(user_match, "================")
    pokemons = Pokemon.query.filter_by(user_id = user_match.id).all()
    print(pokemons, "================")
    if not user_match:
        redirect('/')
    posts = user_match.posts
    return render_template('user.jinja', user=user_match, posts=posts, pokemons=pokemons)


@app.route('/findpokemon', methods=["GET", "POST"])
def find_pokemon():
    form= PokemonCatcherForm()
    if request.method == "POST":
        if form.validate():
            pokemon_name = form.pokemon_name.data
            def pokemon_info(p_name):
                response = requests.get(f'https://pokeapi.co/api/v2/pokemon/{p_name}')
                if response.ok:
                    my_pokemon = {}
                    my_pokemon = {'pokemon_name': response.json()['forms'][0]['name'],
                                  'ability': response.json()['abilities'][0]['ability']['name'],
                                  'type': response.json()['types'][0]['type']['name'],
                                  'sprite': response.json()['sprites']['front_default'],
                                  'apiid': response.json()['id'],
                                # 'other_sprite': response.json()['sprites']['other']['official-artwork']['front_default'],
                                'questionmark': url_for('static', filename = 'questionmark.jpg')
                    }
                    return my_pokemon
        
            if pokemon_name.lower() == 'random':
                a = randint(1, 1008)
                b = randint(10001, 10271)
                c = randint(1, 1279)
                if c < 1009:
                    pokemon_index = a
                elif c > 1008:
                    pokemon_index = b
                the_pokemon = pokemon_info(pokemon_index)
            else:
                the_pokemon = pokemon_info(pokemon_name.lower())
            if current_user.is_authenticated:

                form.pokemon_name.data = ''

                if the_pokemon:
                    pokemon_name = the_pokemon['pokemon_name'].capitalize()
                    ability = the_pokemon['ability']
                    type = the_pokemon['type']
                    if the_pokemon['sprite']:
                        sprite = the_pokemon['sprite']
                    elif the_pokemon['sprite']:
                        sprite= url_for('static', filename = 'questionmark.jpg')
                    user_id = current_user.id

                    dblist = Pokemon.query.filter_by(pokemon_name = pokemon_name).all()
                    if dblist == []:
                        if len(Pokemon.query.filter_by(user_id = current_user.id).all()) < 10:
                            pokemon = Pokemon(pokemon_name, ability, type, sprite, the_pokemon['apiid'], user_id )
                            pokemon.commit()
                            flash("You got the pocket monster!")
                        else:
                            flash("You are at full max!")
                            return redirect(url_for('find_pokemon'))
                    else:
                        flash("That Pokemon already has a trainer!")
                        return redirect(url_for("find_pokemon"))
                return render_template('find_pokemon.jinja', form= form, the_pokemon =the_pokemon)
            
    elif request.method == "GET":
        return render_template('find_pokemon.jinja', form=form)
        


# @app.route('/catch/<name>')
# @login_required
# def catchpoke(name):
#     pokemon = Pokemon.query.filter_by(pokemon_name=name)
#     return render_template('cards.jinja')







# @app.route('/mypokemon')
# def mypokemon():
#     pokemons = Pokemon.query.filter_by(user_id = current_user.id)
#     return render_template('mypokemon.', pokemons = pokemons)


@app.route('/deletepokemon')
def delpokemon(pokemon_id):
    pokemon = Pokemon.query.get(pokemon_id)
    if current_user.id != pokemon.user_id:
        flash("That Pokemon doesn't belong to you.")
        return redirect (url_for('/'))
    pokemon.delete_pokemon()
    flash("Pokemon deleted.")
    return redirect(url_for('/'))


        
                




