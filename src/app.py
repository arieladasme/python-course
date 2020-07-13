from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow

# CONEXION Y DEFINICION DE LA BASE DE DATOS
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root@localhost/flaskmysql'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
ma = Marshmallow(app)


class Task(db.Model):  # Creo clase Task que hereda un modelo de la db
    id = db.Column(db.Integer, primary_key=True)  # Colum: defino columna
    title = db.Column(db.String(70), unique=True)  # Columna string de 70 caracteres
    description = db.Column(db.String(100))

    def __init__(self, title, description):  # Defino y asigno datos
        self.title = title
        self.description = description


db.create_all()  # Lee clases y crea tabla


class TaskSchema(ma.Schema):  # Desde ma creo schema
    class Meta:
        field = ('id', 'title', 'description')  # Defino campos a obtener cada vez que actue en Meta


task_schema = TaskSchema()
tasks_schema = TaskSchema(many=True)  # obtengo multiples datos que cumple con los valores de Meta


# DEFINO RUTAS

@app.route('/tasks', methods=['POST'])
def create_task():
    title = request.json['title']  # Guardo req en title
    description = request.json['description']

    new_task = Task(title, description)  # Creo task y la guardo en new_task
    db.session.add(new_task)  # Guardo en la DB
    db.session.commit()  # Termino operacion
    return task_schema.jsonify(new_task)  # Retorno task al cliente


@app.route('/tasks', methods=['GET'])
def get_tasks():
    tasks = Task.query.all()  # Obtengo todas las tareas
    result = task_schema.dump(tasks)  # Genero lista de datos
    return jsonify(result)  # jsonify: desde String a JSON


@app.route('/tasks/<id>', methods=['GET'])  # <id> === :id
def get_task(id):
    task = Task.query.get(id)  # Obtengo tarea
    return task_schema.jsonify(task)


@app.route('/tasks/<id>', methods=['PUT'])
def update_task(id):
    task = Task.query.get(id)

    title = request.json['title']
    description = request.json['description']

    task.title = title
    task.description = description

    db.session.commit()
    return task_schema.jsonify(task)


@app.route('/tasks/<id>', methods=['DELETE'])
def delete_task(id):
    task = Task.query.get(id)
    db.session.delete(task)
    db.session.commit()
    return task_schema.jsonify(task)


@app.route('/', methods=['GET'])
def index():
    return task_schema.jsonify({'message': 'Welcome to my api'})


if __name__ == "__main__":  # Inicio app
    app.run(debug=True)  # debug: reinicia si detecta cambios
