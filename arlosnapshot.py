
import os
import boto3
import botocore
from datetime import datetime
from urllib.request import urlopen
from Arlo import Arlo
from pprint import pprint
import base64
from base64 import b64decode

s3 = boto3.resource('s3')

USERNAME_ENC = os.environ['ARLO_USERNAME']
PASSWORD_ENC = os.environ['ARLO_PASSWORD']
S3_BUCKET_NAME = os.environ['S3_BUCKET_NAME']

if '@' not in USERNAME_ENC:
    USERNAME = boto3.client('kms').decrypt(CiphertextBlob=b64decode(USERNAME_ENC))['Plaintext'].decode('utf-8')
    PASSWORD = boto3.client('kms').decrypt(CiphertextBlob=b64decode(PASSWORD_ENC))['Plaintext'].decode('utf-8')
else:
    # string was not encrypted
    USERNAME = USERNAME_ENC
    PASSWORD = PASSWORD_ENC




def lambda_handler(event, context):
    print('Looking up sequence number')
    sequence = 0
    try:
        s3.Bucket(S3_BUCKET_NAME).download_file('sequence.txt', '/tmp/sequence.txt')
        with open('/tmp/sequence.txt', 'r') as myfile:
          data=myfile.read().replace('\n', '')
          sequence = int(data)
    except botocore.exceptions.ClientError as e:
        if e.response['Error']['Code'] == "404":
            print("Sequence file does not exist")
        else:
            raise
    sequence = sequence + 1 
    print('Creating ARLO snapshot {}'.format(sequence))
    try:
        # Instantiating the Arlo object automatically calls Login(), which returns an oAuth token that gets cached.
        # Subsequent successful calls to login will update the oAuth token.
        arlo = Arlo(USERNAME, PASSWORD)
        # At this point you're logged into Arlo.

        # Get the list of devices and filter on device type to only get the basestation.
        # This will return an array which inclbakkerlvl14udes all of the basestation's associated metadata.
        basestations = arlo.GetDevices('basestation')
        #print("BASE: {}".format(basestations))

        # Get the list of devices and filter on device type to only get the camera.
        # This will return an array which includes all of the camera's associated metadata.
        cameras = arlo.GetDevices('camera')
        #print("CAMERA: {}".format(cameras))

        # Tells the Arlo basestation to trigger a snapshot on the given camera.
        # This snapshot is not instantaneous, so this method waits for the response and returns the url
        # for the snapshot, which is stored on the Amazon AWS servers.
        snapshot_url = arlo.TriggerFullFrameSnapshot(basestations[0], cameras[0])

        # This method requests the snapshot for the given url and writes the image data to the location specified.
        # In this case, to the current directory as a file named "snapshot.jpg"
        # Note: Snapshots are in .jpg format.
        tag = datetime.now().strftime('%Y-%m-%d_%H-%M-%S')
        filename = 'snapshot_{}_{}.jpg'.format(tag, "{:09d}".format(sequence))

        while  snapshot_url == None:
            print("RETRY...")
            def callback(basestation, event):
                print("Re-grab event: {}".format(event))
                if event.get("from") == basestation.get("deviceId") and event.get("resource") == "cameras/"+camera.get("deviceId") and event.get("action") == "fullFrameSnapshotAvailable":
                    return event.get("properties", {}).get("presignedFullFrameSnapshotUrl")
                return None
            snapshot_url = self.HandleEvents(basestation, callback)

        print('retrieving and storing  {}'.format(filename))
        arlo.DownloadSnapshot(snapshot_url, '/tmp/' + filename)
        data = open('/tmp/' + filename, 'rb')
        s3.Bucket(S3_BUCKET_NAME).put_object(Key=filename, Body=data)


        # store the sequence
        fh = open("/tmp/sequence.txt","w")
        fh.write(str(sequence))
        fh.close()

        data = open('/tmp/sequence.txt', 'rb')
        s3.Bucket(S3_BUCKET_NAME).put_object(Key='sequence.txt', Body=data)

        arlo.Logout()
        print('Script complete at {}'.format(str(datetime.now())))
    except Exception as e:
        print(e)

if __name__ == '__main__':
    lambda_handler({"time": "2018-01-01"}, None)