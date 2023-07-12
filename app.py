from flask import Flask, render_template, request, flash, redirect, session, g
from flask_debugtoolbar import DebugToolbarExtension
from sqlalchemy.exc import IntegrityError
from models import db, connect_db, User, Favorite
from forms import UserAddForm, LoginForm, UserEditForm
import requests
import os


CURR_USER_KEY = "curr_user"

app = Flask(__name__)
app.secret_key = 'capstone_project'  # Used to encrypt session data

# Get DB_URI from environ variable (useful for production/testing) or,
# if not set there, use development local db.
app.config['SQLALCHEMY_DATABASE_URI'] = (
    os.environ.get('DATABASE_URL', 'postgresql:///mealdb'))

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = False
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = True
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', "capstone_project")
toolbar = DebugToolbarExtension(app)

connect_db(app)
app.app_context().push()
db.create_all()

##############################################################################
# User signup/login/logout

@app.before_request
def add_user_to_g():
    """If we're logged in, add curr user to Flask global."""

    if CURR_USER_KEY in session:
        g.user = User.query.get(session[CURR_USER_KEY])

    else:
        g.user = None


def do_login(user):
    """Log in user."""

    session[CURR_USER_KEY] = user.id


def do_logout():
    """Logout user."""

    if CURR_USER_KEY in session:
        del session[CURR_USER_KEY]

if __name__ == '__main__':
    app.run(debug=True)



# Home page

@app.route('/')
def homepage():
    """Show homepage:

    - anon users: no nav bar button to collections of favorited recipes
    - logged in: show nav bar button to collections of favorited recipes
    """

    if g.user:
        return render_template('home.html')

    else:
        return render_template('home-anon.html')



# Recipe search by different filters:

@app.route('/search/by_name')
def search_by_name_form ():
    """show search by name page"""

    return render_template('searches/search_by_name.html')


@app.route('/search/by_area')
def search_by_area_form ():
    """show search by area page"""

    return render_template('searches/search_by_area.html')


@app.route('/search/by_main_ingredient')
def search_by_main_ingredient_form():
    """show search by main ingredient page"""
    
    return render_template('searches/search_by_main_ingredient.html')



# Search results/recipe recommendations by different filters:

@app.route('/recipes/by_name')
def search_by_name():
    """ Retrieve meal name input from the form """
    meal_name = request.args.get('meal_name')
    
    return redirect(f"/recipes/{meal_name}")


@app.route('/recipes/by_area')
def search_by_area():
    """ Retrieve meal area input from the form """
    area = request.args.get('area')
    res = requests.get(f"http://www.themealdb.com/api/json/v1/1/filter.php?a={area}")
    data = res.json()
    meals = data["meals"]

    if meals:

        recipes = []

        # Iterate over each meal from the search result

        for meal in meals:
            recipe = {}
            meal_name = meal["strMeal"]
            img = meal["strMealThumb"].replace("\/", "/")
            recipe["name"] = meal_name
            recipe["img"] = img
            recipes.append(recipe)
        
        return render_template('recipes/recipes.html', recipes=recipes)
    
    else:
        flash("Please provide a valid area input.", "danger")

        return redirect('/search/by_area')


@app.route('/recipes/by_main_ingredient')
def search_by_main_ingredient():
    """ Retrieve main ingredient input from the form """
    main_ingredient = request.args.get('main_ingredient')
    res = requests.get(f"http://www.themealdb.com/api/json/v1/1/filter.php?i={main_ingredient}")
    data = res.json()
    meals = data["meals"]

    if meals:
        
        recipes = []

        # Iterate over each meal from the search result

        for meal in meals:
            recipe = {}
            meal_name = meal["strMeal"]
            img = meal["strMealThumb"].replace("\/", "/")
            recipe["name"] = meal_name
            recipe["img"] = img
            recipes.append(recipe)
    
        return render_template('recipes/recipes.html', recipes=recipes)
    
    else:
        flash("Please provide a valid ingredient input.", "danger")

        return redirect('/search/by_main_ingredient')


# Iterate over each recommended recipe and show specific ingredients and instructions:

@app.route('/recipes/<meal_name>')
def recipe(meal_name):
        res = requests.get(f"https://www.themealdb.com/api/json/v1/1/search.php?s={meal_name}")
        data = res.json()
        meals = data["meals"]
        
        if meals:
            meal = data["meals"][0]
            meal_id = int(meal["idMeal"])
            meal_area = meal["strArea"]
            img = meal["strMealThumb"].replace("\/", "/")
            video = meal["strYoutube"].replace("\/", "/")

            lines = meal["strInstructions"].replace(".", ". \n")
            instructions = []
            for line in lines.splitlines():
                instructions.append(line)

            i = 1
            ingredients = []

            while i < 21:
                ingredient = {}
                ingre = meal[f"strIngredient{i}"]
                measure = meal[f"strMeasure{i}"]
                ingredient["ingredient"] = ingre
                ingredient["measure"] = measure
                ingredients.append(ingredient)
                i += 1

            if g.user:
                user= User.query.get_or_404(g.user.id)
                favorites = user.favorites

                favorite_ids = []

                if favorites:                
                    for favorite in favorites:
                        favorite_id = favorite.meal_id
                        favorite_ids.append(favorite_id)

                    return render_template('recipes/recipe.html', meal_name=meal_name, meal_id=meal_id, favorite_ids=favorite_ids, instructions=instructions, img=img, video=video, ingredients=ingredients)   

                else:

                    return render_template('recipes/recipe.html', meal_name=meal_name, meal_id=meal_id, instructions=instructions, img=img, video=video, ingredients=ingredients)

            else:

                return render_template('recipes/recipe.html', meal_name=meal_name, meal_id=meal_id, instructions=instructions, img=img, video=video, ingredients=ingredients)
        
        else:
            flash("Please provide a valid dish name input.", "danger")

            return redirect('/search/by_name')



