"""Models for Cupcake app."""

from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

DEFAULT_IMAGE = "https://tinyurl.com/demo-cupcake"

class Ingredient(db.Model):
    __tablename__ = "ingredients"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.Text, nullable=False)
    
    def __repr__(self): return f"<Ingredient id={self.id} name={self.name}>"
    
class CupcakeIngredient(db.Model):
    __tablename__ = "cupcake_ingredients"
    cupcake_id = db.Column(db.Integer, db.ForeignKey('cupcakes.id'), primary_key=True)
    ingredient_id = db.Column(db.Integer, db.ForeignKey('ingredients.id'), primary_key=True)
    

class Cupcake(db.Model):
    """Model for a Cupcake."""
    
    __tablename__ = "cupcakes"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    flavor = db.Column(db.Text, nullable=False)
    size = db.Column(db.Text, nullable=False)
    rating = db.Column(db.Float, nullable=False)
    image = db.Column(db.Text, nullable=False, default=DEFAULT_IMAGE)

    def __repr__(self):
        return f"<Cupcake id={self.id} flavor={self.flavor} rating={self.rating}>"

    def to_dict(self):
        """Serialize cupcake to a dict of cupcake info."""
        return {
            "id": self.id,
            "flavor": self.flavor,
            "rating": self.rating,
            "size": self.size,
            "image": self.image,
        }

def connect_db(app):
    """Connect to database."""
    db.app = app
    db.init_app(app)
