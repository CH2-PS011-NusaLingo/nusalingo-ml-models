from flask import Flask, request, jsonify
from google.cloud import storage
import os

import sys
sys.path.append('Sunda/')
from sunda import predict_output_sunda

app = Flask(__name__)

def download_wav_from_gcs(bucket_name, filename, destination_folder):
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
    #Bucket name and Folder name variables
    bucket_name = "nusalingo-resources"
    destination_folder = "temp/"

    #download the file from GCS to the local folder
    download_wav_from_gcs(bucket_name, filename, destination_folder)

    #using the ml model to predict the output
    sunda, final_y = predict_output_sunda("temp/test.wav")

    #converting the result to a percentage
    try:
        percentage = float(f"{final_y}")*100
    except:
        percentage = 0

    #deleting the temporary file
    os.remove('temp/'+filename)

    #return the percentage and classification result
    return sunda, percentage


#GET and POST functions for '/sundapredict'
@app.route('/sundapredict', methods=['GET', 'POST'])
def sundaApi():

    #POST method
    if request.method == 'POST':
        #request and response if not error
        try:
            filename = request.json['filename']
            classification, percentage = sundaPredictionModule(filename)
        #error handling, returning 400 as status code and error message
        except Exception:
            respond = jsonify({'message': 'Error'})
            respond.status_code = 400
            return respond
        
        #building the result.json file
        result = {
            "classification": classification,
            "percentage": percentage
        }
        respond = jsonify(result)
        respond.status_code = 200
        
        #responding to the client request
        return respond
    return 'OK'


if __name__ == '__main__':
    """
    while True:
        output, percentage = sundaPredictionModule()
        print("%s %.5f%%" % (output, percentage))
        break"""
    #Running the application
    app.run(host='0.0.0.0')