# User registration

@app.route('/signup', methods=['GET', 'POST'])
def register():
    """Handle user signup.

    Create new user and add to DB. Redirect to home page.

    If form not valid, present form.

    If the there already is a user with that username: flash message
    and re-present form.
    """

    form = UserAddForm()

    if form.validate_on_submit():
        try:
            user = User.signup(
                username=form.username.data,
                password=form.password.data,
                email=form.email.data,
                image_url=form.image_url.data or User.image_url.default.arg,
                header_image_url=form.header_image_url.data or User.header_image_url.default.arg,
                bio=form.bio.data,
                location=form.location.data
            )
            db.session.commit()

        except IntegrityError:
            flash("Username already taken", 'danger')
            return render_template('users/signup.html', form=form)

        do_login(user)

        return redirect("/")

    else:
        return render_template('users/signup.html', form=form)


    if request.method == 'POST':
        # Retrieve user registration data from the form
        username = request.form.get('username')
        password = request.form.get('password')
       
        return render_template('login.html')
    
    return render_template('users/signup.html')


@app.route('/login', methods=["GET", "POST"])
def login():
    """Handle user login."""

    form = LoginForm()

    if form.validate_on_submit():
        user = User.authenticate(form.username.data,
                                 form.hashed_password.data)

        if user:
            do_login(user)
            flash(f"Hello, {user.username}!", "success")
            return redirect("/")

        flash("Invalid credentials.", 'danger')

    return render_template('users/login.html', form=form)


@app.route('/logout')
def logout():
    """Handle logout of user."""
    
    do_logout()
    flash(f'You have successfully logged out.','success')

    return redirect('/login')


@app.route('/users/<int:user_id>')
def show_detail(user_id):
    """Show details of a user and edit/delete file buttons."""
    
    user = User.query.get_or_404(user_id)

    return render_template('users/details.html', user=user)


@app.route('/users/profile', methods=["GET", "POST"])
def profile():
    """Update profile for current user."""

    if not g.user:
        flash("Access unauthorized.", "danger")
        return redirect("/")
        
    user = g.user
    form = UserEditForm(obj=g.user)

    if form.validate_on_submit():
        if User.authenticate(user.username, form.password.data):
            user.username = form.username.data
            user.email = form.email.data
            user.image_url = form.image_url.data or "/static/images/default-pic.png"
            user.header_image_url = form.header_image_url.data or "/static/images/warbler-hero.jpg"
            user.bio = form.bio.data

            db.session.commit()
            return redirect(f"/users/{user.id}")
        
        flash('Wrong password. Please try again.', 'danger')
    
    return render_template('users/edit.html', form=form, user_id=user.id)


@app.route('/users/delete', methods=["POST"])
def delete_user():
    """Delete user."""

    if not g.user:
        flash("Access unauthorized.", "danger")
        return redirect("/")

    do_logout()

    db.session.delete(g.user)
    db.session.commit()

    return redirect("/signup")   



# Display/Add/Delete favorites:

@app.route('/users/<int:user_id>/favorites')
def show_favorites(user_id):
    """Show user's favorited recipes."""
    
    user = User.query.get_or_404(user_id)
    favorites = user.favorites

    recipes = []

    if favorites:                
        for favorite in favorites:

            recipe = {}

            meal_id = favorite.meal_id
            res = requests.get(f"https://www.themealdb.com/api/json/v1/1/lookup.php?i={meal_id}")
            data = res.json()
            meal = data["meals"][0]

            meal_name = meal["strMeal"]
            img = meal["strMealThumb"].replace("\/", "/")
            recipe["name"] = meal_name
            recipe["img"] = img
            recipes.append(recipe)

        return render_template('users/favorites.html', user=user, recipes=recipes, meal_id=meal_id)

    else:
        flash("Please add recipe to your favorites first.", "danger")

        return redirect(f"/users/{g.user.id}")


@app.route('/users/<int:user_id>/<int:meal_id>/favorite', methods=['POST'])
def add_favorite(meal_id, user_id):
    """Add a favorite for logged-in user."""

    if not g.user:
        flash("Access unauthorized.", "danger")
        return redirect("/")

    user = User.query.get(user_id)
    favorites = user.favorites

    favorite_ids = []

    for favorite in favorites:
        favorite_id = favorite.meal_id
        favorite_ids.append(favorite_id)

    if meal_id not in favorite_ids:
        
        favorite = Favorite(
                meal_id=meal_id,
                )

        db.session.add(favorite)

        user.favorites.append(favorite)

        db.session.commit()

    else:
        flash("You have already favorited this recipe.", "danger")

    return redirect(f"/users/{g.user.id}/favorites")


@app.route('/users/<int:user_id>/<int:meal_id>/unfavorite', methods=['POST'])
def unfavorite(user_id, meal_id):
    """Have logged-in user unfavorite this recipe."""

    if not g.user:
        flash("Access unauthorized.", "danger")
        return redirect("/")

    favorite = Favorite.query.filter(Favorite.user_id == user_id, Favorite.meal_id == meal_id).first()
 
    user = User.query.get(g.user.id)

    db.session.delete(favorite)

    db.session.commit()

    return redirect(f"/users/{g.user.id}/favorites")


