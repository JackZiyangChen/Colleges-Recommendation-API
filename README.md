# College Information API

## Project Description
Some description will go here.

## Architecture Overview
This project is divided into two separate section: one being the web app itself contained under "app" package, the other being a series of web scraper stored under the "scraper" folder. For the web app, flask framework was used to link together the database, the ML recommendation models, and the API. The API itself was constructed using the flask_restful library which was directly integrated into the flask's blueprint system. 

## Running the project
To run the project locally, feel free to use a local git terminal to download the project. To configure the project, please run "setup.py" and follow the instructions of localhost in your terminal. Alternatively, after configuring appropriate environment variables, the project can also be ran using the command "flask run" at the root directory of the project.

For security reasons, I chose to exclude the .env file in my commit. Please reconfigure the project yourself with the following parameters:
* SECRET_KEY
* LOCAL_DB_URL
* FLASK_APP=setup.py
* DEBUG

## Prerequisites
Before you begin, ensure you have met the following requirements:
* You have Python 3 installed
* All packages listed under the requirements.txt has been installed. To install a specific package, run "pip install {package name}" in your terminal.

## SQL Database
Databse is handled through PostgreSQL database, powered by Heroku and AWS. 

## Contacts
If you have any questions regarding the project, you can reach out to me via the email listed on this github



















