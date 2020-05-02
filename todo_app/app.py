from flask import Flask, render_template, redirect, request, redirect, url_for, jsonify, abort
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
import sys

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://prudhvi:050895@localhost:5432/todoapp'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)
migrate = Migrate(app, db)


class Todo(db.Model):
    __tablename__ = 'todos'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(), nullable=False)
    completed = db.Column(db.Boolean, nullable=False, default=False)

    def __repr__(self):
        return f'<todo id: {self.id}, name: {self.name}>'


# db.create_all()


@app.route('/todos/create', methods=['POST'])
def create_todo():
    name = request.get_json()['description']

    error = False
    body = {}

    try:
        todo = Todo(name=name)
        db.session.add(todo)
        db.session.commit()
        body['name'] = todo.name
    except:
        db.session.rollback()
        error = True
        print(sys.exc.info())
    finally:
        db.session.close()
        if not error:
            return jsonify(body)
        else:
            return abort(400)


@app.route('/todos/<todo_id>', methods=['DELETE'])
def delete_todo(todo_id):
    print(todo_id)
    try:
        todo = Todo.query.get(todo_id)
        db.session.delete(todo)
        db.session.commit()
    except:
        db.session.rollback()
    finally:
        db.session.close()

    return jsonify({'success': True})


@app.route('/todos/<todo_id>/set-completed', methods=['POST'])
def set_completed_todo(todo_id):
    try:
        completed = request.get_json()['completed']
        todo = Todo.query.get(todo_id)
        todo.completed = completed
        db.session.commit()
    except:
        db.session.rollback()
    finally:
        db.session.close()

    return redirect(url_for('index'))


@app.route('/')
def index():
    data = Todo.query.order_by('id').all()

    return render_template('index.html', data=data)


if __name__ == '__main__':
    app.debug = True
    app.run()
