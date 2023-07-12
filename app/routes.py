from flask import render_template, request, redirect, url_for, jsonify
import os
import pandas as pd
from datetime import datetime
from app import server

@server.route('/', methods=['GET'])
def index():
    # return "Hello"
    return render_template('index.html')

@server.errorhandler(404)
def invalid_route(e):
    return "missing route"

@server.route('/upload', methods=['POST'])
def upload():
    file = request.files['file']
    if file.filename == '':
        return redirect(url_for('index'))

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
    for column in df.columns:
        column_data = {
            'column_name': column,
            'data_type': str(df[column].dtype),
            'null_percentage': df[column].isnull().mean() * 100,
            'unique_percentage': df[column].nunique() / df.shape[0] * 100,
            'likely_pii': False,  # Update this based on your rule for identifying PII
            'low_cardinality': df[column].nunique() < 10,
            'boolean_data': df[column].dropna().isin([0, 1]).all(),
            'mean': df[column].mean() if df[column].dtype == 'float64' else None,
            'std': df[column].std() if df[column].dtype == 'float64' else None,
            'skewness': df[column].skew() if df[column].dtype == 'float64' else None,
            'log_transform': False  # Update this based on your statistical rule
        }
        column_summary.append(column_data)

    # Clean up the temporary file
    os.remove(temp_path)

    return render_template('summary.html', file_size=file_size, shape=shape, last_saved=last_saved, columns=column_summary)


