# arlo-timelapse-lambda
Simpe AWS lambda function to create a timelapse movie by creating periodic snapshots using a NetGear Arlo Pro Camera and ffmpeg (on a local machine)

# Introduction 

When looking for a way to create a timelapse using a Arlo camera I bumped into [Jeffrey d Walter's Arlo python library](https://github.com/jeffreydwalter/arlo) that has all the functionality required. Running the code on AWS lambda provides a cheap (first year should be within the AWS free tier) and hassle-free way to host such a repeating task.

The script works like this:

* AWS triggers a snapshot every 10 minutes (configurable in AWS)
* Lambda function triggers a snapshot through the Arlo cloud endpoint
* Lambda function retrieves and stores the snapshot in a private S3 bucket
* On your desktop: grab all images and construct a timelapse uing ffmpeg


Below are the steps I took to get everything up and running on OSX (other platforms should also work, but the commands will be a bit different)


# Setup environment and dependencies

Install [python](https://www.python.org/downloads/) - or you can install it using homebrew (OSX)

Install pipenv

```
pip3 install --user pipenv
```

_depending on your install the command could be 'pip' instead of 'pip3'. I had to run the commands below to set up the enviroment properly_

```
export LC_LOCAL=en_US.UTF-8
export LANG=en_US.UTF-8
```

## Clone this project

```
git clone https://github.com/Notalifeform/arlo-timelapse-lambda
```

## Install required pyhton libraries

In your project directory run

```
pipenv install
```

## Install aws CLI

The aws library boto3 uses the aws CLI configuration to access S3, we'll also use it later to retrieve the snapshots.

```
brew install awscli 
```

## AWS setup S3

First sign up for an AWS account

Make sure the aws cli and python can write to aws S3

 - create bucket
 - create user
 - assign S3 full rights to user
 - setup was cli access key locally

see https://boto3.readthedocs.io/en/latest/guide/quickstart.html


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
Creating ARLO snapshot 1
retrieving and storing  snapshot_2018-02-10_23-03-18_000000143.jpg
Script complete at 2018-02-10 23:03:24.209948
```


# Create distribution

in your project directory run

```
make clean && make build
```

# Upload your code to AWS Lambda 

This is a good start to create a first version of your function

https://docs.aws.amazon.com/lambda/latest/dg/with-scheduledevents-example.html

When you upload `delivery.zip` make sure to set the handler to `arlosnapshot.lambda_handler`

The trigger you can set to something like `*/10 6-18 ? * MON-FRI *` (in this case: weekday create a snapshot every 10 minutes from 6AM to 6PM - GMT)

# Downloading pictures and creating the timelapse

## Install dependencies

```
brew install libvpx
brew install ffmpeg --with-libvpx
```

## Create the timelapse

Run from your snapshot dir (asuming it is next to your project dir)

```
../snapshot-lambda/tools/create-slideshow.sh
```

this should

* download all your snapshots
* symlink them so ffmpeg can find them
* create a movie using ffmpeg

_the ffmpeg command line will probably need some tuning to fit your situation/preferences_

# Thank you

Big thanks to [jeffdwalter](https://github.com/jeffreydwalter/) for providing the pyhton library and quickly fixing a threading issue that I ran into using this library on AWS Lambda.


# See also

* arlo pyhton library - https://github.com/jeffreydwalter/arlo
* make files for AWS Lambda - https://github.com/browniebroke/hello-lambda
* ffmpeg commands fro creating slideshows - http://hamelot.io/visualization/using-ffmpeg-to-convert-a-set-of-images-into-a-video/

