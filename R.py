### Desarrollo de la Web App MVC para la Caja Nacional de Salud con Flask

Para abordar este proyecto, seguiremos los principios del patrón MVC (Modelo-Vista-Controlador) y utilizaremos Flask para la creación del backend, SQLAlchemy como ORM para la base de datos SQLite y Flask-Login para la autenticación de los usuarios. A continuación, detallo los pasos necesarios para construir esta aplicación.

#### Estructura de Carpetas

```plaintext
app/
|-- __init__.py
|-- config.py
|-- models.py
|-- views.py
|-- controllers/
|   |-- __init__.py
|   |-- auth.py
|   |-- patients.py
|-- templates/
|   |-- base.html
|   |-- index.html
|   |-- login.html
|   |-- register.html
|   |-- list_patients.html
|   |-- create_patient.html
|   |-- update_patient.html
|-- static/
|   |-- css/
|   |-- js/
```

#### Archivos y Código

1. **app/__init__.py**

    ```python
    from flask import Flask
    from flask_sqlalchemy import SQLAlchemy
    from flask_login import LoginManager

    app = Flask(__name__)
    app.config.from_object('config')

    db = SQLAlchemy(app)
    login_manager = LoginManager()
    login_manager.init_app(app)
    login_manager.login_view = 'auth.login'

    from app.controllers import auth, patients

    app.register_blueprint(auth.bp)
    app.register_blueprint(patients.bp)

    db.create_all()

    from app.models import User

    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))
    ```

2. **app/config.py**

    ```python
    import os

    basedir = os.path.abspath(os.path.dirname(__file__))

    class Config:
        SECRET_KEY = 'your_secret_key'
        SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'app.db')
        SQLALCHEMY_TRACK_MODIFICATIONS = False

    app.config.from_object(Config)
    ```

3. **app/models.py**

    ```python
    from flask_sqlalchemy import SQLAlchemy
    from flask_login import UserMixin
    from werkzeug.security import generate_password_hash, check_password_hash
    from app import db

    class User(UserMixin, db.Model):
        id = db.Column(db.Integer, primary_key=True, autoincrement=True)
        username = db.Column(db.String(150), unique=True, nullable=False)
        password = db.Column(db.String(150), nullable=False)
        role = db.Column(db.String(50), nullable=False)

        def set_password(self, password):
            self.password = generate_password_hash(password)

        def check_password(self, password):
            return check_password_hash(self.password, password)

    class Patient(db.Model):
        id = db.Column(db.Integer, primary_key=True, autoincrement=True)
        name = db.Column(db.String(150), nullable=False)
        lastname = db.Column(db.String(150), nullable=False)
        ci = db.Column(db.String(20), unique=True, nullable=False)
        birth_date = db.Column(db.String(50), nullable=False)
    ```

4. **app/controllers/auth.py**

    ```python
    from flask import Blueprint, render_template, redirect, url_for, request, flash
    from flask_login import login_user, logout_user, login_required, current_user
    from werkzeug.security import generate_password_hash, check_password_hash
    from app.models import User
    from app import db

    bp = Blueprint('auth', __name__)

    @bp.route('/login', methods=['GET', 'POST'])
    def login():
        if request.method == 'POST':
            username = request.form['username']
            password = request.form['password']
            user = User.query.filter_by(username=username).first()

            if user and user.check_password(password):
                login_user(user)
                return redirect(url_for('patients.list_patients'))

            flash('Invalid username or password')
        return render_template('login.html')

    @bp.route('/logout')
    @login_required
    def logout():
        logout_user()
        return redirect(url_for('auth.login'))

    @bp.route('/users', methods=['GET', 'POST'])
    def register():
        if request.method == 'POST':
            username = request.form['username']
            password = request.form['password']
            role = request.form['role']

            user = User(username=username, role=role)
            user.set_password(password)
            db.session.add(user)
            db.session.commit()
            return redirect(url_for('auth.login'))
        return render_template('register.html')
    ```

