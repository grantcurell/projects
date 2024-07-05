from sklearn.feature_extraction.text import TfidfVectorizer
import matplotlib.pyplot as plt
import numpy as np

# Example documents
documents = [
    "The cat in the hat.",
    "The cat and the dog.",
    "The dog chased the cat.",
    "The dogus sat on the mat.",
    "The dog and the cat played.",
    "The cat and the mouse.",
    "The cat was hungry.",
    "The parrot slept all day.",
    "The cat and the bird.",
    "The cat is black."
]

# Initialize TfidfVectorizer
vectorizer = TfidfVectorizer()

# Calculate TF-IDF matrix
tf_idf_matrix = vectorizer.fit_transform(documents)

# Convert matrix to numpy array
tf_idf_array = tf_idf_matrix.toarray()

# Plot heatmap
fig, ax = plt.subplots()
im = ax.imshow(tf_idf_array, cmap='coolwarm')

# Add colorbar
cbar = ax.figure.colorbar(im, ax=ax)

# Set axis labels
ax.set_xticks(np.arange(len(vectorizer.get_feature_names_out())))
ax.set_yticks(np.arange(len(documents)))
ax.set_xticklabels(vectorizer.get_feature_names_out())
ax.set_yticklabels(documents)

# Rotate tick labels
plt.setp(ax.get_xticklabels(), rotation=45, ha="right",
         rotation_mode="anchor")

# Set title and show plot
ax.set_title("TF-IDF")
fig.tight_layout()
plt.show()
