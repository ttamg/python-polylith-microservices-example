#!/bin/bash

# A script to poetry build and docker build the following list of projects

WORKSPACE="mousetrap"
PROJECTS=("api_app" "worker_1" "worker_2")

# Get all subdirectories
cd projects
for project in ${PROJECTS[@]}; do
    cd $project
    poetry build-project
    docker build -t $WORKSPACE/$project .
    cd ..
done

echo "Done."
