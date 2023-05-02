<h1 align="center">Flask Homecloud</h1>
<p align="center">
    <img src="https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white" alt="Python">
    <img src="https://img.shields.io/badge/Flask-000000?style=for-the-badge&logo=flask&logoColor=white" alt="Flask">
    <img src="https://img.shields.io/badge/HTML5-E34F26?style=for-the-badge&logo=html5&logoColor=white" alt="HTML">
    <img src="https://img.shields.io/badge/CSS3-1572B6?style=for-the-badge&logo=css3&logoColor=white" alt="CSS">
    <img src="https://img.shields.io/badge/Bootstrap-563D7C?style=for-the-badge&logo=bootstrap&logoColor=white" alt="Boostrap">
    <img src="https://img.shields.io/badge/SQLite-07405E?style=for-the-badge&logo=sqlite&logoColor=white" alt="Sqlite">
</p>

This is a web application that allows its users to save files locally. he application is written in Flask, a Python framework used to create web applications, and uses SQLite as its database.</p>

## Features

The application allows users to upload, download, create, rename, delete, share files and folders with other users. Users can log in and create an account to save their files in the cloud. Files are saved locally, can be used on a home network.

## Usage

First you need to create a virtual environment. After that, you should:

1. Clone the repository from Github and switch to the new directory:

   ```bash
   git clone https://github.com/SSleimann/flask-homecloud.git
   cd flask-homecloud
   ```

2. Activate the virtual enviroment and install project dependencies:

   ```bash
   pip install -r requirements.txt
    ```

3. Set the environment variables:

   ```bash
   export FLASK_APP=__init__.py
   export FLASK_DEBUG=1
   ```

4. Now you can run the server:

   ```bash
   flask run
   ```

   Or to use it on the network:

   ```bash
   flask run -p 8000 -h 0.0.0.0
   ```
