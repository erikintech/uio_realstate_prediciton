from crypt import methods
from fileinput import filename
from flask import Flask, render_template, request, jsonify
import pandas as pd
import numpy as np
import pickle

app = Flask(__name__)
df = pd.read_csv('./data/clean_data.csv')
locations = sorted(df['location'].unique())
pipe = pickle.load( open('./model/finalModel.pkl', 'rb') )


@app.route('/', methods=['POST', 'GET'])
def index():
    return render_template('home.html', locations=locations)
 
@app.route('/predict', methods=['POST'])
def prediction():
    location = request.form.get('location')
    lot_area = request.form.get('lotarea')
    house_area = request.form.get('housearea')
    bedrooms = request.form.get('bedrooms')
    bathrooms = request.form.get('bathrooms')
    parking_spaces = request.form.get('parkingspaces')
    input_data = pd.DataFrame( [[location, lot_area, house_area, bedrooms, bathrooms, parking_spaces]],
        columns= ['location', 'lotArea', 'houseArea', 'bedroom', 'bathroom', 'parkingSpaces'] )
    prediction = pipe.predict(input_data)[0]

    return str( np.round(prediction, 2) )

@app.route('/predict/api', methods=['POST'])
def house_api():
    location = request.json['location']
    lot_area = request.json['lotArea']
    house_area = request.json['houseArea']
    bedrooms = request.json['bedroom']
    bathrooms = request.json['bathroom']
    parking_spaces = request.json['parkingspaces']
    input_data = pd.DataFrame( [[location, lot_area, house_area, bedrooms, bathrooms, parking_spaces]],
        columns= ['location', 'lotArea', 'houseArea', 'bedroom', 'bathroom', 'parkingSpaces'] )
    prediction = pipe.predict(input_data)[0]
    
    print(request.json['location'])
    
    return jsonify({'Estimate Price': f'US$ {round(prediction, 2)}'})

if __name__ == '__main__':
    app.run()