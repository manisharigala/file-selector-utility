from flask import render_template, request, redirect, url_for
import os
import pandas as pd
from datetime import datetime
from app import server, pii_helper as pii
import re

# Store the dataframe as a global variable
df = None

@server.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        return render_template('index.html', success_message='CSV file saved successfully.')
    return render_template('index.html')

@server.errorhandler(404)
def invalid_route(e):
    return "Page not found"

@server.route('/upload', methods=['POST'])
def upload():
    global df
    file = request.files['file']
    if file.filename == '':
        return redirect(url_for('index'))
    
    # Check if the file has a CSV format
    if not file.filename.lower().endswith('.csv'):
        return render_template('index.html', error_message='Please upload a file with a CSV format.')

    # Save the uploaded file to a temporary location
    temp_path = f'temp/{file.filename}'
    file.save(temp_path)

    # Perform analysis on the CSV file
    df = pd.read_csv(temp_path)
    file_size = os.path.getsize(temp_path) / (1024 * 1024)
    shape = df.shape
    last_saved = datetime.fromtimestamp(os.path.getmtime(temp_path))

    # Prepare column summary data
    column_summary = []
    low_cardinality_features = []
    for column in df.columns:
        column_data = {
            'column_name': column,
            'data_type': str(df[column].dtype),
            'null_percentage': df[column].isnull().mean() * 100,
            'unique_percentage': df[column].nunique() / df.shape[0] * 100,
            'likely_pii': any(pattern in column.lower() for pattern in pii.pii_keywords) or any(pii.check_for_pii(str(value)) for value in df[column]),
            'low_cardinality': df[column].nunique() < 10,
            'boolean_data': df[column].dropna().isin([0, 1]).all(),
            'mean': df[column].mean() if df[column].dtype == 'float64' else None,
            'std': df[column].std() if df[column].dtype == 'float64' else None,
            'skewness': df[column].skew() if df[column].dtype == 'float64' else None,
        }
        column_summary.append(column_data)
        if column_data['low_cardinality'] and column_data['data_type'] == 'object' and not column_data['likely_pii']:
            low_cardinality_features.append(column)

    # Clean up the temporary file
    os.remove(temp_path)

    return render_template('summary.html', file_size=file_size, shape=shape, last_saved=last_saved, columns=column_summary, df=df, min=min)

@server.route('/encode', methods=['POST'])
def encode():
    selected_features = request.form.getlist('feature')

    # Perform one-hot encoding and create a copy of the DataFrame
    encoded_df = df.copy()
    encoded_df = pd.get_dummies(encoded_df, columns=selected_features)

    # Get the top 10 rows of the encoded DataFrame
    encoded_preview = encoded_df.head(10)

    return render_template('encode.html', encoded_preview=encoded_preview)

@server.route('/save_encoded', methods=['POST'])
def save_encoded():
    encoded_data = request.form['encoded_data']

    # Create the 'saved_files' directory if it doesn't exist
    os.makedirs('saved_files', exist_ok=True)

    # Save the encoded DataFrame as a CSV file
    encoded_file_path = f'saved_files/{datetime.now().strftime("%Y%m%d%H%M%S")}_encoded.csv'
    with open(encoded_file_path, 'w') as file:
        file.write(encoded_data)

    # Set the success message
    success_message = 'Encoded DataFrame saved successfully.'

    return render_template('index.html', success_message=success_message)


# Custom filter to calculate the minimum value
@server.template_filter('min')
def min_filter(column):
    return column.min()