from flask import render_template, redirect, request, session, flash
from flask_app import app
from flask_app.models.magazine import Magazine
from flask_app.models.user import User


@app.route('/dashboard')
def show_magazines():
    if 'user_id' not in session:
        flash('You must be logged into view the dashboard!', 'log_error')
        return redirect('/')
    user_data = {
        'id': session['user_id']
    }
    return render_template('dashboard.html', magazines=Magazine.get_all(), user = User.get_user_by_id(user_data))

@app.route('/magazine/create')
def add_magazine_render():
    if session['user_id'] == '':
        return redirect('/logout')
    return render_template('new_magazine.html')

@app.route('/magazine/<int:id>')
def show_magazine(id):
    data = {
        "id": id
    }
    user_data = {
        'id': int(session['user_id'])
    }
    user = User.get_user_by_id(user_data)
    magazine=Magazine.get_one(data)
    return render_template("show_magazine.html", magazine = magazine, user=user) #subscribers = Magazine.get_magazine_subscribers(data)) 
        
        # {% for subsciber in subscribers.subscribers %}
        # <p>- {{subscriber['first_name']}} {{subscriber.last_name}}</p>
        # {% endfor %}


@app.route('/magazine/create/save', methods=["POST"])
def create_magazine():
    if not Magazine.validate_magazine(request.form):
        return redirect('/magazine/create')
    Magazine.create_magazine(request.form)
    return redirect('/dashboard')


@app.route('/magazine/delete/<int:id>', methods=['POST'])
def delete_magazine(id):
    data = {
        "id": id
    }
    Magazine.delete(data)
    return redirect('/dashboard')