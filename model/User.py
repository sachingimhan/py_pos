from application import db
from dataclasses import dataclass


@dataclass
class User(db.Model):
    id: int
    email: str
    password: str

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    email = db.Column(db.String(100), nullable=False)
    password = db.Column(db.String(100), nullable=False)

    def __init__(self, email, password):
        self.email = email
        self.password = password

    def __repr__(self) -> str:
        return f"User : ['id'=> {self.id}, 'email' => {self.email}, 'password' => {self.password}]"
