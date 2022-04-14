"""Server for movie ratings app."""

from flask import (Flask, render_template, request, flash, session,
                   redirect)
from model import connect_to_db, db
import crud

from jinja2 import StrictUndefined

app = Flask(__name__)
app.secret_key = "dev"
app.jinja_env.undefined = StrictUndefined


# Replace this with routes and view functions!
@app.route('/')
def homepage():
    """View homepage"""

    return render_template('homepage.html')


@app.route('/movies')
def all_movies():
    """View all movies"""
    
    movies = crud.get_movies()
    return render_template('all_movies.html', movies = movies)


@app.route('/movies/<movie_id>')
def show_movie(movie_id):
    """Show details on a particular movie."""
    
    movie= crud.get_movie_by_id(movie_id)
    
    return render_template('movie_details.html', movie = movie)

@app.route('/movies/<movie_id>/rating', methods=["POST"])
def add_rating(movie_id):
    """Add rating for specific movie"""
#check if in session

    if session:
        score = request.form.get('score')
        user = crud.get_user_by_email(session['user_email'])
        movie = crud.get_movie_by_id(movie_id)


        rating = crud.create_rating(user, movie, int(score))

        db.session.add(rating)
        db.session.commit()

        flash(f'Your rating has been added! It is {score}.')
    else:
        flash('You must be logged fin, in order to submit a rating.')
    
    return redirect(f'/movies/{movie_id}')



@app.route('/users')
def all_users():
    """View all users"""

    users = crud.get_users()

    return render_template('all_users.html', users=users)



@app.route('/users', methods=["POST"])
def register_user():
    """Create a new user."""

    email = request.form.get('email')
    password = request.form.get('password')

    user = crud.get_user_by_email(email)

    if user:
        flash("Cannot create an account with that email. Try again.")
    else:
        user = crud.create_user(email, password)
        db.session.add(user)
        db.session.commit()
        flash("Account created! Please log in.")

    return redirect("/")


@app.route('/login', methods=["POST"])
def login_user():
    """User logs in"""

    email = request.form.get('email')
    password = request.form.get('password')

    user = crud.get_user_by_email(email)

    if not user or user.password != password:
        flash("The email or password you entered was incorrect!")
    else:
        # Log in user by storing the user's email in session
        session["user_email"] = user.email
        flash(f"Welcome back, {user.email}!")

    return redirect("/")




@app.route('/users/<user_id>')
def show_user(user_id):
    """Show details on a particular user"""

    user = crud.get_user_by_id(user_id)
    
    return render_template('user_details.html', user=user)

if __name__ == "__main__":
    # DebugToolbarExtension(app)
    connect_to_db(app)
    app.run(host="0.0.0.0", debug=True)
