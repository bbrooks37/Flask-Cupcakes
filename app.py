from flask import Flask, jsonify, request, render_template
from flask_cors import CORS
from models import db, connect_db, Cupcake
from flask_wtf import FlaskForm
from wtforms import StringField, FloatField, SubmitField
from wtforms.validators import DataRequired, URL

app = Flask(__name__)
CORS(app)  # Enable CORS

# Configuration
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://bbswag:Planthigh37$$@localhost:5432/cupcakes'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = 'your-secret-key'  # Required for WTForms

# Connect the database
connect_db(app)

# Ensure the app context is active
with app.app_context():
    db.create_all()

# Forms
class CupcakeForm(FlaskForm):
    flavor = StringField('Flavor', validators=[DataRequired()])
    size = StringField('Size', validators=[DataRequired()])
    rating = FloatField('Rating', validators=[DataRequired()])
    image = StringField('Image URL', validators=[URL(), DataRequired()])
    submit = SubmitField('Add Cupcake')

# Routes
@app.route('/')
def index():
    form = CupcakeForm()
    return render_template('index.html', form=form)

@app.route('/api/cupcakes', methods=['GET'])
def get_cupcakes():
    """Get all cupcakes."""
    cupcakes = Cupcake.query.all()
    cupcakes_list = [cupcake.to_dict() for cupcake in cupcakes]
    return jsonify(cupcakes=cupcakes_list)

@app.route('/api/cupcakes/<int:cupcake_id>', methods=['GET'])
def get_cupcake(cupcake_id):
    """Get a single cupcake by ID."""
    cupcake = Cupcake.query.get_or_404(cupcake_id)
    return jsonify(cupcake=cupcake.to_dict())

@app.route('/api/cupcakes', methods=['POST'])
def create_cupcake():
    """Create a new cupcake."""
    try:
        data = request.json
        print(f"Received data: {data}")  # Debugging line
        new_cupcake = Cupcake(
            flavor=data['flavor'],
            size=data['size'],
            rating=data['rating'],
            image=data.get('image', 'https://tinyurl.com/demo-cupcake')
        )
        db.session.add(new_cupcake)
        db.session.commit()
        return jsonify(cupcake=new_cupcake.to_dict()), 201
    except KeyError as e:
        print(f"Missing field: {e.args[0]}")  # Detailed error message
        return jsonify(error=f"Missing required field: {e.args[0]}"), 400
    except Exception as e:
        print(f"Error creating cupcake: {e}")  # General error logging
        return jsonify(error="An error occurred while creating the cupcake"), 500

@app.route('/api/cupcakes/<int:cupcake_id>', methods=['PATCH'])
def update_cupcake(cupcake_id):
    """Update an existing cupcake."""
    cupcake = Cupcake.query.get_or_404(cupcake_id)
    data = request.json
    cupcake.flavor = data.get('flavor', cupcake.flavor)
    cupcake.size = data.get('size', cupcake.size)
    cupcake.rating = data.get('rating', cupcake.rating)
    cupcake.image = data.get('image', cupcake.image)
    db.session.commit()
    return jsonify(cupcake=cupcake.to_dict())

@app.route('/api/cupcakes/<int:cupcake_id>', methods=['DELETE'])
def delete_cupcake(cupcake_id):
    """Delete a cupcake by ID."""
    cupcake = Cupcake.query.get_or_404(cupcake_id)
    db.session.delete(cupcake)
    db.session.commit()
    return jsonify(message="Cupcake deleted")

@app.route('/api/cupcakes/search', methods=['GET'])
def search_cupcakes():
    search_term = request.args.get('q', '')
    cupcakes = Cupcake.query.filter(Cupcake.flavor.ilike(f'%{search_term}%')).all()
    cupcakes_list = [cupcake.to_dict() for cupcake in cupcakes]
    return jsonify(cupcakes=cupcakes_list)

if __name__ == '__main__':
    app.run(debug=True)