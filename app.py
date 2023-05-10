"""
This module contains the flask app that runs the web application.
The app has two routes:
    1. /: The main page of the web application.
    2. /result: The result page of the web application.
    
    The main page contains a form that allows the user to upload an image.
    The result page contains the result of the image classification.
    
    The app sends a POST request to the API with the image and receives the result.
    The result is then displayed on the result page.

    The app also saves the image to a file and displays it on the result page.
        
    The app is run by running the main.py file.
"""
import json
import base64
import os
import requests
from flask import Flask, render_template, request, redirect, url_for
import config

app = Flask(__name__)

# direct to main.html
@app.route('/')
def main():
    """Renders the main page."""
    # Remove the result.jpg file if it exists
    if os.path.exists('static/result.jpg'):
        os.remove('static/result.jpg')

    return render_template('main.html')

@app.route('/result',  methods=['GET'])
def redirect_to_main():
    """Redirects the user to the main page if user tries to access result page directly."""
    return redirect(url_for('main'))

# direct to result.html
@app.route('/result',  methods=['POST'])
def result():
    """Sends the POST request to the API and renders the result page."""
    try:
        # Get the image from the form
        image = request.files['image']
        # Convert image to base64 string
        encoded_string = base64.b64encode(image.read()).decode('utf-8')
        # Send image to api
        data = {'image': encoded_string}
        headers = {'Content-type': 'application/json'}
        response = requests.post(config.API_URL, data=json.dumps(data), headers=headers, timeout=20)
        # Get the result from api
        resp = json.loads(response.text)
        # Get the image from api and convert from base64 string to image
        img_display = base64.b64decode(resp['image'])
        # Get the mfg date from api
        mfg_date = resp['mfg_date']
        # Get the exp date from api
        exp_date = resp['expiry_date']
        # Save the image to a file
        with open("static/result.jpg", "wb") as result_file:
            result_file.write(img_display)
        # Direct to result.html
        return render_template('/result.html',mfg_date=mfg_date, exp_date=exp_date)
    except Exception as e:
        # Direct to error.html if there is an error
        return render_template('/error.html', error=e)

if __name__=='__main__':
    app.run(debug = False)
