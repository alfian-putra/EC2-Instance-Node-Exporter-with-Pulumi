#!/usr/bin/bash

export AWS_ACCESS_KEY_ID=""
export AWS_SECRET_ACCESS_KEY=""
export AWS_REGION="us-east-1"
export AWS_EC2_AMI="ami-0b6d9d3d33ba97d99" # jammy jellyfish
export AWS_EC2_INSTANCE_TYPE="t3.micro"

export AWS_EC2_INSTANCE_NAME="example_server_1"
export AWS_EC2_USER="ubuntu"

export PUBLIC_KEY=$(cat ~/.ssh/id_rsa.pub)

export NODE_EXPORTER_VERSION="1.12.1"
export NODE_EXPORTER_USER="admin"
export NODE_EXPORTER_PLAIN_PASSWORD="AdminPassword123!"
