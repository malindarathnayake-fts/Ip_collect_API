from flask import Flask, request, jsonify
import csv
from datetime import datetime
import os
import argparse

app = Flask(__name__)

# Define the directory where CSV files will be saved
CSV_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'ip_info_data')

# Ensure the directory exists
os.makedirs(CSV_DIR, exist_ok=True)

# Global variable for the CSV filename
csv_filename = None

@app.route('/', methods=['GET'])
def home():
    return "Data collector API is up", 200

@app.route('/ip-info', methods=['POST'])
def receive_ip_info():
    global csv_filename
    data = request.json
    
    if not data or not all(key in data for key in ['hostname', 'ip', 'subnetmask', 'gateway', 'dns']):
        return jsonify({"error": "Invalid data format"}), 400
    
    filepath = os.path.join(CSV_DIR, csv_filename)
    
    file_exists = os.path.isfile(filepath)
    
    with open(filepath, 'a', newline='') as csvfile:
        fieldnames = ['timestamp', 'hostname', 'ip', 'subnetmask', 'gateway', 'dns']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        
        if not file_exists:
            writer.writeheader()
        
        data['timestamp'] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        writer.writerow(data)
    
    return jsonify({
        "message": "Data received and appended successfully",
        "filename": csv_filename,
        "filepath": filepath
    }), 200

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="Run the IP Info API with a specific CSV filename.")
    parser.add_argument("filename", help="Name of the CSV file to use (will be created in the ip_info_data directory)")
    args = parser.parse_args()

    csv_filename = args.filename
    if not csv_filename.endswith('.csv'):
        csv_filename += '.csv'

    print(f"API is running. Data will be appended to: {os.path.join(CSV_DIR, csv_filename)}")
    app.run(host='0.0.0.0', port=8080)
