from google.cloud import storage
import os

import sys
sys.path.append('Sunda/')
from sunda import predict_output_sunda

def download_wav_from_gcs(bucket_name, file_name, destination_folder):
    """
    Download a .wav file from Google Cloud Storage and save it to a local folder.

    :param bucket_name: Name of the GCS bucket.
    :param file_name: Name of the .wav file in the GCS bucket.
    :param destination_folder: Local folder to save the downloaded .wav file.
    """
    # Set Google Cloud Storage credentials (replace 'path/to/your/keyfile.json' with your actual key file path)
    os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "key.json"

    # Create a GCS client
    client = storage.Client()

    # Get the GCS bucket and file
    bucket = client.get_bucket(bucket_name)
    blob = bucket.blob(file_name)

    # Create the destination folder if it doesn't exist
    os.makedirs(destination_folder, exist_ok=True)

    # Specify the local file path to save the downloaded .wav file
    local_file_path = os.path.join(destination_folder, file_name)

    # Download the file from GCS to the local folder
    blob.download_to_filename(local_file_path)

    print(f"File downloaded to: {local_file_path}")

# Example usage
def sundaPredictionModule():
    bucket_name = "rr-gcs-sandbox"
    file_name = "test.wav"
    destination_folder = "temp/"

    download_wav_from_gcs(bucket_name, file_name, destination_folder)
    sunda, final_y = predict_output_sunda("temp/test.wav")
    percentage = float(f"{final_y}")*100
    os.remove('temp/'+file_name)

    return sunda, percentage

if __name__ == '__main__':
    while True:
        output, percentage = sundaPredictionAPI()
        print("%s %.5f%%" % (output, percentage))
        break