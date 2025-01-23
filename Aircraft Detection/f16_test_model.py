import os
import json
import numpy as np
import tensorflow as tf
from tensorflow.keras.preprocessing.image import load_img, img_to_array
from tensorflow.keras.applications.efficientnet import preprocess_input

# Path to the saved model, class indices, and F-16 image folder
MODEL_PATH = "aircraft_classifier.keras"  # Replace with your actual model file
CLASS_INDICES_PATH = "class_indices.json"  # Path to saved class indices
IMAGE_FOLDER = "/media/grant/OS/Documents and Settings/grant/Documents/code/dell/Aircraft Detection/data_set/f16"  # Replace with your folder

# Parameters
IMG_SIZE = (224, 224)  # Input size for the model

# Load the trained model
print("Loading model...")
model = tf.keras.models.load_model(MODEL_PATH)

# Load class indices
print("Loading class indices...")
if os.path.exists(CLASS_INDICES_PATH):
    with open(CLASS_INDICES_PATH, "r") as file:
        class_indices = json.load(file)
    # Reverse the mapping: {index: label}
    class_indices = {v: k for k, v in class_indices.items()}
else:
    raise FileNotFoundError(f"Class indices file not found at {CLASS_INDICES_PATH}!")

# Function to preprocess a single image
def preprocess_image(image_path):
    img = load_img(image_path, target_size=IMG_SIZE)  # Resize the image
    img_array = img_to_array(img)  # Convert to array
    img_array = preprocess_input(img_array)  # Preprocess for EfficientNet
    return np.expand_dims(img_array, axis=0)  # Add batch dimension

# Iterate over images in the folder and make predictions
print("Processing images...")
correct_predictions = 0
total_images = 0

for filename in os.listdir(IMAGE_FOLDER):
    if filename.lower().endswith(('.jpg', '.jpeg', '.png', '.bmp', '.webp')):
        total_images += 1
        image_path = os.path.join(IMAGE_FOLDER, filename)
        img = preprocess_image(image_path)

        # Predict
        prediction = model.predict(img, verbose=0)
        predicted_class = np.argmax(prediction)  # Get the index of the highest probability
        confidence = prediction[0][predicted_class]

        # Handle unknown classes
        predicted_label = class_indices.get(predicted_class, "Unknown")

        # Check if it's an F-16
        is_correct = "Yes" if predicted_label == "F16" else "No"
        if is_correct == "Yes":
            correct_predictions += 1

        # Print prediction details
        print(f"Image: {filename} | Predicted: {predicted_label} | Confidence: {confidence:.2f} | Correct: {is_correct}")

# Calculate and display accuracy
accuracy = (correct_predictions / total_images) * 100 if total_images > 0 else 0
print(f"\nTotal Images: {total_images}, Correctly Identified F-16s: {correct_predictions}, Accuracy: {accuracy:.2f}%")
