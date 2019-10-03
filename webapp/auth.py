from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_user, logout_user, login_required, current_user
from .model import User
from . import db

auth = Blueprint('auth', __name__)

# базовый интерфейс
@auth.route('/')                      
def main():
    return render_template('user_out.html')

# базовый интерфейс (в действии)
@auth.route('/', methods=['POST'])
def enter_or_reg():
    button = request.form.get('action')
    if button == 'Войти':
        return redirect(url_for('auth.enter'))
    elif button == 'Зарегистрироваться':
        return redirect(url_for('auth.reg'))

# интерфейс для авторизации (в действии)
@auth.route('/enter')
def enter():
    return render_template('user_auth.html')

# интерфейс для авторизации (в действии)
@auth.route('/enter', methods=['POST'])
def try_to_enter():
    button = request.form.get('action')
    if button == '<< Назад':
        return redirect(url_for('auth.main'))
    elif button == 'Войти >>':
        name     = request.form.get('user')
        password = request.form.get('pass')
        try: # убеждаемся, что Имя и Пароль - непустые значения
            assert name
            assert password
        except AssertionError:
            flash('* Необходимо заполнить все поля')
            return redirect(url_for('auth.enter'))
        else:
            name = name.lower().strip() # приводим имя к стандартной форме
            user = User.query.filter_by(name=name).first()
            try: # убеждаемся, что пользователь есть в базе, и что пароль верен
                assert user
                assert password == user.password
            except AssertionError:
                flash('* Пользователь не зарегистрирован либо пароль неверный')
                return redirect(url_for('auth.enter'))
            else:
                login_user(user)
                return redirect(url_for('auth.profile'))

# интерфейс для регистрации:
@auth.route('/register')
def reg():
    return render_template('user_reg.html')

# интерфейс для регистрации (в действии)
@auth.route('/register', methods=['POST'])
def try_to_reg():
    button = request.form.get('action')
    if button == '<< Назад':
        return redirect(url_for('auth.main'))
    elif button == 'Регистрация и вход >>':
        name         = request.form.get('user')
        password     = request.form.get('pass')
        verification = request.form.get('pass_1')
        try: # убеждаемся, что необходимые поля заполнены
            assert name
            assert password
            assert verification
        except AssertionError:
            flash('* Необходимо заполнить все поля')
            return redirect(url_for('auth.reg'))
        else:
            # проверяем, нет ли в базе пользователей с таким же именем
            name = name.lower().strip() # приводим имя к стандартной форме
            user = User.query.filter_by(name=name).first()
            if user:
                flash('* Пользователь с таким именем уже существует')
                return redirect(url_for('auth.reg'))
            try: # убеждаемся, что пароль и его подтверждение совпадают
                assert password == verification
            except AssertionError:
                flash('* Пароли не совпадают')
                return redirect(url_for('auth.reg'))
            else:
                new_user = User(name=name, password=password)
                db.session.add(new_user)
                db.session.commit()
                login_user(new_user)
                return redirect(url_for('auth.profile'))

# интерфейс авторизованного пользователя
@auth.route('/profile')
@login_required
def profile():
    return render_template('user_in.html', name=current_user)

# интерфейс авторизованного пользователя (в действии)
@auth.route('/profile', methods=['POST'])
@login_required
def profile_out():
    logout_user()
    return redirect(url_for('auth.main'))

