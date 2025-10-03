# Sign Language Interpreter

A real-time sign language interpreter using Python, Flask, and TensorFlow. This application recognizes hand gestures from a webcam and translates them into text.

## Current Status

-   **Project Structure:** The application is set up with a standard Flask project structure.
-   **Image Upload:** Users can upload training images for different letters. These images are stored in a dedicated `dataset` folder, organized by letter.
-   **Database:** A SQLite database is implemented to track all uploaded training images.
-   **Model Training:** The project includes a basic framework for training a model using the uploaded images. Trained models are saved and can be loaded for recognition.
-   **Live Recognition:** A placeholder page for live recognition via webcam is in place.

## Technical Stack

-   **Backend:** Python, Flask, SQLAlchemy
-   **Machine Learning:** TensorFlow/Keras
-   **Image Processing:** OpenCV, Pillow
-   **Frontend:** HTML, CSS, JavaScript

## Getting Started

For detailed instructions on setup, training, and running the application, please see **`train.md`**.