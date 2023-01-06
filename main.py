import streamlit as st
import streamlit.components.v1 as components
from streamlit_image_comparison import image_comparison
from PIL import Image
import requests

from insect_api import get_insect_detections

st.header("Insect Counting and Detection Demo 🦟🟨")
st.write(
    """
    This is a demo of our API for detecting and counting insects on sticky traps, based on  state-of-the-art Deep Learning detection algorithms 🤖.
    This AI is able to detect white insects ⬜, small, and big ones. Also, the model is able to detect insects with high precision 🎯 regardless of the image resolution (it works with 
    pictures from smartphones too 📱).
    """)

image_comparison(
    img1="data/b.png",
    img2="data/c.JPG",
    label1="Original",
    label2="Processed",
    in_memory=True,
    make_responsive=True
)
# image_comparison(img1="data/a1.jpg", img2="data/a2.jpg", width=300)
st.write(' ')
st.subheader("Try it out!")
st.write("Upload your yellow sticky trap image with insects (or try a sample image):")
with open("data/sample_img.jpg", "rb") as file:
    btn = st.download_button(
        label="Download sample image",
        data=file,
        file_name="sample_img.jpg",
        mime="image/jpg"
    )

url = "http://uolabs-insects-api-loadbalancer-572497091.eu-west-1.elb.amazonaws.com/v1/auth/login"
data = {
    "clientId": st.secrets.api_credentials.clientId,
    "clientSecret": st.secrets.api_credentials.clientSecret
}
response = requests.request("POST", url, json=data)
tokens = response.json()

uploaded_file = st.file_uploader("Choose an image...")

if uploaded_file is not None:
    # src_image = load_image(uploaded_file)
    image = Image.open(uploaded_file)
    st.image(uploaded_file, caption='Input Image', use_column_width=True)

    with st.spinner('Analyzing image...'):
        response = get_insect_detections(uploaded_file.name, uploaded_file, tokens)

    st.success('Done!')

    json_response = response.json()
    original_url = json_response['images']['original']['url']
    processed_url = json_response['images']['processed']['url']

    # Metrics
    st.subheader("Results:")
    white_flies = int(json_response['count']['white'])
    small = int(json_response['count']['small'])
    big = int(json_response['count']['medium']) + int(json_response['count']['big'])

    c1, _, _ = st.columns(3)
    c1.metric(label="Total insects", value=small + big)
    c1, c2, c3 = st.columns(3)
    c1.metric(label="Whiteflies", value=white_flies)
    c2.metric(label="Small Insects", value=small)
    c3.metric(label="Big Insects", value=big)

    # st.image(result_url, caption='Analysed Image', use_column_width=True)
    image_comparison(
        img1=original_url,
        img2=processed_url,
        label1="Original",
        label2="Processed",
        in_memory=True,
        make_responsive=True
    )

for _ in range(20):
    st.write(' ')

c1, c2 = st.columns([1, 5])
c1.image('data/logo.png', width=100)
c2.write(
    """
    Find us at www.uolabs.tech!

    Contact us for more information: contact@uolabs.tech

    UoLabs Technology
    """)

