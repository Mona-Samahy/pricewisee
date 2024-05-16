'''
from fastapi import FastAPI, File, UploadFile
from fastapi.responses import JSONResponse
from PIL import Image
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity
import os
import tensorflow as tf
from keras._tf_keras.keras.applications import ResNet50
from keras._tf_keras.keras.applications.resnet50 import preprocess_input
import pickle

app = FastAPI()

# Load pre-trained ResNet50 model
model = ResNet50(weights="imagenet", include_top=False, pooling="avg")

# Load your dataset embeddings and filenames from pickle files
with open("embeddings.pkl", "rb") as f:
    dataset_embeddings = pickle.load(f)

with open("filenames.pkl", "rb") as f:
    dataset_image_paths = pickle.load(f)

# Define the folder where the uploaded images will be saved temporarily
upload_folder = "temp_upload"

# Create the upload folder if it doesn't exist
if not os.path.exists(upload_folder):
    os.makedirs(upload_folder)


@app.post("/upload/")
async def upload_photo(file: UploadFile = File(...), top_n: int = 5):
    # Save the uploaded file temporarily
    file_location = os.path.join(upload_folder, file.filename)
    with open(file_location, "wb") as f:
        f.write(await file.read())

    # Open the uploaded image and resize it
    img = Image.open(file_location)
    img = img.resize((224, 224))  # Resize input image to match ResNet50 input size
    img_array = np.array(img)
    img_array = preprocess_input(img_array)  # Preprocess input for ResNet50
    img_array = np.expand_dims(img_array, axis=0)  # Add batch dimension

    # Extract features (embedding) from the uploaded image
    query_embedding = model.predict(img_array)

    # Calculate cosine similarity between query image and dataset images
    similarities = cosine_similarity(query_embedding, dataset_embeddings)

    # Get indices of top N similar images
    top_n_indices = np.argsort(similarities[0])[::-1][:top_n]

    # Get IDs of top N similar images
    similar_image_ids = [dataset_image_paths[i] for i in top_n_indices]

    # Remove the temporarily saved file
    os.remove(file_location)

    # Extract only the IDs without the file extension
    similar_image_ids = [
        os.path.splitext(os.path.basename(path))[0] for path in similar_image_ids
    ]

    return JSONResponse(content={"similar_image_ids": similar_image_ids})


if __name__ == "main":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)
'''
