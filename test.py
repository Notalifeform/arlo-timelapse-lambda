import arlosnapshot
import time

while True:
  arlosnapshot.lambda_handler({"time": "2018-01-01"}, None)
  print('done. sleeping')
  time.sleep(1)