import json
import os
from flask import Blueprint, render_template, request, redirect, session, flash

def create_auth_routes(monitor):
    auth_bp = Blueprint('auth', __name__)
    USERS_FILE = 'data/users.json'

    def load_users():
        if os.path.exists(USERS_FILE):
            try:
                with open(USERS_FILE, 'r', encoding='utf-8') as f:
                    return json.load(f)
            except: return {}
        return {}

    def save_users(users):
        os.makedirs(os.path.dirname(USERS_FILE), exist_ok=True)
        with open(USERS_FILE, 'w', encoding='utf-8') as f:
            json.dump(users, f, indent=4, ensure_ascii=False)

    @auth_bp.route('/login', methods=['GET', 'POST'])
    def login():
        if request.method == 'POST':
            username = request.form.get('username', '').strip()
            password = request.form.get('password', '').strip()
            users = load_users()
            if username in users and users[username] == password:
                session['user'] = username
                return redirect('/')
            flash('Ошибка: проверьте логин или пароль')
        return render_template('login.html')

    @auth_bp.route('/register', methods=['GET', 'POST'])
    def register():
        if request.method == 'POST':
            username = request.form.get('username', '').strip()
            password = request.form.get('password', '').strip()
            users = load_users()
            if not username or not password:
                flash('Заполните все поля')
            elif username in users:
                flash('Пользователь уже существует')
            else:
                users[username] = password
                save_users(users)
                return redirect('/login')
        return render_template('register.html')

    @auth_bp.route('/logout')
    def logout():
        session.clear()
        return redirect('/')

    return auth_bp