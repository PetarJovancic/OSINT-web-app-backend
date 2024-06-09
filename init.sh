#!/bin/bash

# Clone the external API repository if it does not exist
if [ ! -d "src/api/theHarvester" ]; then
  echo "Cloning theHarvester repository..."
  git clone https://github.com/laramies/theHarvester.git src/api/theHarvester
else
  echo "theHarvester repository already exists."
fi

# Build the theHarvester Docker image
echo "Building theHarvester Docker image..."
cd src/api/theHarvester || exit
docker build -t theharvester .
cd ../../../
