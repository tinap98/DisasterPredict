import joblib
import numpy as np
from pathlib import Path
from flask import jsonify

# Define paths to model files
MODEL_DIR = Path(__file__).parent
MODEL_PATH = MODEL_DIR / 'random_forest_model.joblib'
SCALER_PATH = MODEL_DIR / 'scaler.joblib'

# Load models at module level
try:
    model = joblib.load(MODEL_PATH)
    scaler = joblib.load(SCALER_PATH)
except Exception as e:
    raise RuntimeError(f"Failed to load model files: {str(e)}")

MAGNITUDE_SCALE_MAPPING = {
    0: "Km²",
    1: "Richter Scale", 
    2: "Wind Speed (km/h)",
    3: "Water Level (m)",
    4: "Temperature (°C)",
    5: "Rainfall (mm)"
}

# Mappings (unchanged from your version)
DISASTER_MAPPING = {
    0: "Other", 1: "Drought", 2: "Earthquake", 3: "Epidemic",
    4: "Extreme temperature", 5: "Flood", 6: "Fog",
    7: "Glacial lake outburst", 8: "Impact", 9: "Insect infestation",
    10: "Landslide", 11: "Mass movement (dry)", 12: "Storm",
    13: "Volcanic activity", 14: "Wildfire"
}

COUNTRY_MAPPING = {
    0: 'Afghanistan', 1: 'Albania', 2: 'Algeria', 3: 'American Samoa', 4: 'Angola', 5: 'Anguilla', 6: 'Antigua and Barbuda', 7: 'Argentina', 
    8: 'Armenia', 9: 'Australia', 10: 'Austria', 11: 'Azerbaijan', 12: 'Azores Islands', 13: 'Bahamas (the)', 14: 'Bahrain', 15: 'Bangladesh', 
    16: 'Barbados', 17: 'Belarus', 18: 'Belgium', 19: 'Belize', 20: 'Benin', 21: 'Bermuda', 22: 'Bhutan', 23: 'Bolivia (Plurinational State of)',
    24: 'Bosnia and Herzegovina', 25: 'Botswana', 26: 'Brazil', 27: 'Brunei Darussalam', 28: 'Bulgaria', 29: 'Burkina Faso', 30: 'Burundi', 
    31: 'Cabo Verde', 32: 'Cambodia', 33: 'Cameroon', 34: 'Canada', 35: 'Canary Is', 36: 'Cayman Islands (the)', 37: 'Central African Republic', 
    38: 'Chad', 39: 'Chile', 40: 'China', 41: 'Colombia', 42: 'Comoros (the)', 43: 'Congo (the Democratic Republic of the)', 44: 'Congo (the)', 
    45: 'Cook Islands (the)', 46: 'Costa Rica', 47: 'Croatia', 48: 'Cuba', 49: 'Cyprus', 50: 'Czech Republic (the)', 51: 'Czechoslovakia', 
    52: "Côte d'Ivoire", 53: 'Denmark', 54: 'Djibouti', 55: 'Dominica', 56: 'Dominican Republic (the)', 57: 'Ecuador', 58: 'Egypt', 59: 'El Salvador',
    60: 'Equatorial Guinea', 61: 'Eritrea', 62: 'Estonia', 63: 'Ethiopia', 64: 'Fiji', 65: 'Finland', 66: 'France', 67: 'French Guiana', 
    68: 'French Polynesia', 69: 'Gabon', 70: 'Gambia (the)', 71: 'Georgia', 72: 'Germany', 73: 'Germany Dem Rep', 74: 'Germany Fed Rep', 
    75: 'Ghana', 76: 'Greece', 77: 'Grenada', 78: 'Guadeloupe', 79: 'Guam', 80: 'Guatemala', 81: 'Guinea', 82: 'Guinea-Bissau', 83: 'Guyana', 
    84: 'Haiti', 85: 'Honduras', 86: 'Hong Kong', 87: 'Hungary', 88: 'Iceland', 89: 'India', 90: 'Indonesia', 91: 'Iran (Islamic Republic of)', 
    92: 'Iraq', 93: 'Ireland', 94: 'Isle of Man', 95: 'Israel', 96: 'Italy', 97: 'Jamaica', 98: 'Japan', 99: 'Jordan', 100: 'Kazakhstan',
    101: 'Kenya', 102: 'Kiribati', 103: "Korea (the Democratic People's Republic of)", 104: 'Korea (the Republic of)', 105: 'Kuwait', 106: 'Kyrgyzstan',
    107: "Lao People's Democratic Republic (the)", 108: 'Latvia', 109: 'Lebanon', 110: 'Lesotho', 111: 'Liberia', 112: 'Libya', 113: 'Lithuania',
    114: 'Luxembourg', 115: 'Macao', 116: 'Macedonia (the former Yugoslav Republic of)', 117: 'Madagascar', 118: 'Malawi', 119: 'Malaysia', 
    120: 'Maldives', 121: 'Mali', 122: 'Marshall Islands (the)', 123: 'Martinique', 124: 'Mauritania', 125: 'Mauritius', 126: 'Mexico', 
    127: 'Micronesia (Federated States of)', 128: 'Moldova (the Republic of)', 129: 'Mongolia', 130: 'Montenegro', 131: 'Montserrat', 132: 'Morocco', 
    133: 'Mozambique', 134: 'Myanmar', 135: 'Namibia', 136: 'Nepal', 137: 'Netherlands (the)', 138: 'Netherlands Antilles', 139: 'New Caledonia',
    140: 'New Zealand', 141: 'Nicaragua', 142: 'Niger (the)', 143: 'Nigeria', 144: 'Niue', 145: 'Northern Mariana Islands (the)', 146: 'Norway',
    147: 'Oman', 148: 'Pakistan', 149: 'Palau', 150: 'Palestine, State of', 151: 'Panama', 152: 'Papua New Guinea', 153: 'Paraguay', 154: 'Peru', 
    155: 'Philippines (the)', 156: 'Poland', 157: 'Portugal', 158: 'Puerto Rico', 159: 'Qatar', 160: 'Romania', 161: 'Russian Federation (the)', 
    162: 'Rwanda', 163: 'Réunion', 164: 'Saint Barthélemy', 165: 'Saint Helena, Ascension and Tristan da Cunha', 166: 'Saint Kitts and Nevis', 
    167: 'Saint Lucia', 168: 'Saint Martin (French Part)', 169: 'Saint Vincent and the Grenadines', 170: 'Samoa', 171: 'Sao Tome and Principe', 
    172: 'Saudi Arabia', 173: 'Senegal', 174: 'Serbia', 175: 'Serbia Montenegro', 176: 'Seychelles', 177: 'Sierra Leone', 178: 'Singapore', 
    179: 'Sint Maarten (Dutch part)', 180: 'Slovakia', 181: 'Slovenia', 182: 'Solomon Islands', 183: 'Somalia', 184: 'South Africa', 
    185: 'South Sudan', 186: 'Soviet Union', 187: 'Spain', 188: 'Sri Lanka', 189: 'Sudan (the)', 190: 'Suriname', 191: 'Swaziland',
    192: 'Sweden', 193: 'Switzerland', 194: 'Syrian Arab Republic', 195: 'Taiwan (Province of China)', 196: 'Tajikistan', 
    197: 'Tanzania, United Republic of', 198: 'Thailand', 199: 'Timor-Leste', 200: 'Togo', 201: 'Tokelau', 202: 'Tonga', 
    203: 'Trinidad and Tobago', 204: 'Tunisia', 205: 'Turkey', 206: 'Turkmenistan', 207: 'Turks and Caicos Islands (the)', 
    208: 'Tuvalu', 209: 'Uganda', 210: 'Ukraine', 211: 'United Arab Emirates (the)', 212: 'United Kingdom of Great Britain and Northern Ireland (the)', 
    213: 'United States of America (the)', 214: 'Uruguay', 215: 'Uzbekistan', 216: 'Vanuatu', 217: 'Venezuela (Bolivarian Republic of)', 
    218: 'Viet Nam', 219: 'Virgin Island (British)', 220: 'Virgin Island (U.S.)', 221: 'Wallis and Futuna', 222: 'Yemen', 223: 'Yemen Arab Rep', 
    224: 'Yemen P Dem Rep', 225: 'Yugoslavia', 226: 'Zambia', 227: 'Zimbabwe'
}

