from flask import Flask, render_template, request, redirect, url_for
from werkzeug.utils import secure_filename
import os
from models import db, Image

app = Flask(__name__)
app.config.from_object('config.Config')
db.init_app(app)

with app.app_context():
    db.create_all()

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in app.config['ALLOWED_EXTENSIONS']

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload', methods=['GET', 'POST'])
def upload():
    if request.method == 'POST':
        if 'image' not in request.files:
            return redirect(request.url)
        file = request.files['image']
        if file.filename == '':
            return redirect(request.url)
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            letter = request.form['letter'].upper()
            if letter:
                letter_dir = os.path.join(app.root_path, 'dataset/training_images', letter)
                if not os.path.exists(letter_dir):
                    os.makedirs(letter_dir)
                file.save(os.path.join(letter_dir, filename))
                new_image = Image(filename=filename, letter=letter)
                db.session.add(new_image)
                db.session.commit()
                return redirect(url_for('upload'))
    return render_template('upload.html')

@app.route('/training')
def training():
    return render_template('training.html')

@app.route('/live_recognition', methods=['GET', 'POST'])
def live_recognition():
    models_dir = os.path.join(app.root_path, 'models')
    if not os.path.exists(models_dir):
        os.makedirs(models_dir)
    models = [f for f in os.listdir(models_dir) if f.endswith('.h5')]

    if request.method == 'POST':
        selected_model = request.form.get('model')
        # Load the selected model and perform recognition
        # (recognition logic to be implemented)
        print(f"Selected model: {selected_model}")

    return render_template('live_recognition.html', models=models)

if __name__ == '__main__':
    app.run(debug=True)