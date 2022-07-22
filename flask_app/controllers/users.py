from flask import render_template, redirect, request, session, flash
from flask_app import app
from flask_app.models.user import User
from flask_app.models.subscription import Subscription
from flask_app.models import magazine
from flask_bcrypt import Bcrypt
bcrypt = Bcrypt(app)

@app.route('/')
def login_page():
    return render_template('log_n_reg.html')

@app.route('/login', methods=['POST'])
def login():
    if not User.validate_login(request.form):
        return redirect('/')
    user = User.get_user_by_email(request.form)
    if user:
        if not bcrypt.check_password_hash(user.password, request.form['password']):
            flash('Email/password combo not correct')
            return redirect('/')
        session['user_id'] = user.id
        flash('successful login')
        return redirect('/dashboard')
    flash('That email is not tied to an account')
    return redirect('/')

@app.route('/register', methods=['POST'])
def register():
    if not User.validate_register(request.form):
        return redirect('/')
    pw_hash = bcrypt.generate_password_hash(request.form['password'])
    register_data = {
        'first_name': request.form['first_name'],
        'last_name': request.form['last_name'],
        'email': request.form['email'],
        'password': pw_hash
    }
    user_id = User.register_user(register_data)
    session['user_id'] = user_id
    flash('registration successful')
    return redirect('/dashboard')

@app.route('/user/update', methods=['POST'])
def update():
    user_id = session['user_id']
    if not User.validate_update(request.form):
        return redirect(f'/user/{user_id}')
    User.update_user(request.form)
    flash('update successful', 'update_error')
    return redirect(f'/user/{user_id}')


@app.route('/user/<int:id>')
def account_page(id):
    data = {
        'id': id
    }
    user_data = {
        'user_id': int(session['user_id'])
    }
    magazines = magazine.Magazine.get_all_from_user(user_data)
    
    return render_template('account.html', user = User.get_user_by_id(data), magazines = magazines) #count = magazine.Magazine.num_subscribers()

@app.route('/user/subscribe', methods=['POST'])
def subscribe():
    Subscription.save(request.form)
    return redirect(f'/dashboard')


@app.route('/logout')
def logout():
    session.clear()
    return redirect('/')