import os
import sys
import argparse
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import tensorflow as tf
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense, Dropout, BatchNormalization
from tensorflow.keras.preprocessing.image import ImageDataGenerator
from tensorflow.keras import regularizers
from sklearn.model_selection import train_test_split
import json

# Function to prepare a DataFrame from the 'crop' directory
def prepare_data(crop_dir):
    filepaths = []
    labels = []
    for class_name in os.listdir(crop_dir):
        class_dir = os.path.join(crop_dir, class_name)
        if os.path.isdir(class_dir):
            for file in os.listdir(class_dir):
                filepaths.append(os.path.join(class_dir, file))
                labels.append(class_name)
    return pd.DataFrame({"filepaths": filepaths, "labels": labels})

# Function to split data into train, validation, and test sets
def split_data(df, test_size=0.2, val_size=0.1):
    train_df, test_df = train_test_split(df, test_size=test_size, stratify=df['labels'])
    train_df, val_df = train_test_split(train_df, test_size=val_size, stratify=train_df['labels'])
    return train_df, val_df, test_df

# Function to create data generators
def create_generators(train_df, val_df, test_df, batch_size, img_size=(224, 224)):
    datagen = ImageDataGenerator(preprocessing_function=tf.keras.applications.efficientnet.preprocess_input)

    train_gen = datagen.flow_from_dataframe(
        train_df, x_col='filepaths', y_col='labels',
        target_size=img_size, class_mode='categorical', batch_size=batch_size, shuffle=True
    )
    val_gen = datagen.flow_from_dataframe(
        val_df, x_col='filepaths', y_col='labels',
        target_size=img_size, class_mode='categorical', batch_size=batch_size, shuffle=True
    )
    test_gen = datagen.flow_from_dataframe(
        test_df, x_col='filepaths', y_col='labels',
        target_size=img_size, class_mode='categorical', batch_size=batch_size, shuffle=False
    )
    return train_gen, val_gen, test_gen

# Function to build and compile the model
def build_model(num_classes, input_shape=(224, 224, 3)):
    base_model = tf.keras.applications.EfficientNetB3(include_top=False, weights='imagenet', pooling='max', input_shape=input_shape)

    model = Sequential([
        base_model,
        BatchNormalization(),
        Dense(256, kernel_regularizer=regularizers.l2(0.016), activation='relu'),
        Dropout(0.45),
        Dense(num_classes, activation='softmax')
    ])
    model.compile(optimizer=tf.keras.optimizers.Adamax(learning_rate=0.001),
                  loss='categorical_crossentropy', metrics=['accuracy'])
    return model

# Function to train the model
def train_model(model, train_gen, val_gen, epochs, callbacks):
    history = model.fit(train_gen, validation_data=val_gen, epochs=epochs, callbacks=callbacks)
    return history

# Main script
if __name__ == "__main__":
    # Check for GPU availability
    gpus = tf.config.list_physical_devices('GPU')
    if not gpus:
        print("No GPU found. Exiting.")
        sys.exit(1)
    else:
        print(f"Using GPU: {gpus[0].name}")
        tf.config.set_visible_devices(gpus[0], 'GPU')

    # Argument parsing
    parser = argparse.ArgumentParser(description="Train a military aircraft classifier using EfficientNetB3.")
    parser.add_argument("--dataset", required=True, help="Path to the 'crop' folder of the dataset.")
    parser.add_argument("--batch_size", type=int, default=32, help="Batch size for training (default: 32).")
    parser.add_argument("--epochs", type=int, default=20, help="Number of training epochs (default: 20).")
    parser.add_argument("--output", type=str, default="aircraft_classifier.keras", help="Output model filename (default: 'aircraft_classifier.keras').")
    parser.add_argument("--class_indices_output", type=str, default="class_indices.json", help="Filename to save class indices (default: 'class_indices.json').")
    args = parser.parse_args()

    # Prepare dataset
    print("Preparing data...")
    df = prepare_data(args.dataset)

    # Split data
    print("Splitting data...")
    train_df, val_df, test_df = split_data(df)

    # Create data generators
    print("Creating data generators...")
    train_gen, val_gen, test_gen = create_generators(train_df, val_df, test_df, args.batch_size)

    # Save class indices
    print("Saving class indices...")
    with open(args.class_indices_output, 'w') as f:
        json.dump(train_gen.class_indices, f)
    print(f"Class indices saved to {args.class_indices_output}.")

    # Build model
    print("Building model...")
    num_classes = len(train_gen.class_indices)
    model = build_model(num_classes)

    # Define callbacks
    callbacks = [
        tf.keras.callbacks.EarlyStopping(monitor='val_loss', patience=3),
        tf.keras.callbacks.ReduceLROnPlateau(monitor='val_loss', factor=0.5, patience=2)
    ]

    # Train model
    print("Training model...")
    history = train_model(model, train_gen, val_gen, args.epochs, callbacks)

    # Plot training history
    print("Plotting training history...")
    plt.figure(figsize=(10, 5))
    plt.plot(history.history['accuracy'], label='Training Accuracy')
    plt.plot(history.history['val_accuracy'], label='Validation Accuracy')
    plt.title('Model Accuracy')
    plt.legend()
    plt.show()

    plt.figure(figsize=(10, 5))
    plt.plot(history.history['loss'], label='Training Loss')
    plt.plot(history.history['val_loss'], label='Validation Loss')
    plt.title('Model Loss')
    plt.legend()
    plt.show()

    # Save the model
    print(f"Saving model to {args.output}...")
    model.save(args.output)
    print(f"Model saved as '{args.output}'.")
