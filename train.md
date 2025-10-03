# Training the Sign Language Interpreter

This guide provides detailed instructions on how to set up the environment, prepare the dataset, run the application, and train the model for the Sign Language Interpreter project.

## 1. Environment Setup

Before you begin, ensure you have Python 3.x installed.

1.  **Clone the repository:**
    ```bash
    git clone <repository-url>
    cd sign_language_interpreter
    ```

2.  **Create a virtual environment (recommended):**
    ```bash
    python -m venv venv
    source venv/bin/activate  # On Windows, use `venv\Scripts\activate`
    ```

3.  **Install the dependencies:**
    All the required packages are listed in `requirements.txt`. Install them using pip:
    ```bash
    pip install -r requirements.txt
    ```

## 2. Dataset Preparation

The accuracy of the model depends on the quality and quantity of the training data. The model is trained on images of hand signs, with each letter corresponding to a specific gesture.

### Image Storage

-   The training images are stored in the `sign_language_interpreter/dataset/training_images/` directory.
-   Inside this directory, create a separate folder for each letter of the alphabet (e.g., `A`, `B`, `C`).
-   Place the corresponding images for each letter into their respective folders. For example, all images of the sign for 'A' should be in the `sign_language_interpreter/dataset/training_images/A/` folder.

### Adding New Images

You can add new images to the dataset using the web interface:

1.  Run the application (see instructions below).
2.  Navigate to the "Upload Image for Training" page.
3.  Choose an image file (`.png`, `.jpg`, or `.jpeg`).
4.  Enter the letter that the sign represents.
5.  Click "Upload."

The application will automatically save the image to the correct folder in the `dataset/training_images/` directory.

## 3. Running the Application

To run the Flask web application:

1.  Make sure you are in the `sign_language_interpreter` directory and your virtual environment is activated.
2.  Run the `app.py` script:
    ```bash
    python app.py
    ```
3.  The application will be available at `http://127.0.0.1:5000`.

## 4. Model Training

The model training process involves using the images in the `dataset/training_images/` directory to teach the neural network how to recognize sign language gestures.

**Note:** The training functionality is not yet fully integrated into the web interface. The following steps describe the intended workflow.

1.  **Initiate Training:**
    A dedicated training script or a route in the web application will be used to start the training process. This script will:
    -   Load the images from the dataset folders.
    -   Preprocess the images (resize, normalize, etc.).
    -   Use transfer learning on a pre-trained model (EfficientNetV2-B0).
    -   Train the model on the prepared dataset.

2.  **Model Saving:**
    Once the training is complete, the trained model will be saved to `sign_language_interpreter/models/trained_model.h5`. This model will then be used for real-time recognition.

## 5. Live Recognition

After a model has been trained and saved, you can use the "Live Recognition" feature to get real-time interpretations of sign language gestures from your webcam. The application will load the trained model and use it to predict the meaning of the hand signs it sees.