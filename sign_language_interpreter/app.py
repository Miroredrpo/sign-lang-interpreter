from flask import Flask, render_template, request, redirect, url_for, flash
from flask_socketio import SocketIO
from werkzeug.utils import secure_filename
import os
import threading
from datetime import datetime
from tensorflow.keras.preprocessing.image import ImageDataGenerator
from sklearn.utils.class_weight import compute_class_weight
from .models import db, Image
from .utils import model_utils
import numpy as np
import cv2
import base64
from PIL import Image as PILImage
import io
import json

app = Flask(__name__)
app.config.from_object('sign_language_interpreter.config.Config')
socketio = SocketIO(app)
db.init_app(app)

with app.app_context():
    db.create_all()

# Global variables to hold the loaded model and class names
model = None
class_names = []

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in app.config['ALLOWED_EXTENSIONS']

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload', methods=['GET', 'POST'])
def upload():
    if request.method == 'POST':
        files = request.files.getlist('image')
        letter = request.form.get('letter', '').upper()

        if not files or not letter:
            flash("Please select at least one image and specify a letter.", 'warning')
            return redirect(request.url)

        uploaded_count = 0
        for file in files:
            if file and allowed_file(file.filename):
                filename = secure_filename(file.filename)
                letter_dir = os.path.join(app.root_path, 'dataset/training_images', letter)
                if not os.path.exists(letter_dir):
                    os.makedirs(letter_dir)

                file.save(os.path.join(letter_dir, filename))

                new_image = Image(filename=filename, letter=letter)
                db.session.add(new_image)
                uploaded_count += 1

        if uploaded_count > 0:
            db.session.commit()
            flash(f"Successfully uploaded {uploaded_count} images for the letter '{letter}'.", 'success')

        return redirect(url_for('upload'))

    return render_template('upload.html')

def train_model_in_background():
    with app.app_context():
        try:
            dataset_path = os.path.join(app.root_path, 'dataset/training_images')

            # Check for sufficient images and classes before proceeding
            min_images_per_class_for_split = 5
            can_split = True
            class_dirs = [d for d in os.listdir(dataset_path) if os.path.isdir(os.path.join(dataset_path, d))]

            if not class_dirs or len(class_dirs) < 2:
                print("Training aborted: Not enough classes to train. Need at least 2.")
                return

            for class_dir in class_dirs:
                class_path = os.path.join(dataset_path, class_dir)
                num_images = len([f for f in os.listdir(class_path) if os.path.isfile(os.path.join(class_path, f))])
                if num_images < min_images_per_class_for_split:
                    can_split = False
                    print(f"Warning: Class '{class_dir}' has only {num_images} images. Validation split will be disabled.")
                    break

            validation_split = 0.2 if can_split else 0.0

            datagen = ImageDataGenerator(
                rescale=1./255,
                rotation_range=40,
                width_shift_range=0.3,
                height_shift_range=0.3,
                shear_range=0.3,
                zoom_range=0.3,
                horizontal_flip=True,
                brightness_range=[0.5, 1.5],
                channel_shift_range=50.0,
                fill_mode='nearest',
                validation_split=validation_split
            )

            train_generator = datagen.flow_from_directory(
                dataset_path,
                target_size=(224, 224),
                batch_size=32,
                class_mode='categorical',
                subset='training',
                shuffle=True
            )

            validation_generator = None
            if can_split:
                validation_generator = datagen.flow_from_directory(
                    dataset_path,
                    target_size=(224, 224),
                    batch_size=32,
                    class_mode='categorical',
                    subset='validation',
                    shuffle=False
                )
                if validation_generator.n == 0:
                    validation_generator = None

            if train_generator.n == 0:
                print("Not enough images to train. Please upload more images.")
                return

            # Calculate class weights to handle data imbalance
            class_weights = compute_class_weight(
                'balanced',
                classes=np.unique(train_generator.classes),
                y=train_generator.classes
            )
            class_weights_dict = dict(enumerate(class_weights))

            num_classes = len(train_generator.class_indices)
            model = model_utils.create_model(num_classes)
            model_utils.compile_model(model)
            model_utils.train_model(model, train_generator, validation_generator, epochs=25, class_weight=class_weights_dict)

            timestamp = datetime.now().strftime("%Y%m%d-%H%M%S")
            model_name_base = f"sign_language_model_{timestamp}"
            model_filename = f"{model_name_base}.keras"
            class_indices_filename = f"{model_name_base}_classes.json"

            models_dir = os.path.join(app.root_path, 'models')
            if not os.path.exists(models_dir):
                os.makedirs(models_dir)

            # Save the model
            model_utils.save_model(model, os.path.join(models_dir, model_filename))

            # Save the class indices
            class_indices = train_generator.class_indices
            # Invert the dictionary to map index to class name
            class_names_map = {v: k for k, v in class_indices.items()}
            with open(os.path.join(models_dir, class_indices_filename), 'w') as f:
                json.dump(class_names_map, f)

            print(f"Training complete. Model saved as {model_filename}")
        except Exception as e:
            print(f"An error occurred during training: {e}")

@app.route('/training', methods=['GET', 'POST'])
def training():
    if request.method == 'POST':
        training_thread = threading.Thread(target=train_model_in_background)
        training_thread.start()
        flash("Training has started in the background. This may take several minutes.")
        return redirect(url_for('training'))

    return render_template('training.html')

@app.route('/live_recognition', methods=['GET', 'POST'])
def live_recognition():
    global model, class_names
    models_dir = os.path.join(app.root_path, 'models')
    if not os.path.exists(models_dir):
        os.makedirs(models_dir)
    models = [f for f in os.listdir(models_dir) if f.endswith('.keras')]

    if request.method == 'POST':
        selected_model_name = request.form.get('model')
        if selected_model_name:
            model_path = os.path.join(models_dir, selected_model_name)
            model_name_base = selected_model_name.replace('.keras', '')
            class_map_path = os.path.join(models_dir, f"{model_name_base}_classes.json")

            if not os.path.exists(class_map_path):
                flash(f"Error: Class mapping file not found for model '{selected_model_name}'.", 'danger')
                return redirect(url_for('live_recognition'))

            model = model_utils.load_model(model_path)
            model_utils.compile_model(model)  # Re-compile the model after loading
            with open(class_map_path, 'r') as f:
                class_names_map = json.load(f)
                # Convert keys from string back to integer and create a list of names
                class_names = [class_names_map[str(i)] for i in range(len(class_names_map))]

            flash(f"Model '{selected_model_name}' loaded successfully.", 'success')
        else:
            flash("Please select a model.", 'warning')

    return render_template('live_recognition.html', models=models)

@socketio.on('image')
def handle_image(image_data):
    if model is None:
        return

    try:
        # Decode the base64 image
        image_data_decoded = base64.b64decode(image_data.split(',')[1])
        pil_image = PILImage.open(io.BytesIO(image_data_decoded))

        # Convert to a format that OpenCV can handle
        frame = cv2.cvtColor(np.array(pil_image), cv2.COLOR_RGB2BGR)

        # Preprocess the frame for the model
        img = cv2.resize(frame, (224, 224))
        img_array = np.expand_dims(img, axis=0)
        img_array = img_array / 255.0

        # Make a prediction
        prediction = model.predict(img_array)
        predicted_class_index = np.argmax(prediction)
        predicted_letter = class_names[predicted_class_index]

        # Send the prediction back to the client
        socketio.emit('prediction_result', {'letter': predicted_letter})
    except Exception as e:
        print(f"Error processing image: {e}")

if __name__ == '__main__':
    socketio.run(app, debug=True)