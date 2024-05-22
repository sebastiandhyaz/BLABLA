{% extends "base.html" %}
{% block content %}
<h1>Lista de Pacientes</h1>
<table>
  <tr>
    <th>ID</th>
    <th>Nombre</th>
    <th>Apellido</th>
    <th>CI</th>
    <th>Fecha de Nacimiento</th>
    <th>Acciones</th>
  </tr>
  {% for patient in patients %}
  <tr>
    <td>{{ patient.id }}</td>
    <td>{{ patient.name }}</td>
    <td>{{ patient.lastname }}</td>
    <td>{{ patient.ci }}</td>
    <td>{{ patient.birth_date }}</td>
    <td>
      <a href="{{ url_for('patients.update_patient', id=patient.id) }}">Editar</a>
      <a href="{{ url_for('patients.delete_patient', id=patient.id) }}">Eliminar</a>
    </td>
  </tr>
  {% endfor %}
</table>
{% if current_user.role == 'admin' %}
<a href="{{ url_for('patients.create_patient') }}">Crear Nuevo Paciente</a>
{% endif %}
{% endblock %}
