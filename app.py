# app.py
from flask import Flask, render_template, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime, date
import os

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# Models
class Pet(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    level = db.Column(db.Integer, default=1)
    experience = db.Column(db.Integer, default=0)
    last_fed = db.Column(db.DateTime)
    last_played = db.Column(db.DateTime)
    last_bathed = db.Column(db.DateTime)
    last_reset = db.Column(db.Date, default=date.today)
    fed_today = db.Column(db.Boolean, default=False)
    played_today = db.Column(db.Boolean, default=False)
    bathed_today = db.Column(db.Boolean, default=False)

    def to_dict(self):
        return {
            'name': self.name,
            'level': self.level,
            'experience': self.experience,
            'last_fed': self.last_fed,
            'last_played': self.last_played,
            'last_bathed': self.last_bathed,
            'fed_today': self.fed_today,
            'played_today': self.played_today,
            'bathed_today': self.bathed_today
        }


@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/pet', methods=['GET', 'POST'])
def pet():
    pet = Pet.query.first()
    today = date.today()

    if pet and pet.last_reset != today:
        pet.last_reset = today
        pet.fed_today = False
        pet.played_today = False
        pet.bathed_today = False
        db.session.commit()

    if request.method == 'POST':
        data = request.json
        if not pet:
            pet = Pet(name=data['name'])
            db.session.add(pet)
        else:
            action = data['action']
            now = datetime.utcnow()
            if action == 'feed' and not pet.fed_today:
                pet.last_fed = now
                pet.experience += 10
                pet.fed_today = True
            elif action == 'play' and not pet.played_today:
                pet.last_played = now
                pet.experience += 15
                pet.played_today = True
            elif action == 'bathe' and not pet.bathed_today:
                pet.last_bathed = now
                pet.experience += 5
                pet.bathed_today = True

            if pet.experience >= 100:
                pet.level += 1
                pet.experience = 0

        db.session.commit()
        return jsonify(pet.to_dict())

    return jsonify(pet.to_dict() if pet else {})

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run()
