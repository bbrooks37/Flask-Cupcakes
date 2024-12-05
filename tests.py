import unittest
from app import app
from models import db, Cupcake

class CupcakeTestCase(unittest.TestCase):
    def setUp(self):
        self.client = app.test_client()
        app.config['TESTING'] = True

        # Use an in-memory SQLite database
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
        app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

        with app.app_context():
            db.create_all()

    def tearDown(self):
        with app.app_context():
            db.drop_all()

    def test_get_nonexistent_cupcake(self):
        response = self.client.get('/api/cupcakes/999')
        self.assertEqual(response.status_code, 404)

    def test_patch_nonexistent_cupcake(self):
        response = self.client.patch('/api/cupcakes/999', json={})
        self.assertEqual(response.status_code, 404)

    def test_delete_nonexistent_cupcake(self):
        response = self.client.delete('/api/cupcakes/999')
        self.assertEqual(response.status_code, 404)

if __name__ == '__main__':
    unittest.main()
