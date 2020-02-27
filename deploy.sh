#!/usr/bin/env bash
sam build -t template.yaml

sam package \
    --s3-bucket rawley-sam-package \
    --output-template-file packaged.yaml \
    --template-file ./.aws-sam/build/template.yaml

sam deploy \
    --template-file packaged.yaml \
    --stack-name arlo-snapshot \
    --capabilities CAPABILITY_NAMED_IAM CAPABILITY_AUTO_EXPAND
