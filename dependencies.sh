#!/bin/bash

cd ./src/api/theHarvester || exit
docker build -t theharvester .

cd ..

docker image pull caffix/amass
