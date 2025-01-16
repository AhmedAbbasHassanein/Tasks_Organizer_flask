from flask import Flask, render_template, redirect, request
from flask_scss import Scss
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app=Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///database.db"
db=SQLAlchemy(app)

class MyTask(db.Model):
    id=db.Column(db.Integer, primary_key=True)
    content=db.Column(db.String(100),nullable=False)
    due=db.Column(db.DateTime)
    created=db.Column(db.DateTime, default=datetime.utcnow)
    
    def __repr__(self):
        return f"Task{self.id}"

@app.route('/', methods=["POST","GET"])
def index():
    # Add new task
    if request.method=="POST":       
        current_task=request.form['content']
        current_due= datetime.strptime(request.form['due'],'%Y-%m-%d')
        new_task=MyTask(content=current_task,due=current_due)
        try:
            db.session.add(new_task)
            db.session.commit()
            return redirect('/') 
        except Exception as e:
            return f"Error : {e}"
    # See All current tasks
    tasks=MyTask.query.order_by(MyTask.created).all()
    return render_template('index.html',tasks=tasks)

# Delete an item
@app.route("/delete/<int:id>")
def delete(id):
    delete_task=MyTask.query.get_or_404(id)
    try:
        db.session.delete(delete_task)
        db.session.commit()
        return redirect("/")
    except Exception as e:
        return f"Error : {e}"
    
# Update an item
@app.route("/edit/<int:id>", methods=["GET","POST"])
def edit(id):
    task=MyTask.query.get_or_404(id)
    if request.method=="POST":
        task.content= request.form['content']
        task.due=datetime.strptime(request.form['due'],'%Y-%m-%d')
        try:
            db.session.commit()
            return redirect("/")
        except Exception as e:
            return f"Error : {e}"
    else:
        return render_template('edit.html',task=task)

if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    app.run(debug=True)


