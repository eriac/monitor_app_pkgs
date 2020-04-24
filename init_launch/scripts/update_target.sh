#! /bin/bash

TARGET_USER=${TARGET_USER:-admin}
TARGET_IP=${TARGET_IP:-192.168.2.91}
SCRIPT_DIR=`dirname $0`
SOURCE_DIR=`readlink -m $SCRIPT_DIR/../..`

echo "SOURCE_DIR="$SOURCE_DIR
echo "TARGET="$TARGET_USE"@"$TARGET_IP

scp -r $SOURCE_DIR $TARGET_USER"@"$TARGET_IP":/home/"$TARGET_USER"/ros/"