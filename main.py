from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import os

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///messages.db'
db = SQLAlchemy(app)

class Message(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.String(500))
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)

db.create_all()

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        msg_content = request.form['message']
        if msg_content:
            new_msg = Message(content=msg_content)
            db.session.add(new_msg)
            db.session.commit()
            os.system(f'notify-send "New Message" "{msg_content}"')
        return redirect('/')
    messages = Message.query.order_by(Message.timestamp.desc()).all()
    return render_template('index.html', messages=messages)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
