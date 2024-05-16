import os
import numpy as np
import pandas as pd
import pickle
import tensorflow
from tensorflow.keras.preprocessing import image
from tensorflow.keras.layers import GlobalMaxPooling2D
from tensorflow.keras.applications.resnet50 import ResNet50, preprocess_input
from sklearn.neighbors import NearestNeighbors
from numpy.linalg import norm
from tqdm import tqdm
from PIL import Image
from sklearn.neighbors import NearestNeighbors

# TRAIN PART
model = ResNet50(weights="imagenet", include_top=False, input_shape=(256, 256, 3))
model.trainable = False

model = tensorflow.keras.Sequential([model, GlobalMaxPooling2D()])

# print(model.summary())


def extract_features(img_path, model):
    img = image.load_img(img_path, target_size=(256, 256))
    img_array = image.img_to_array(img)
    expanded_img_array = np.expand_dims(img_array, axis=0)
    preprocessed_img = preprocess_input(expanded_img_array)
    result = model.predict(preprocessed_img).flatten()
    normalized_result = result / norm(result)

    return normalized_result


filenames = []

for file in os.listdir("/kaggle/input/fashiondatasetgrad/images"):
    filenames.append(file)

print("DAne")
feature_list = []
path = "/kaggle/input/fashiondatasetgrad/images/"
for file in tqdm(filenames):
    feature_list.append(extract_features(path + file, model))

pickle.dump(feature_list, open("embeddings.pkl", "wb"))
pickle.dump(filenames, open("filenames.pkl", "wb"))


# TEST PART
# Assuming feature_list and filenames are already defined
neighbors = NearestNeighbors(n_neighbors=6, algorithm="brute", metric="euclidean")
neighbors.fit(feature_list)


# Function to find similar images to a query image based on photo ID
def find_similar_images(photo_id, feature_list, filenames, model, neighbors):
    # Find the index of the filename corresponding to the given photo ID
    idx = filenames.index(str(photo_id) + ".jpg")
    if idx == -1:
        print("Photo ID not found.")
        return

    # Extract features of the query image
    query_features = feature_list[idx]

    # Find nearest neighbors to the query image
    distances, indices = neighbors.kneighbors([query_features])

    # Display similar images along with their IDs
    print("Similar images to Photo ID {}: ".format(photo_id))
    for idx in indices[0]:
        img = Image.open("/kaggle/input/fashiondatasetgrad/images/" + filenames[idx])
        print("Photo ID:", filenames[idx].split(".")[0])
        display(img)


# Example usage:
# Assuming 'photo_id' is the ID of the photo you want to use as the query image
photo_id = 27  # Change this to the desired photo ID
find_similar_images(photo_id, feature_list, filenames, model, neighbors)
