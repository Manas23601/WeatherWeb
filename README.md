# WeatherWeb
A flask application to check the weather in any place in the world using city name with the help of OpenWeatherMapAPI.

# Steps to Install
```bash
# Create a virtual Environment
python -m venv <environment name>
# Install requirements
pip install requirements.txt
```

# Steps to Run
```bash
# Configure environment variables
set FLASK_APP=application.py
# Run using localhost(127.0.0.1)
flask run
```
Note: if you don't have data.db file present, it will automatically create one for you.  
The database has two columns (username, hash). Username has to be unique and password's hash was stored.