5. **app/controllers/patients.py**

    ```python
    from flask import Blueprint, render_template, request, redirect, url_for, flash
    from flask_login import login_required, current_user
    from app.models import Patient
    from app import db

    bp = Blueprint('patients', __name__)

    @bp.route('/patients')
    @login_required
    def list_patients():
        patients = Patient.query.all()
        return render_template('list_patients.html', patients=patients)

    @bp.route('/patients/create', methods=['GET', 'POST'])
    @login_required
    def create_patient():
        if request.method == 'POST':
            name = request.form['name']
            lastname = request.form['lastname']
            ci = request.form['ci']
            birth_date = request.form['birth_date']

            patient = Patient(name=name, lastname=lastname, ci=ci, birth_date=birth_date)
            db.session.add(patient)
            db.session.commit()
            return redirect(url_for('patients.list_patients'))
        return render_template('create_patient.html')

    @bp.route('/patients/<int:id>/update', methods=['GET', 'POST'])
    @login_required
    def update_patient(id):
        patient = Patient.query.get_or_404(id)
        if request.method == 'POST':
            patient.name = request.form['name']
            patient.lastname = request.form['lastname']
            patient.ci = request.form['ci']
            patient.birth_date = request.form['birth_date']

            db.session.commit()
            return redirect(url_for('patients.list_patients'))
        return render_template('update_patient.html', patient=patient)

    @bp.route('/patients/<int:id>/delete', methods=['GET', 'POST'])
    @login_required
    def delete_patient(id):
        patient = Patient.query.get_or_404(id)
        if request.method == 'POST':
            db.session.delete(patient)
            db.session.commit()
            return redirect(url_for('patients.list_patients'))
        return render_template('delete_patient.html', patient=patient)
    ```

6. **Plantillas HTML (Ubicadas en `app/templates`)**

    **base.html**
    ```html
    <!doctype html>
    <html lang="en">
      <head>
        <meta charset="utf-8">
        <title>Gestión de Pacientes</title>
        <link rel="stylesheet" href="{{ url_for('static', filename='css/style.css') }}">
      </head>
      <body>
        <header>
          <nav>
            <ul>
              <li><a href="{{ url_for('patients.list_patients') }}">Lista de Pacientes</a></li>
              <li><a href="{{ url_for('auth.logout') }}">Logout</a></li>
            </ul>
          </nav>
        </header>
        <main>
          {% block content %}{% endblock %}
        </main>
      </body>
    </html>
    ```

    **login.html**
    ```html
    {% extends "base.html" %}
    {% block content %}
    <form action="{{ url_for('auth.login') }}" method="post">
      <label for="username">Username</label>
      <input type="text" id="username" name="username" required>
      <label for="password">Password</label>
      <input type="password" id="password" name="password" required>
      <button type="submit">Login</button>
    </form>
    {% endblock %}
    ```

    **register.html**
    ```html
    {% extends "base.html" %}
    {% block content %}
    <form action="{{ url_for('auth.register') }}" method="post">
      <label for="username">Username</label>
      <input type="text" id="username" name="username" required>
      <label for="password">Password</label>
      <input type="password" id="password" name="password" required>
      <label for="role">Role</label>
      <select id="role" name="role">
        <option value="admin">Admin</option>
        <option value="doctor">Doctor</option>
      </select>
      <button type="submit">Register</button>
    </form>
    {% endblock %}
    ```

    **list_patients.html**
    ```html
    {% extends "base.html" %}
    {% block content %}
    <h1>Lista de Pacientes</h1>
    <table>
      <tr>
        <th>ID</th>
        <th>Name</th>
        <th>Lastname</th>
        <th>CI</th>
        <th>Birth Date</th>
        <th>Actions</th>
      </tr>
      {% for patient in patients %}
      <tr>
        <td>{{ patient.id }}</td>
        <td>{{ patient.name }}</td>
        <td>{{ patient.lastname }}</td>
        <td>{{ patient.ci }}</td>
        <td>{{ patient.birth_date }}</
