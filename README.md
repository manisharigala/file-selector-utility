# File Selector Utility

File Selector Utility is a web application built with Flask that allows users to upload CSV files, perform analysis on the data, and perform one-hot encoding of low-cardinality non-numeric features.

## Getting Started

To run the File Selector Utility on your local machine, follow these steps:

### Prerequisites

- Python 3.x
- Flask
- pandas

### Installation

1. Clone the repository:

git clone <repository_url>


2. Navigate to the project directory:

cd file-selector-utility


3. Install the required packages:

pip install -r requirements.txt


### Running the Application

1. Start the Flask server:

python run.py


2. Open your web browser and go to `http://localhost:8888`.

3. Use the web interface to upload and analyze CSV files.

## API Documentation

The File Selector Utility provides the following API endpoints:

### POST /upload

This endpoint handles file upload and analysis. It accepts a CSV file and performs analysis on the data, including identifying PII (Personally Identifiable Information) columns and low-cardinality features.

### POST /encode

This endpoint performs one-hot encoding of selected low-cardinality non-numeric features. It returns a preview of the encoded DataFrame.

### POST /save_encoded

This endpoint saves the encoded DataFrame as a CSV file in the `saved_files` directory.

