import os
from flask import Flask, render_template, session, redirect, url_for # tools that will make it easier to build on things
from flask_sqlalchemy import SQLAlchemy # handles database stuff for us - need to pip install flask_sqlalchemy in your virtual env, environment, etc to use this and run this

# Application configurations
app = Flask(__name__)
app.debug = True
app.use_reloader = True
app.config['SECRET_KEY'] = 'hard to guess string for app security adgsdfsadfdflsdfsj'

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///./movie_db.db'
app.config['SQLALCHEMY_COMMIT_ON_TEARDOWN'] = True
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False


# Set up Flask debug stuff
db = SQLAlchemy(app) # For database use
session = db.session # to make queries easy





#########
######### Everything above this line is important/useful setup, not problem-solving.
#########


##### Set up Models #####

# Set up association Table between artists and albums
collections = db.Table('collections',db.Column('director_id',db.Integer, db.ForeignKey('Directors.id')),db.Column('distributor_id',db.Integer, db.ForeignKey('Distributors.id')))

class Distributor(db.Model):
    __tablename__ = "Distributors"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64))
    directors = db.relationship('Director',secondary=collections,backref=db.backref('Distributors',lazy='dynamic'),lazy='dynamic')
    movies = db.relationship('Movie',backref='Distributor')


class Director(db.Model):
    __tablename__ = "Directors"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64))
    movies = db.relationship('Movie',backref='Director')

    def __repr__(self):
        return "{} (ID: {})".format(self.lastname, self.firstname, self.id)


class Movie(db.Model):
    __tablename__ = "Movies"
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(64),unique=True) # Only unique title songs can exist in this data model
    director_id = db.Column(db.Integer, db.ForeignKey("Directors.id")) # ok to be null for now
    distributor_id = db.Column(db.Integer, db.ForeignKey("Distributors.id")) #ok to be null for now
    major_genre = db.Column(db.String(64))
    us_gross = db.Column(db.Integer)
    worldwide_gross = db.Column(db.Integer)
    us_dvd_sales = db.Column(db.Integer)
    production_budget = db.Column(db.Integer)
    # ok to be null
    # keeping genre as atomic element here even though in a more complex database it could be its own table and be referenced here

    def __repr__(self):
        return "{} by {} | {}".format(self.title,self.director_id, self.distributor_id, self.major_genre)


##### Helper functions #####

### For database additions
### Relying on global session variable above existing

def get_or_create_director(director_name):
    director = Director.query.filter_by(name=director_name).first()
    if director:
        return director
    else:
        director = Director(name=director_name)
        session.add(director)
        session.commit()
        return director

def get_or_create_distributor(distributor_name):
    distributor = Distributor.query.filter_by(name=distributor_name).first()
    if distributor:
        return distributor
    else:
        distributor = Distributor(name=distributor_name)
        session.add(distributor)
        session.commit()
        return distributor


##### Set up Controllers (route functions) #####

## Main route
@app.route('/movie/new/<title>/<director>/<distributor>/<major_genre>/<us_gross>/<worldwide_gross>/<us_dvd_sales>/<production_budget>/')
def new__movie(title, director, distributor, major_genre,us_gross,worldwide_gross,us_dvd_sales,production_budget):
    if Movie.query.filter_by(title=title).first(): # if there is a song by that title
        return "That movie already exists. Go back to the main app."
    else:
        director = get_or_create_director(director)
        distributor = get_or_create_distributor(distributor)
        movie = Movie(title=title, director_id=director.id,distributor_id=distributor.id,major_genre=major_genre,us_gross=us_gross,worldwide_gross=worldwide_gross,us_dvd_sales=us_dvd_sales,production_budget=production_budget)
        session.add(movie)
        session.commit()
        return "New movie: {} directed by {}, distributed by {}, has been saved in the list. More info: Major Genre: {}; US Gross: {}, Worldwide Gross: {}, US DVD Sales: {}, Production Budget: {}. ".format(movie.title, director.name,distributor.name,movie.major_genre,movie.us_gross,movie.worldwide_gross,movie.us_dvd_sales,movie.production_budget)

@app.route('/')
def index():
    movies = Movie.query.all()
    num_movies = len(movies)
    return render_template('index.html', num_movies=num_movies)

@app.route('/all_movies')
def see_all():
    all_movies = [] # Will be be tuple list of title, genre
    movies = Movie.query.all()
    for i in movies:
        all_movies.append((i.title)) # get list of songs with info to easily access [not the only way to do this]
    return render_template('all_movies.html',all_movies=all_movies) # check out template to see what it's doing with what we're sending!

@app.route('/all_directors')
def see_director():
    all_directors = [] # Will be be tuple list of title, genre
    directors = Director.query.all()
    for i in directors:
        all_directors.append((i.name)) # get list of songs with info to easily access [not the only way to do this]
    return render_template('all_directors.html',all_directors=all_directors)

# @app.route('/all_artists')
# def see_all_artists():
#     artists = Artist.query.all()
#     names = []
#     for a in artists:
#         num_songs = len(Song.query.filter_by(artist_id=a.id).all())
#         newtup = (a.name,num_songs)
#         names.append(newtup) # names will be a list of tuples
#     return render_template('all_artists.html',artist_names=names)

if __name__ == '__main__':
    db.create_all() # This will create database in current directory, as set up, if it doesn't exist, but won't overwrite if you restart - so no worries about that
    app.run() # run with this: python main_app.py runserver
