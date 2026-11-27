
import requests
import os
import requests
import streamlit as st

try:
    API_BASE_URL = st.secrets["API_BASE_URL"]
except Exception:
    API_BASE_URL = os.getenv(
        "API_BASE_URL",
        "http://127.0.0.1:8001/api/v1/documents"
    )


def upload_documents(employee_id, dependent_name, relationship, files):

    uploaded_files = [
        (
            "files",
            (file.name, file.getvalue(), file.type)
        )
        for file in files
    ]

    data = {
        "employee_id": employee_id,
        "dependent_name": dependent_name,
        "relationship": relationship
    }

    response = requests.post(
        f"{API_BASE_URL}/upload",
        data=data,
        files=uploaded_files,
        timeout=120
    )

    response.raise_for_status()
    return response.json()


def process_submission(submission_id):

    response = requests.post(
        f"{API_BASE_URL}/{submission_id}/process",
        timeout=600
    )

    response.raise_for_status()
    return response.json()

def get_submission_history():

    response = requests.get(
        f"{API_BASE_URL}/history",
        timeout=30
    )

    response.raise_for_status()
    return response.json()

def get_submission_result(submission_id):
    response = requests.get(
        f"{API_BASE_URL}/{submission_id}/result",
        timeout=60
    )
    response.raise_for_status()
    return response.json()