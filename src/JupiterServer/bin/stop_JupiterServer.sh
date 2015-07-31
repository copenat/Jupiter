#! /bin/bash

me=`whoami`
pids=`ps auxww | grep -i runserver | grep -i $me | grep -iv grep | awk '{print $2}'`
if [ "$pids" != "" ]; then
    echo "Killing: "
    echo `ps auxww | grep -i runserver | grep -i $me | grep -iv grep`
    kill $pids
fi



