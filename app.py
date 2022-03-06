from flask import Flask, render_template, url_for, request, redirect
from flask_sqlalchemy import SQLAlchemy

from datetime import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///test.db"
db = SQLAlchemy(app)

class Todo(db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    text = db.Column(db.String(1000), nullable=False)
    priority = db.Column(db.String(8), nullable=False)
    complete = db.Column(db.Integer,default=0)
    date_created = db.Column(db.DateTime, default=datetime.utcnow)
    
    def __repr__(self):
        return '<Task %r>' % self.id

@app.route('/', methods=['POST','GET'])
def home(): 
    if request.method == 'POST':
        task_content = request.form['text']
        task_priority = request.form['priority']
        new_task = Todo(text=task_content,priority=task_priority)
        
        try:
            db.session.add(new_task)
            db.session.commit( )
            return redirect('/')
        except: 
            return 'tjere wsa an error addig task'
    else:
        Tasks = Todo.query.order_by(Todo.date_created).all()
        return render_template("index.html", tasks=Tasks)
    
@app.route('/delete/<int:id>')
def delete(id): 
    content = Todo.query.get_or_404(id)
    try:
        db.session.delete(content)
        db.session.commit()
        return redirect('/')
    except: 
        return "some error in deleting the task..recheck the code in delete"

@app.route('/update/<int:id>', methods=['POST','GET'])
def update(id):
    task = Todo.query.get_or_404(id)    
    if request.method == 'POST':
        task.text = request.form['text']
        task.priority = request.form['priority']
        print(task.text,task.priority)
        print(task)
        try: 
            db.session.commit()
            return redirect('/')
        except: 
            return "some error in updating the task"
    else: 
        return render_template('update.html',task=task)
     
if __name__ == "__main__":
    app.run(debug=True)     