
import os
from datetime import datetime
from Arlo import Arlo
from pprint import pprint
import time
import threading


USERNAME = os.environ['ARLO_USERNAME']
PASSWORD = os.environ['ARLO_PASSWORD']

sequence = 0
def lambda_handler(event, context, sequence):
    print('Creating ARLO snapshot {}'.format(sequence))
    try:
        arlo = Arlo(USERNAME, PASSWORD)
        basestations = arlo.GetDevices('basestation')
        cameras = arlo.GetDevices('camera')
        snapshot_url = arlo.TriggerFullFrameSnapshot(basestations[0], cameras[0])
        tag = datetime.now().strftime('%Y-%m-%d_%H-%M-%S')
        filename = 'snapshot_{}_{}.jpg'.format(tag, "{:09d}".format(sequence))
        print('retrieving and storing  {}'.format(filename))
        arlo.DownloadSnapshot(snapshot_url, '/tmp/' + filename)
        print('Script complete at {}'.format(str(datetime.now())))
        arlo.Logout()
    except Exception as e:
        print(e)


while True:
  print("thread count: {}".format(threading.active_count()))
  lambda_handler(None, None, sequence)
  sequence = sequence + 1
  print('done. sleeping')
  time.sleep(10)