def predict_disaster(request):
    """Handle prediction request"""
    data = request.get_json()
    
    if not data:
        response = jsonify({'success': False, 'error': 'No data provided'})
        return response, 400
    
    try:
        required_fields = [
            'year', 'mag_scale_index', 'dis_mag_value',
            'country_code_index', 'longitude', 'latitude'
        ]
        
        if not all(field in data for field in required_fields):
            response = jsonify({
                'success': False,
                'error': f'Missing required fields. Required: {required_fields}'
            })
            return response, 400

        # Prepare and predict
        features = np.array([[
            data['year'],
            data['mag_scale_index'],
            data['dis_mag_value'],
            data['country_code_index'],
            data['longitude'],
            data['latitude']
        ]])
        features_scaled = scaler.transform(features)
        prediction = model.predict(features_scaled)[0]
        
        response = jsonify({
            'success': True,
            'disaster_name': DISASTER_MAPPING.get(int(prediction), "Unknown"),
            'magnitude_scale': MAGNITUDE_SCALE_MAPPING.get(data['mag_scale_index'], "Unknown"),
            'magnitude_value': data['dis_mag_value'],
            'country_name': COUNTRY_MAPPING.get(data['country_code_index'], "Unknown"),
            'original_data': {  # Include original values for debugging
                'predicted_label': int(prediction),
                'mag_scale_index': data['mag_scale_index'],
                'country_code_index': data['country_code_index']
            }
        })
        return response

    except Exception as e:
        response = jsonify({
            'success': False,
            'error': str(e)
        })
        return response, 500