from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///todo.db"
app.config['SQLALCHEMY_TRACK_MODIFICATION'] = False
db = SQLAlchemy(app)


class Todo(db.Model):
    sno = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(30), nullable=False)
    desc = db.Column(db.String(500), nullable=False)
    date_created = db.Column(db.DateTime, default=datetime.utcnow())

    def __repr__(self) -> str:
        return f"{self.sno} - {self.title}"


@app.route('/', methods=['GET', 'POST'])
def home():
    if request.method == 'POST':
        title = request.form['title']
        desc = request.form['desc']
        todo = Todo(title=title, desc=desc)
        db.session.add(todo)
        db.session.commit()
    alltodos = Todo.query.all()
    return render_template('index.html', alltodos=alltodos)


@app.route('/delete/<int:sno>')
def delete(sno):
    delete_todo = Todo.query.filter_by(sno=sno).first()
    db.session.delete(delete_todo)
    db.session.commit()
    return redirect('/')


@app.route('/update/<int:sno>', methods=['GET', 'POST'])
def update(sno):
    if request.method == 'POST':
        title = request.form['title']
        desc = request.form['desc']
        todo_update = Todo.query.filter_by(sno=sno).first()
        todo_update.title = title
        todo_update.desc = desc
        db.session.add(todo_update)
        db.session.commit()
        return redirect("/")

    update_todo = Todo.query.filter_by(sno=sno).first()
    return render_template('update.html', update_todo=update_todo)


if __name__ == "__main__":
    app.run(debug=True, port=8000)
