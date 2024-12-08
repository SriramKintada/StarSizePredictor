from fastapi import FastAPI, File, UploadFile, Query
from fastapi.responses import StreamingResponse
from fastapi.middleware.cors import CORSMiddleware
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import io

# Initialize the FastAPI app
app = FastAPI()

# Configure CORS to allow communication with specific frontend URLs
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Change "*" to specific origins for production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Constants for the linear regression model
WEIGHT = 1.982015  # Slope of the regression line
BIAS = 9.500380    # Intercept of the regression line

@app.get("/")
def home():
    """
    Root endpoint to verify that the application is running.
    Returns:
        dict: A JSON message indicating the app status.
    """
    return {"message": "API is active"}

@app.post("/generate_data/")
async def generate_data(num_samples: int = Query(500, gt=0, description="Number of data samples to generate")):
    """
    Generates a synthetic dataset for linear regression.
    Args:
        num_samples (int): The number of data samples to generate.
    Returns:
        StreamingResponse: CSV file containing the generated dataset.
    """
    # Simulate random data for brightness (inputs) and size (targets)
    brightness = 3 * np.random.random(size=(num_samples, 1))  # Random brightness values
    noise = np.random.normal(0, 0.5, size=(num_samples, 1))  # Noise for realism
    size = BIAS + WEIGHT * brightness + noise  # Calculate size with some noise

    # Create a DataFrame to store the generated data

data = pd.DataFrame(list(zip(brightness.reshape(num_samples,), size.reshape(num_samples,))), 
                       columns=['Brightness', 'Size'])
    # Convert DataFrame to a CSV byte stream for response
    output = data.to_csv(index=False).encode('utf-8')
    return StreamingResponse(
        io.BytesIO(output),
        media_type="text/csv",
        headers={"Content-Disposition": f"attachment; filename=star_data_{num_samples}.csv"}
    )

@app.post("/predict/")
async def predict(file: UploadFile = File(...)):
    """
    Predicts star sizes based on the input brightness values.
    Args:
        file (UploadFile): A CSV file containing 'inputs' and 'targets'.
    Returns:
        StreamingResponse: CSV file with predictions added.
    """
    # Read and process the uploaded CSV file
    contents = await file.read()
    data = pd.read_csv(io.BytesIO(contents))
    data.columns = ['Brightness', 'Actual Size']  # Rename columns for clarity

    # Apply the regression formula to generate predictions
    data['Predicted Size'] = WEIGHT * data['Brightness'] + BIAS
    output = data.to_csv(index=False).encode('utf-8')

    return StreamingResponse(
        io.BytesIO(output),
        media_type="text/csv",
        headers={"Content-Disposition": "attachment; filename=predicted_sizes.csv"},
    )

@app.post("/plot/")
async def plot(file: UploadFile = File(...)):
    """
    Generates a plot showing the regression model.
    Args:
        file (UploadFile): A CSV file containing the brightness and predicted size.
    Returns:
        StreamingResponse: The plot as an image file.
    """
    # Read and process the uploaded CSV file
    contents = await file.read()
    data = pd.read_csv(io.BytesIO(contents))

    # Create the plot
    plt.figure(figsize=(8, 6))
    plt.scatter(data['Brightness'], data['Actual Size'], color='blue', label='Actual Sizes')
    plt.plot(data['Brightness'], data['Predicted Size'], color='red', label='Predicted Sizes', linewidth=2)
    plt.title("Star Size Prediction")
    plt.xlabel("Brightness")
    plt.ylabel("Size")
    plt.legend()

    # Save the plot to a BytesIO object
    buf = io.BytesIO()
    plt.savefig(buf, format="png")
    buf.seek(0)

    return StreamingResponse(buf, media_type="image/png")

