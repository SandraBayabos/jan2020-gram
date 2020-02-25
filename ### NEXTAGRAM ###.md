### NEXTAGRAM

1. Forking the repository
2. Git clone it and enter into the folder
3. Create your environment with python=3.7 and activate your environment
4. pip install -r requirements.txt
5. Create a database for your nextagram_dev
6. Create a .env file and save your FLASK_APP, FLASK_ENV, DATABASE, SECRET_KEY for your flash messages

### FOLDER STRUCTURE

1. We will mostly be working under instagram_web
2. You'll see a folder called models and inside, you'll see a file called user.py. From now on you'll be separating out your models into their respective files.
3. Then go to instagram_web, which is where we will be spending the majority of our time working on
4. You'll see a bunch of folders including blueprints, static, templates and util.
5. The templates folder has the more generic, global type templates at the moment, like the homepage and error pages, so you won't really be working here
6. Take a look at the blueprints folder and you'll see how folders and files are actually structured.
7. Blueprints => folder relating to each model (e.g. users, sessions, images (note that they are plural)) => views.py (this is where you will be writing all your routes and functions) & templates folder => another models folder called users => all your html files

### REGISTERING BLUEPRINTS

1. Before a route can be used, you need to register the blueprints accordingly.
2. First we need to register them as actual blueprints in each of the views.py files like this. This creates an instance of a Blueprint class and it gets saved to the users_blueprint variable:-

from flask import Blueprint

users_blueprint = Blueprint('users',
**name**,
template_folder='templates/users')

and then in the init.py file in the root of the util folder, we assign it a url_prefix:-

from instagram_web.blueprints.users.views import users_blueprint

app.register_blueprint(users_blueprint, url_prefix="/users")

3. You'll need to import and then register all of your blueprints here, by assigning a url_prefix to each one
4. This is also how you'll be able to maintain your restful routes for each one of your models.
5. So you'll have something like /users/; /users/new; users/show; users/<id>/edit etc. etc.
