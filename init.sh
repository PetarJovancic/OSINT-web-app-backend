# Building theHarvester Docker image directly from the repository
echo "Building theHarvester Docker image directly from the repository..."
docker build -t theharvester https://github.com/laramies/theHarvester.git#master

# Building Amass Docker image directly from the repository
echo "Building Amass Docker image directly from the repository..."
docker build -t amass https://github.com/owasp-amass/amass.git#master
