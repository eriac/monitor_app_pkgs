#! /bin/bash

SCRIPT_DIR=`dirname $0`
source $SCRIPT_DIR/install/setup.bash
export ROS_HOME=~/ros
export ROS_IP=`hostname -I|cut -d' ' -f1`
mkdir -p $ROS_HOME/mongodb
roslaunch monitor_app main.launch
