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
