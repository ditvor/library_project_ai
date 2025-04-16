#!/bin/bash

echo "Testing Docker setup for Library Management System"
echo "=================================================="

# Build the Docker image
echo "Building Docker image..."
docker build -t library-system-test .

# Run a simple test command
echo "Running test command..."
docker run --rm library-system-test python -c "from library_system import Library; lib = Library('Test'); print(f'Library \"{lib.name}\" created successfully!')"

# Check the exit code
if [ $? -eq 0 ]; then
    echo "Test passed! Docker setup is working correctly."
else
    echo "Test failed! Please check your Docker setup."
fi

echo "=================================================="
echo "To run the full application, use: docker-compose up -d"
echo "Then attach to the container with: docker attach library-management-system"