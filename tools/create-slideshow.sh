#!/bin/bash

echo "syncing images"
aws s3 sync s3://$S3_BUCKET_NAME/ .  > /dev/null

echo "creating symlinks"


for i in snapshot_201* ; do
    y=`echo $i | sed -e 's/_.*_//'`; 
    ln -fs $i $y
done

filename="snapshot-"`date +'%Y-%m-%d'`".mp4"
echo "creating movie $filename"

ffmpeg -y -r 30 -f image2 -s 1280x720 -i snapshot%09d.jpg -start_number 6 -vcodec libx264 -crf 25 -pix_fmt yuv420p -loglevel panic $filename

echo "movie $filename is ready"
