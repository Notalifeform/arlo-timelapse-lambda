# arlo-timelapse-lambda
Little AWS lambda function to create periodic snapshots to create a timelapse using a NetGear Arlo Pro Camera

# Introduction 

When looking for a way to create a timelapse using a timelapse using a Arlo camera I bumped into Jeffrey d Walter's Arlo python library that would enable me to accomplish my goal. Runing it on AWS lambda provides a cheap and hassle-free way to host such a repeating task

_UNDER CONSTRUCTION_ 

# Setup environment and dependencies


pip3 install --user pipenv

```
export LC_LOCAL=en_US.UTF-8
export LANG=en_US.UTF-8
```

## Install required pyhton libraries

pipenv install
pipenv install git+https://github.com/jeffreydwalter/arlo


## Install aws CLI
(to work w/ boto3)

```
brew install awscli 
```

## AWS setup S3

Make sure the aws cli and python can write to aws S3

 - create bucket
 - create user
 - assign S3 full rights to user
 - setup was cli access key


## Test locally

set up your environment 

```
export ARLO_USERNAME=user@example.com                                           
export ARLO_PASSWORD=password
export S3_BUCKET_NAME=my.bucket.name 
```

then run

```
make run 
```

it should output something like

```
pipenv run python ./arlosnapshot.py
Looking up sequence number
Creating ARLO snapshot 143
retrieving and storing  snapshot_2018-02-10_23-03-18_000000143.jpg
Script complete at 2018-02-10 23:03:24.209948
```


# create distribution

make clean && make build

# upload your code to AWS Lambda 

https://docs.aws.amazon.com/lambda/latest/dg/with-scheduledevents-example.html

!name function properly

```
*/10 6-18 ? * MON-FRI *
```

# Download pictures and create timelapse

```
brew install libvpx
brew install ffmpeg --with-libvpx
```
and run

```
./tools/create-slideshow.sh
```

this should

* download all your snapshots
* symlink them so ffmpeg can find them
* create a movie using ffmpeg

_the ffmpeg command line will probably need some tuning to fit your situation/preferences_

# Next steps

* encrypt your username and password 

# See also

* arlo pyhton library - https://github.com/jeffreydwalter/arlo
* make files for AWS Lambda - https://github.com/browniebroke/hello-lambda
* ffmpeg commands fro creating slideshows - http://hamelot.io/visualization/using-ffmpeg-to-convert-a-set-of-images-into-a-video/

