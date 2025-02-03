import os
import zipfile
import requests

SPRING_INITIALIZR_URL = "https://start.spring.io/starter.zip"


def download(params, output_dir=None):
    """Download and extract the Spring Boot project."""
    if output_dir is None:
        output_dir = os.getcwd()

    response = requests.get(SPRING_INITIALIZR_URL, params=params, stream=True)

    if response.status_code == 200:
        zip_file_path = os.path.join(output_dir, f"{params['artifactId']}.zip")
        with open(zip_file_path, "wb") as zip_file:
            zip_file.write(response.content)

        # Extract ZIP file
        with zipfile.ZipFile(zip_file_path, "r") as zip_ref:
            extract_dir = os.path.join(output_dir, params["artifactId"])
            zip_ref.extractall(extract_dir)

        # Delete the zip file
        os.remove(zip_file_path)

        return extract_dir
    else:
        response.raise_for_status()
