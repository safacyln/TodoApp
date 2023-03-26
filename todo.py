from flask import Flask,render_template,request,redirect,url_for
from flask_sqlalchemy import SQLAlchemy

# create the extension
db = SQLAlchemy()
# create the app
app = Flask(__name__)
# configure the SQLite database, relative to the app instance folder
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:////Users/mustafaceylan/Desktop/project/TodoApp/todo.db"
# initialize the app with the extension
db.init_app(app)

@app.route("/")
def index():
    todos = Todo.query.all()
    return render_template("index.html",todos=todos)


@app.route("/complate/<string:id>")
def complateTodo(id):
    todo = Todo.query.filter_by(id=id).first()
    if (todo.complate == False):
        todo.complate = True
    else:
        todo.complate = False
    db.session.commit()
    return redirect(url_for("index"))

@app.route("/delete/<string:id>")
def removeTodo(id):
    todo = Todo.query.filter_by(id=id).first()
    db.session.delete(todo)
    db.session.commit()
    return redirect(url_for("index"))

@app.route("/add",methods = ["POST"])
def addTodo():
    task_title = request.form.get("task_title")
    task_content = request.form.get("task_content")

    newTodo = Todo(title=task_title, task_content=task_content, complate=False)
    db.session.add(newTodo)
    db.session.commit()
    return redirect(url_for("index"))

class Todo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(80))
    content = db.Column(db.Text)
    complate = db.Column(db.Boolean)

with app.app_context():
    db.create_all()

if __name__ == "__main__":
    app.run(debug=True)
