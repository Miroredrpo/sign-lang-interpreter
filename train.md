# Training and Using the Sign Language Interpreter

This guide provides detailed instructions on how to set up the environment, prepare the dataset, run the application, train a model, and use the live recognition feature.

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
-   Place the corresponding images for each letter into their respective folders.

### Adding New Images

You can add new images to the dataset using the web interface:

1.  Run the application (see instructions below).
2.  Navigate to the **Upload** page.
3.  Choose an image file (`.png`, `.jpg`, or `.jpeg`).
4.  Enter the letter that the sign represents.
5.  Click "Upload."

The application will automatically save the image to the correct folder.

## 3. Running the Application

To run the Flask web application:

1.  Make sure you are in the project's **root directory** (the one containing `run.py`) and that your virtual environment is activated.
2.  Run the `run.py` script:
    ```bash
    python run.py
    ```
3.  The application will be available at `http://127.0.0.1:5000`.

## 4. Model Training

The model training process is initiated directly from the web interface.

1.  Navigate to the **Train** page.
2.  Click the **"Start Training"** button.
3.  The training process will start in the background. This may take several minutes, but the web application will remain responsive.
4.  Once training is complete, the new model will be saved in the `sign_language_interpreter/models/` directory with a unique, timestamped name (e.g., `sign_language_model_20231027-143000.h5`).

## 5. Live Recognition

After a model has been trained and saved, you can use the **Live Recognition** feature.

1.  Navigate to the **Live Recognition** page.
2.  Select a trained model from the dropdown menu.
3.  Click **"Load Model"**.
4.  Once the model is loaded, the application will begin processing your webcam feed and displaying the predicted letter in real-time.