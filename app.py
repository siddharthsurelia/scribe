from flask import Flask, request, render_template, redirect
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.sql import func
from os import path

DBNAME = "note.db"
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///'+DBNAME
db = SQLAlchemy(app)

class Note(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    dataNote = db.Column(db.String(65535), unique=True)
    datetime = db.Column(db.String(50), default=func.now())

@app.route('/create', methods=["GET", "POST"])
def create_note():
    dataNote = str(request.form.get("dataNote"))
    
    n = Note(dataNote=dataNote)
    db.session.add(n)
    id = db.session.commit()
    
    return redirect("/read")

@app.route('/read')
def read_note():
    notes = Note.query.all()
    res = []

    for note in notes:
        data = {
            "id": note.id,
            "dataNote": note.dataNote,
            "datetime": note.datetime
        }
        res.append(data)

    # return res, 200
    return render_template("index.html", data=res)

@app.route('/read/<int:id>')
def read_note_one(id):
    n = Note.query.get(id)

    if n:
        data = {
            "id": n.id,
            "dataNote": n.dataNote,
            "datetime": n.datetime
        }
        return data, 200
    else:
        return "Not Found", 404

@app.route('/update/<int:id>')
def update_note(id):
    dataNote = request.form.get("dataNote")

    n = Note.query.get(id)

    if not n:
        return "Not Found", 404

    n.dataNote = dataNote

    db.session.commit()

    return "Updated", 201

@app.route('/delete/<int:id>')
def delete_note(id):
    n = Note.query.get(id)

    if not n:
        return "Not Found", 404

    db.session.delete(n)
    db.session.commit()

    return redirect("/read")

if __name__ == "__main__":
    if not path.exists("instance/"+DBNAME):
        with app.app_context():
            db.create_all()
    app.run(host='0.0.0.0', port=8080, debug=True)