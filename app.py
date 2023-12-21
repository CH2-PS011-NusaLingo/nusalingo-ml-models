from flask import Flask, request, jsonify
from google.cloud import storage
import os

import sys
sys.path.append('Sunda/')
from sunda import predict_output_sunda

app = Flask(__name__)

def download_wav_from_gcs(bucket_name, filename, destination_folder):
    """
    Download a .wav file from Google Cloud Storage and save it to a local folder.

    :param bucket_name: Name of the GCS bucket.
    :param filename: Name of the .wav file in the GCS bucket.
    :param destination_folder: Local folder to save the downloaded .wav file.
    """
    # Set Google Cloud Storage credentials (replace 'path/to/your/keyfile.json' with your actual key file path)
    os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "key.json"

    # Create a GCS client
    client = storage.Client()

    # Get the GCS bucket and file
    bucket = client.get_bucket(bucket_name)
    blob = bucket.blob(filename)

    # Create the destination folder if it doesn't exist
    os.makedirs(destination_folder, exist_ok=True)

    # Specify the local file path to save the downloaded .wav file
    local_file_path = os.path.join(destination_folder, filename)

    # Download the file from GCS to the local folder
    blob.download_to_filename(local_file_path)

    print(f"File downloaded to: {local_file_path}")

# Example usage
def sundaPredictionModule(filename):
    bucket_name = "rr-gcs-sandbox"
    destination_folder = "temp/"

    download_wav_from_gcs(bucket_name, filename, destination_folder)
    sunda, final_y = predict_output_sunda("temp/test.wav")
    percentage = float(f"{final_y}")*100
    os.remove('temp/'+filename)

    return sunda, percentage

@app.route('/sundapredict', methods=['GET', 'POST'])
def sundaApi():
    if request.method == 'POST':
        try:
            filename = request.json['filename']
            classification, percentage = sundaPredictionModule(filename)
        except Exception:
            respond = jsonify({'message': 'Error'})
            respond.status_code = 400
            return respond
        
        result = {
            "classification": classification,
            "percentage": percentage
        }
        respond = jsonify(result)
        respond.status_code = 200
        return respond
    return 'OK'


if __name__ == '__main__':
    """
    while True:
        output, percentage = sundaPredictionModule()
        print("%s %.5f%%" % (output, percentage))
        break"""
    app.run(host='0.0.0.0')