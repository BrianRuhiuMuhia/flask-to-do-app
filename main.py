from flask import Flask,render_template,request,url_for,redirect
from flask_sqlalchemy import SQLAlchemy
app=Flask(__name__)
DB_NAME="database.sqlite"
app.config['SQLALCHEMY_DATABASE_URI']=f'sqlite:///{DB_NAME}'
db=SQLAlchemy(app=app)
db.init_app(app)
class Database(db.Model):
    id=db.Column(db.Integer,primary_key=True)
    text=db.Column(db.String(100))
    checked=db.Column(db.Boolean)
@app.route('/')
def home_page():
    items=Database.query.all()
    return render_template("index.html",list=items)
@app.route("/delete<id>")
def delete(id):
    item=Database.query.filter_by(id=id).first()
    db.session.delete(item)
    db.session.commit()
    return redirect(url_for("home_page"))
@app.route("/add",methods=['POST','GET'])
def add():
    input_text=request.form.get("input")
    if not input_text:
        return redirect(url_for("home_page"))
    new_todo=Database(text=input_text)
    db.session.add(new_todo)
    db.session.commit()
    return redirect(url_for("home_page"))
@app.route("/search",methods=['POST','GET'])
def search():
    search_item=request.form.get("search")
    if not search_item:
        return redirect(url_for("home_page"))
    search=Database.query.filter_by(text=search_item)
    return render_template("index.html",list=search)
if __name__ == "__main__":
    db.create_all()
    app.run(debug=True)