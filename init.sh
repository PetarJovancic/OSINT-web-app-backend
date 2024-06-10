#THEHARVERSTER
if [ ! -d "src/api/theHarvester" ]; then
  echo "Cloning theHarvester repository..."
  git clone https://github.com/laramies/theHarvester.git src/api/theHarvester
else
  echo "theHarvester repository already exists."
fi

echo "Building theHarvester Docker image..."
cd src/api/theHarvester || exit
docker build -t theharvester .
cd ../../../

#AMASS
if [ ! -d "src/api/amass" ]; then
  echo "Cloning amass repository..."
  git clone https://github.com/owasp-amass/amass.git src/api/amass
else
  echo "amass repository already exists."
fi

echo "Building amass Docker image..."
cd src/api/amass || exit
docker build -t amass .
cd ../../../