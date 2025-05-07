# Use the official Python 3.13.3 image as the base image.
# This image comes with Python pre-installed.
FROM python:3.13.3

# Set the working directory inside the container to `/app`.
# All subsequent commands will be executed in this directory.
WORKDIR /app

# Copy the `requirements.txt` file from the host machine to the container.
# This file contains the list of Python dependencies required for the project.
COPY requirements.txt .

# Install the Python dependencies listed in `requirements.txt` using pip.
RUN pip install -r requirements.txt

# Copy the `src` folder from the host machine to the container.
# This folder contains the application source code.
COPY src/ ./src/

# Copy the `tests` folder from the host machine to the container.
# This folder contains the test scripts for the application.
COPY src/tests/ .src/tests/

# Define the command to run the application when the container starts.
# Here, it runs the `main.py` script located in the `src/app` directory.
CMD ["python3", "src/app/main.py"]