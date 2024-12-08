import streamlit as st
import pandas as pd
import requests
import io
import random

# Set page configuration
st.set_page_config(
    page_title="Star Size Predictor 🌌",
    page_icon="✨",
)

# Background Image URLs for dynamic visuals
background_images = [
    "https://images.unsplash.com/photo-1527467779599-34448b3fa6a7?fm=jpg&q=60&w=3000&ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxzZWFyY2h8Nnx8c3RhcnMlMjBibGFja3xlbnwwfHwwfHx8MA%3D%3D",
    "https://c4.wallpaperflare.com/wallpaper/428/985/301/sea-night-stars-milky-way-wallpaper-preview.jpg","https://images.newscientist.com/wp-content/uploads/2022/10/19155951/SEI_130175152.jpg?width=1003"
]

# Select a random background image for every session
if "bg_image" not in st.session_state:
    st.session_state.bg_image = random.choice(background_images)

# Custom CSS for styling
st.markdown(
    f"""
    <style>
    .stApp {{
        background-image: url('{st.session_state.bg_image}');
        background-size: cover;
        background-position: center;
        background-attachment: fixed;
        color: white;
    }}
    .custom-header {{
        font-family: 'Arial', sans-serif;
        text-align: center;
        margin-bottom: 20px;
    }}
    .footer {{
        position: fixed;
        left: 0;
        bottom: 0;
        width: 100%;
        text-align: center;
        background: rgba(0, 0, 0, 0.7);
        color: white;
        padding: 10px;
    }}
    .instruction-box {{
        background-color: rgba(0, 0, 0, 0.6);
        padding: 15px;
        border-radius: 10px;
        color: white;
        font-size: 16px;
    }}
    </style>
    """,
    unsafe_allow_html=True,
)

# Header Section
st.markdown("<h1 class='custom-header'>✨ Star Size Predictor ✨</h1>", unsafe_allow_html=True)

# Instruction Section
st.markdown(
    """
    <div class='instruction-box'>
        <h4>How to Use:</h4>
        <ol>
            <li>Enter the number of stars to generate a dataset with brightness and size values.</li>
            <li>Click <b>Generate Dataset</b> to create star data.</li>
            <li>Once created, click <b>Predict Sizes</b> to get predictions using a Linear Regression model.</li>
            <li>Visualize the results by clicking <b>Generate Plot</b>.</li>
            <li>Download the data and plot for further exploration!</li>
        </ol>
    </div>
    """,
    unsafe_allow_html=True,
)

# API Endpoints
API_URL = "https://starsizepredictor-5.onrender.com"  # Update to your backend API URL

# Initialize Session States
if "generated_data" not in st.session_state:
    st.session_state.generated_data = None
if "predicted_data" not in st.session_state:
    st.session_state.predicted_data = None
if "plot_image" not in st.session_state:
    st.session_state.plot_image = None

# Input for the number of stars
num_stars = st.number_input("Enter the number of stars to generate:", min_value=10, value=100)

# Button: Generate Dataset
if st.button("Generate Dataset"):
    st.info("Generating dataset, please wait...")
    response = requests.post(f"{API_URL}/generate_data/", params={"num_samples": num_stars})
    if response.status_code == 200:
        st.session_state.generated_data = pd.read_csv(io.BytesIO(response.content))
        st.success("Dataset generated successfully!")
    else:
        st.error("Failed to generate dataset. Please try again.")

# Display Generated Dataset
if st.session_state.generated_data is not None:
    st.subheader("Generated Dataset")
    st.dataframe(st.session_state.generated_data)

# Button: Predict Star Sizes
if st.button("Predict Sizes") and st.session_state.generated_data is not None:
    st.info("Predicting star sizes...")
    response = requests.post(
        f"{API_URL}/predict/",
        files={"file": io.BytesIO(st.session_state.generated_data.to_csv(index=False).encode("utf-8"))},
    )
    if response.status_code == 200:
        st.session_state.predicted_data = pd.read_csv(io.BytesIO(response.content))
        st.success("Predictions generated successfully!")
    else:
        st.error("Failed to predict sizes. Please try again.")

# Display Predicted Dataset
if st.session_state.predicted_data is not None:
    st.subheader("Predicted Dataset")
    st.dataframe(st.session_state.predicted_data)

# Button: Generate Plot
if st.button("Generate Plot") and st.session_state.predicted_data is not None:
    st.info("Generating plot, please wait...")
    response = requests.post(
        f"{API_URL}/plot/",
        files={"file": io.BytesIO(st.session_state.predicted_data.to_csv(index=False).encode("utf-8"))},
    )
    if response.status_code == 200:
        st.session_state.plot_image = response.content
        st.success("Plot generated successfully!")
    else:
        st.error("Failed to generate plot. Please try again.")

# Display Plot
if st.session_state.plot_image is not None:
    st.image(st.session_state.plot_image, caption="Regression Line Plot", use_column_width=True)

# Footer Section
st.markdown(
    """
    <div class="footer">
        Developed with ❤️ by <b>Sriram Kintada</b> as part of the ML4A Programme.
    </div>
    """,
    unsafe_allow_html=True,
)
