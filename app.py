# -- Import section --
from flask import Flask
from flask import render_template
from flask import request
from flask import url_for
from flask import redirect
from flask import request
from flask_pymongo import PyMongo
import os
from dotenv import load_dotenv
import datetime

import model

load_dotenv()

# -- Initialization section --
app = Flask(__name__)
app.jinja_env.globals['current_time'] = datetime.datetime.now()


MONGO_DBNAME = os.getenv("MONGO_DBNAME")
MONGO_DB_USERNAME = os.getenv("MONGO_DB_USERNAME")
MONGO_DB_PASSWORD = os.getenv("MONGO_DB_PASSWORD")

app.config['MONGO_DBNAME'] = MONGO_DBNAME
app.config['MONGO_URI'] = f'mongodb+srv://{MONGO_DB_USERNAME}:{MONGO_DB_PASSWORD}@cluster0.94cb3.mongodb.net/{MONGO_DBNAME}?retryWrites=true'

mongo = PyMongo(app)

# -- Routes section --

@app.route('/')
@app.route('/index')
def index():
    data = {
    }
    return render_template('index.html', data=data)

@app.route('/about_us')
def about_us():
    data = {
    }
    return render_template('aboutUs.html', data=data)

@app.route('/users')
def users_view():
    data = {
    'users':mongo.db.users.find({}),
    }
    return render_template('usersView.html', data=data)

@app.route('/users/<USER>')
def users_detail(USER):
    data = {
    'user':mongo.db.users.find_one({'name':USER}),
    'reviews':mongo.db.reviews.find({'user':USER}),
    }
    return render_template('usersDetail.html', data=data)

@app.route('/users/add', methods=['GET','POST'])
def users_add():
    if request.method == 'GET':
        return ""
        # data = {
        # }
        # return render_template('usersAdd.html', data=data)
    elif request.method == 'POST':
        form = request.form
        user = {
        'name':form['searchForm'],
        }
        print(user)
        return render_template('index.html', user=user)

# @app.route('/users/add', methods=['GET','POST'])
# def users_add():
#     if request.method == 'GET':
#         data = {
#         }
#         return render_template('usersAdd.html', data=data)
#     else:
#         form = request.form
#         user = {
#         'name':form['userName'],
#         }

#         return redirect(url_for('users_view'))
@app.route('/movie')
def movie_view():
    data = {
    'movie':mongo.db.movie.find({}),
    }
    return render_template('movieView.html', data=data)

@app.route('/movie/<title>')
def movie_detail(title):
    data = {
    'movie':mongo.db.movie.find_one({'title':title}),
    'reviews':mongo.db.reviews.find({'title':title}),
    }
    return render_template('movieDetail.html', data=data)

@app.route('/movie/add', methods=['GET','POST'])
def movie_add():
    if request.method == 'GET':
        data = {
        }
        return render_template('movieAdd.html', data=data)
    else:
        form = request.form
        movie = {
        'title':form['movieTitle'],
        'genre':form['movieGenre'],
        }
        data = {
        'movie':movie
        }
        mongo.db.movie.insert(movie)
        return render_template('movieDetail.html', data=data)


@app.route('/review/add', methods=['GET','POST'])
def reviews_add():
    if request.method == 'GET':
        data = {
            'movie':mongo.db.movie.find({}),
            'users':mongo.db.users.find({}),
        }
        return render_template('reviewsAdd.html', data=data)
    else:
        form = request.form
        review = {
        'title':form['movieTitle'],
        'user':form['reviewUser'],
        'rating':int(form['reviewRating']),
        'review':form['reviewText'],
        }
        data = {
        'review':review
        }
        mongo.db.reviews.insert(review)
        return redirect("https://0.0.0.0:5000" + url_for('movie_detail',title=form['movieTitle']))



#### Add new routes below this line ###

@app.route('/search', methods = ['GET','POST'])
def search():
    if request.method == 'POST':
        form = request.form
        query = {
            'title':form['search']
        }
        document = mongo.db.movie.find_one(query)
        if document:
            return redirect("https://0.0.0.0:5000" + url_for('movie_detail',title=form['search']))
        else:
            return redirect("https://0.0.0.0:5000" + url_for('movie_nf'))
    else:
        return redirect("https://0.0.0.0:5000" + url_for('index'))

@app.route('/movie_nf')
def movie_nf():
    data = {
    }
    return render_template('movieNf.html', data=data)