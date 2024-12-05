from app import app
from models import db, Cupcake

with app.app_context():
    db.drop_all()
    db.create_all()

cupcakes = [ 
    Cupcake(flavor="Vanilla", size="Medium", rating=4.5), 
    Cupcake(flavor="Chocolate", size="Large", rating=4.8, image="https://tinyurl.com/chocolate-cupcake"), 
    Cupcake(flavor="Strawberry", size="Small", rating=4.0, image="https://tinyurl.com/strawberry-cupcake") 
]

db.session.add_all(cupcakes)  # Corrected to pass the list of objects directly
db.session.commit()
