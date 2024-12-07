# STAR SIZE PREDICTION

This web application provides the following functionalities:

1.Allows users to create a synthetic dataset containing 'n' stars.
2.The dataset automatically includes the stars' brightness and corresponding sizes.
3.Using Artificial Intelligence (specifically linear regression), the program predicts the star sizes based on their brightness values.
4.A feature is available to generate a plot of the predictions, which helps evaluate the model's performance on the unseen data.


#### Python Libraries Used:

* streamlit
* fastapi
* uvicorn
* requests
* pandas
* numpy
* matplotlib


# Installation

This project is a Streamlit application for generating and predicting star data using a FastAPI backend.

## Prerequisites

- Python 3.7 or higher
- pip (Python package installer)

## Installation

1. **Clone the Repository**:

   Open your terminal and clone the repository:

   ```bash
   git clone https://github.com/yourusername/star-data-prediction-app.git
   cd star-data-prediction-app

2. **Install dependencies**:
   Create a virtual environment (optional but recommended) and install the required packages:

    For windows

   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows use `venv\Scripts\activate`
   pip install -r requirements.txt
   ```
    For linux or Mac
   ```bash
   python3 -m venv venv
   ```

3. Activate the virtual environment:
   
   For windows
   ```bash
   venv\Scripts\activate
   ```
   For linux or Mac
   ```bash
   source venv/bin/activate
   ```
   
5. Install the requirements:
   
   For windows
   ```bash
   python -m pip install -r requirements.txt
   ```
   For linux or Mac
   ```bash
   pip install -r requirements.txt
   ```
   
7. Run the backend powered by FastAPI using Uvicorn:
   ```bash
   uvicorn main:app
   ```

8. Run the frontend powered by Streamlit:
   ```bash
   streamlit run frontend.py
   ```



# Tools Used In This Project:
1. FastAPI - To build the API endpoints
2. Streamlit - To build and host the frontend of the web application
3. Render - To host the backend API built using FastAPI
4. NumPy - To create the synthetic dataset for training, validation, testing, and the web application
5. Matplotlib - To visualize the cost vs iterations and in the web application to visualize the regression line
6. Pandas - To read CSV files, create the dataframe, and save dataframes back to CSV

# Acknowledgements
Special thanks to the authors of the libraries used in this project.

# Contact Info
For questions or support, please reach out to kintadasrirama3637fgmail.com 


