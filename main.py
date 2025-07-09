import os
import git
from flask import Flask, render_template, url_for, flash, redirect, request
from forms import RegistrationForm
from flask_debugtoolbar import DebugToolbarExtension
from flask_behind_proxy import FlaskBehindProxy
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)                    
proxied = FlaskBehindProxy(app)

#get rid of redirect pause
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False

app.config['SECRET_KEY'] = '342983a04237f3a7d7d98db26c404908'

app.debug = True
toolbar = DebugToolbarExtension(app)

#Set up table
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///new_friends.db'
db = SQLAlchemy(app)

class User(db.Model):
  id = db.Column(db.Integer, primary_key=True)
  username = db.Column(db.String(20), unique=True, nullable=False)
  email = db.Column(db.String(120), unique=True, nullable=False)

  def __repr__(self):
    return f"User('{self.username}', '{self.email}')"

with app.app_context():
  db.create_all()

@app.route("/")                         
def hello_world():
    #build path to album folder
    album_dir = os.path.join(app.static_folder, 'images', 'album')
    #get list of files
    images = [f for f in os.listdir(album_dir)]
    #pass into html
    return render_template('home.html', subtitle='Home Page', images=images, full_name='Obademilade Mary-anne Fashemo')        

#making a second page
@app.route("/about")
def second_page():
    about_me_dir = os.path.join(app.static_folder, 'images', 'about-me')
    about_images = [f for f in os.listdir(about_me_dir) if f.lower().endswith('.png')]
    return render_template('about_me.html', subtitle='About', text='A Few Facts About Me!', about_images=about_images)

#third webpage
@app.route("/favorites")
def favorites():
    favorites_dir = os.path.join(app.static_folder, 'images', 'sisters')
    favorites = [f for f in os.listdir(favorites_dir) if f.lower().endswith('.jpg')]
    return render_template('favorites.html', subtitle='My Favorite Things!', images=favorites, fav_sis="Lola <3")

#register success page
@app.route('/success')
def register_success():
    return render_template('register_success.html')

#register page
@app.route("/register", methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit(): 
        user = User(username=form.username.data, email=form.email.data)
        db.session.add(user)
        db.session.commit()
        flash(f'Account created for {form.username.data}!', 'success')
        return redirect(url_for('register_success')) 
    return render_template('register.html', title='Register', form=form)

#webhook for auto deployment
@app.route("/update_server", methods=['POST'])
def webhook():
    if request.method == 'POST':
        repo = git.Repo('/home/demi0aam0webpage/AllAboutMeWebpage/new_friends')
        origin = repo.remotes.origin
        origin.pull()
        return 'Updated PythonAnywhere successfully', 200
    else:
        return 'Wrong event type', 400
  
if __name__ == '__main__':               
    app.run(debug=True, host="0.0.0.0")

