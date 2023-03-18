# Start Flask:
# Import the Flask class.
from flask import Flask

# Create an instance of the Flask class. This lets Flask find app's resources (files).
app = Flask(__name__)

# Point Flask to the module with paths to the website's template files.
# This makes opening any of the website's pages in a web browser possible.
from app import routes

# Redundant if you turn on debug mode with "export FLASK_ENV=development".
# Debugging let's you make changes to the app's files without restarting the server.
# app.run(debug=True)
