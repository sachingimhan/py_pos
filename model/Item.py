from application import db
from dataclasses import dataclass


@dataclass
class Item(db.Model):

    id: int
    description: str
    unit_price: float
    qty: int

    id = db.Column(db.Integer, primary_key=True)
    description = db.Column(db.String(50), nullable=False)
    unit_price = db.Column(db.Float, nullable=False)
    qty = db.Column(db.Integer, nullable=False)

    def __init__(self, id, description, unit_price, qty) -> None:
        super().__init__()
        self.id = id
        self.description = description
        self.unit_price = unit_price
        self.qty = qty

    def __repr__(self) -> str:
        return f"Item : ['id'=> {self.id}, 'description' => {self.description}, 'unit_price' => {self.unit_price}, 'qty' => {self.qty} ]"
