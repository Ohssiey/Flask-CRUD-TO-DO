#Imports
from flask import Flask, render_template, redirect, url_for, request
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime



#My Application
app = Flask(__name__)



#Database configuration
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///database.db"
db = SQLAlchemy(app)



#Database Model- A model is a row of data
class mytask(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.String(100), nullable=False)
    complete = db.Column(db.Integer, default=0)
    created = db.Column(db.DateTime, default=datetime.now)
    
    def __repr__(self):
        return f"Task {self.id}"
    


#Routes

#HOMEPAGE
@app.route("/", methods=["POST","GET"])
def index():
    #Add Task
    if request.method == "POST":
        current_task = request.form["content"] # i.e from the html form.
        new_task = mytask(content=current_task)
        
        #Block to commit to the database
        try:
            db.session.add(new_task)
            db.session.commit()
            return redirect("/")
        except Exception as e:
            print(f"ERROR: {e}")
            return f"ERROR: {e}"
        
    #See all current task
    else:
        tasks = mytask.query.order_by(mytask.created).all()
        return render_template("index.html", tasks=tasks)
    
    
#DELETE
@app.route("/delete/<int:id>")
def delete(id:int):
    delete_task = mytask.query.get_or_404(id)
    try:
        db.session.delete(delete_task)
        db.session.commit()
        return redirect("/")
    except Exception as e:
        return f"ERROR: {e}"
    
    
#EDIT{}
@app.route("/edit/<int:id>", methods=["POST","GET"])
def edit(id:int):
    task = mytask.query.get_or_404(id)
    if request.method == "POST":
        task.content = request.form["content"]
        try:
            db.session.commit()
            return redirect("/")
        except Exception as e:
            return f"ERROR: {e}"
        
    else:
        return render_template("edit.html", task=task)




#Runner and Debugger
if __name__ == "__main__":
    with app.app_context():#Moves this
        db.create_all()#below the db model when ready for deployment
        
    app.run(debug=True)