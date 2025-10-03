import unittest
import os
import io
import sys

# Add project root to the Python path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from sign_language_interpreter.app import app, db
from sign_language_interpreter.models import Image

class AppTestCase(unittest.TestCase):
    def setUp(self):
        """Set up a test client and a temporary database."""
        app.config['TESTING'] = True
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
        app.config['WTF_CSRF_ENABLED'] = False
        self.app = app.test_client()
        with app.app_context():
            db.create_all()

    def tearDown(self):
        """Clean up the database session."""
        with app.app_context():
            db.session.remove()
            db.drop_all()

    def test_home_page(self):
        """Test that the home page loads correctly."""
        response = self.app.get('/')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Welcome to the Sign Language Interpreter', response.data)

    def test_image_upload(self):
        """Test the image upload functionality."""
        data = {
            'letter': 'A',
            'image': (io.BytesIO(b'my fake image content'), 'test.jpg')
        }
        response = self.app.post('/upload', data=data, content_type='multipart/form-data')

        # Check for a successful redirect
        self.assertEqual(response.status_code, 302)

        # Check that the image was saved to the database
        with app.app_context():
            image = Image.query.filter_by(filename='test.jpg').first()
            self.assertIsNotNone(image)
            self.assertEqual(image.letter, 'A')

    def test_training_route(self):
        """Test that the training process can be initiated."""
        response = self.app.post('/training')

        # Check for a successful redirect
        self.assertEqual(response.status_code, 302)

        # Check for the flash message indicating training has started
        with self.app.session_transaction() as session:
            self.assertIn('_flashes', session)
            self.assertIn('Training has started', session['_flashes'][0][1])

if __name__ == '__main__':
    unittest.main()