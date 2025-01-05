from flask import Flask, request, render_template, jsonify

import re
import pickle
import pandas as pd

app = Flask(__name__)

# Load models===========================================================================================================

sex_code_dict = {'female': -2, 'mostly_female': -1, 'unknown': 0, 'mostly_male': 1, 'male': 2}
language_code_dict = {'de': 0, 'en': 1, 'es': 2, 'fr': 3, 'gl': 4, 'it': 5, 'nl': 6, 'tr': 7}

# Load the model===========================================================================================================
with open('model.pkl', 'rb') as model_file:  # Update the path to your model file
    model = pickle.load(model_file)

@app.route('/')
def home():
    return render_template('main.html')

@app.route('/detect')
def detect():
    return render_template('detect.html')

@app.route('/predict', methods=['POST'])
def predict():
    data = request.json
    statuses = data.get('statuses')
    followers = data.get('followers')
    friends = data.get('friends')
    favourites = data.get('favourites')
    listed = data.get('listed')
    sex = data.get('sex')
    language = data.get('language')

    # Encode sex and language
    sex_code = sex_code_dict.get(sex, 0)  # Default to 'unknown' if not found
    language_code = language_code_dict.get(language, -1)  # Default to -1 if not found

    # Prepare input for the model
    input_data = [
        int(statuses), 
        int(followers), 
        int(friends), 
        int(favourites), 
        int(listed), 
        sex_code, 
        language_code
    ]

    l = [input_data]
    print(l)

    # Convert input_data to DataFrame with appropriate column names
    # input_df = pd.DataFrame([input_data], columns=['statuses', 'followers', 'friends', 'favourites', 'listed', 'sex_code', 'language_code'])

    # Make prediction using the loaded model
    prediction = model.predict(l)
    if(prediction == 0):
        prediction = "Not  a Fake account"
    else:
        prediction = "Fake account"

    return jsonify({'result': prediction, 'input': input_data})  # Convert prediction to list for JSON response

if __name__ == '__main__':
    app.run(debug=True)
