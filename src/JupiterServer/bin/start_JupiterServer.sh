#! /bin/bash

_whence="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
_property_dir="$( cd "$_whence/../../properties" && pwd )"
_python="$( cd "$_whence/../../PythonLinux/bin" && pwd )"
if [ $? -ne 0 ]; then
    echo "ERROR: PythonLinux is a requirement to starting JupiterServer. Add PythonLinux application to this grid and deploy."
    exit 1
fi

function check_dependancy {
    appname=$1
    _dep="$( cd "$_whence/../../$appname" && pwd )"
    if [ $? -ne 0 ]; then
        echo "ERROR: $appname is a requirement to starting JupiterServer. Add $appname application to this grid and deploy."
        exit 1
    fi
    export PYTHONPATH=$PYTHONPATH:$_dep
}
check_dependancy PythonDjango
check_dependancy PythonRestFramework
check_dependancy PythonGoogleFinance

if [ -f "$_property_dir/grid.properties" ]; then
    source $_property_dir/grid.properties
fi

# if property file is in dos format then convert to unix style
host=`echo ${jupiter_http_host} | tr -d '\r'`
port=`echo ${jupiter_http_port} | tr -d '\r'`

export empty_dbfile=$_whence/../db/jupiterdb.sqlite3

# The live version of this db will be stored locally
export dbfile=$HOME/db/jupiterdb.sqlite3

export logfile=$HOME/logs/JupiterServer.$$.log

cd $_whence/../web
$_python/python3 manage.py runserver $host:$port


