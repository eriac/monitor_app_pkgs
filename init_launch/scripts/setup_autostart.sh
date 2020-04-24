#! /bin/bash
SCRIPT_DIR=`dirname $0`
SRS_HOME=`readlink -m $SCRIPT_DIR/../../..`
RESOURCE_DIR=`rospack find init_launch`/resources

cp $RESOURCE_DIR/start_ros.sh $SRS_HOME
chmod +x $SRS_HOME/start_ros.sh

sudo cp $RESOURCE_DIR/ros.service /etc/systemd/system/ 
sudo systemctl enable ros.service
sudo systemctl restart ros.service
