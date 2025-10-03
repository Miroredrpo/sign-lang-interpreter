import tensorflow as tf
from tensorflow.keras.applications import EfficientNetV2B0
from tensorflow.keras.layers import Dense, GlobalAveragePooling2D
from tensorflow.keras.models import Model

def create_model(num_classes):
    """
    Creates a model for sign language classification using EfficientNetV2-B0 as a base.
    """
    base_model = EfficientNetV2B0(weights='imagenet', include_top=False, input_shape=(224, 224, 3))
    base_model.trainable = False  # Freeze the base model

    x = base_model.output
    x = GlobalAveragePooling2D()(x)
    x = Dense(1024, activation='relu')(x)
    predictions = Dense(num_classes, activation='softmax')(x)

    model = Model(inputs=base_model.input, outputs=predictions)
    return model

def compile_model(model):
    """
    Compiles the model.
    """
    model.compile(optimizer='adam',
                  loss='categorical_crossentropy',
                  metrics=['accuracy'])

def train_model(model, train_data, val_data, epochs=10, class_weight=None):
    """
    Trains the model.
    """
    history = model.fit(train_data,
                        epochs=epochs,
                        validation_data=val_data,
                        class_weight=class_weight)
    return history

def save_model(model, filepath):
    """
    Saves the model to a file.
    """
    model.save(filepath)

def load_model(filepath):
    """
    Loads a model from a file.
    """
    return tf.keras.models.load_model(filepath)