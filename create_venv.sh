#!/bin/bash

env_path=~/venvs/${PWD##*/}
PYTHON3=/opt/homebrew/bin/python3.10

if [ -d $env_path ]; then
        echo Deleting old environment...
        rm -rf $env_path
fi

if [ ! -d $env_path ]; then
        echo Creating new environment...
        mkdir -p $env_path
        $PYTHON3 -m venv $env_path
fi

if [ -d $env_path ]; then
        echo Upgrading pip...
        $PYTHON3 -m pip install --upgrade pip -q
        echo Activating...
        source $env_path/bin/activate
        $PYTHON3 -m pip install --upgrade pip -q

        if test -f "requirements.txt"; then
                for req in $(find . -name 'requirements.txt'); do
                        echo "Installing/Updating requirements from $req ..........."
                        pip3 install -r $req
        done
    fi
fi
