import requests
import streamlit as st

url = "http://uolabs-insects-api-loadbalancer-572497091.eu-west-1.elb.amazonaws.com/v1/detections"


@st.cache(suppress_st_warning=True)
def get_insect_detections(filename, file, tokens):
    data = {
        "file": file,
        "model": "DL"
    }
    headers = {
        "Authorization": f"Bearer {tokens['accessToken']}"
    }
    response = requests.request("POST", url, files=data, headers=headers)
    return response
